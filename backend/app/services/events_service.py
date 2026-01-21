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
    """Ingest a single event with deduplication and validation."""
    _validate_worker_and_station(db, event.worker_id, event.workstation_id)

    duplicate = crud.get_event_by_identity(db, event.timestamp, event.worker_id, event.event_type)
    if duplicate:
        return {"duplicate": True, "event": duplicate}

    created = crud.create_ai_event(db, event)
    return {"duplicate": False, "event": created}


def ingest_batch(db: Session, events: List[schemas.AIEventCreate]) -> schemas.AIEventBatchResponse:
    """Batch ingest with per-event deduplication."""
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
