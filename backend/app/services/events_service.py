"""
Event service layer.

Provides ingestion with deduplication, validation, and batch handling.
Separates API routes from business logic for clarity and testability.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from .. import crud, schemas


def _validate_worker_and_station(db: Session, worker_id: str, workstation_id: str) -> None:
    """Ensure referenced worker/workstation exist."""
    if not crud.get_worker(db, worker_id):
        raise HTTPException(status_code=404, detail=f"Worker {worker_id} not found. Seed data first.")
    if not crud.get_workstation(db, workstation_id):
        raise HTTPException(status_code=404, detail=f"Workstation {workstation_id} not found. Seed data first.")


def ingest_event(db: Session, event: schemas.AIEventCreate) -> Dict[str, Any]:
    """
    Ingest a single AI event with idempotent deduplication.
    
    **Deduplication Logic**:
    Events are identified by a composite key: (timestamp, worker_id, event_type).
    This prevents duplicate ingestion when edge devices retry POSTs due to network timeouts.
    
    **Design**:
    - If the same (timestamp, worker_id, event_type) tuple exists in the database,
      the duplicate is silently ignored and the existing record is returned.
    - Uniqueness is enforced at the database layer via SQL UNIQUE INDEX, ensuring
      consistency even under concurrent writes.
    - This approach is idempotent: multiple POST calls with identical events yield
      the same result (exactly-once semantics).
    
    **Example**:
    Edge device at 14:30:00 observes worker W1 "working". It POSTs the event.
    If the network times out, the device retries at 14:30:05 with the same event.
    The second POST detects the duplicate by (14:30:00, W1, working) and returns
    the existing record without re-inserting.
    
    **Parameters**:
    - db: SQLAlchemy session
    - event: AIEventCreate schema with (timestamp, worker_id, workstation_id, event_type, confidence, count)
    
    **Returns**:
    - {"duplicate": False, "event": <newly created AIEvent>} if new
    - {"duplicate": True, "event": <existing AIEvent>} if deduped
    
    **Raises**:
    - HTTPException(404) if worker or workstation not found
    - IntegrityError if database constraint violations occur
    """
    _validate_worker_and_station(db, event.worker_id, event.workstation_id)

    duplicate = crud.get_event_by_identity(db, event.timestamp, event.worker_id, event.event_type)
    if duplicate:
        return {"duplicate": True, "event": duplicate}

    created = crud.create_ai_event(db, event)
    return {"duplicate": False, "event": created}


def ingest_batch(db: Session, events: List[schemas.AIEventCreate]) -> schemas.AIEventBatchResponse:
    """
    Batch ingest multiple events with atomic-per-event error handling.
    
    **Batch Processing Strategy**:
    This function processes events sequentially, maintaining granular error tracking.
    Each event is independently evaluated for duplicates and validation errors,
    allowing partial success (e.g., 50 new events ingested, 10 duplicates skipped, 5 errors logged).
    
    **Use Case**:
    When edge devices batch-upload events (e.g., 100 events collected over 1 hour),
    network failures, or server restarts may have caused some events to already exist.
    This approach ensures:
    1. No duplicate re-insertion (atomic deduplication)
    2. Detailed error logs for operations teams (which events failed and why)
    3. Resilience (failures don't cascade; partial batches complete)
    
    **Idempotency**:
    If the same batch is POSTed twice:
    - First call: success_count=100, duplicate_count=0
    - Second call: success_count=0, duplicate_count=100 (all marked as duplicates)
    Result: Exactly-once semantic preservation; safe to retry.
    
    **Parameters**:
    - db: SQLAlchemy session
    - events: List of AIEventCreate; batch size typically 1–1000 events
    
    **Returns**:
    - AIEventBatchResponse with:
      - success_count: newly inserted events
      - duplicate_count: skipped due to existing (timestamp, worker_id, event_type)
      - error_count: validation failures (worker/workstation not found, schema errors, etc.)
      - errors: list of error messages for debugging
    
    **Performance**:
    O(n * m) where n = batch size, m = avg. dedup query time (~1ms per event).
    For n=1000, expect ~1–2 seconds end-to-end including database writes.
    
    **Example Response**:
    {
      "success_count": 85,
      "duplicate_count": 12,
      "error_count": 3,
      "errors": [
        "W7@S4 2026-01-21T14:30:00Z: Worker W7 not found. Seed data first.",
        "W1@S1 2026-01-21T14:31:00Z: Invalid event_type 'unknown'",
        "W2@S3 2026-01-21T14:32:00Z: Confidence 0.5 below threshold (0.7)"
      ]
    }
    """
    success = 0
    duplicate = 0
    errors: List[str] = []

    for ev in events:
        try:
            result = ingest_event(db, ev)
            if result["duplicate"]:
                duplicate += 1
            else:
                success += 1
        except HTTPException as exc:  # validation issues
            errors.append(f"{ev.worker_id}@{ev.workstation_id} {ev.timestamp}: {exc.detail}")
        except Exception as exc:
            errors.append(f"{ev.worker_id}@{ev.workstation_id} {ev.timestamp}: {str(exc)}")

    return schemas.AIEventBatchResponse(
        success_count=success,
        duplicate_count=duplicate,
        error_count=len(errors),
        errors=errors,
    )


def fetch_events(
    db: Session,
    worker_id: Optional[str] = None,
    workstation_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 1000,
    chronological: bool = False,
):
    """Wrapper to fetch events with optional chronological order."""
    events = crud.get_events(db, worker_id, workstation_id, start_time, end_time, limit)
    if chronological:
        return list(reversed(events))  # crud returns newest first
    return events
