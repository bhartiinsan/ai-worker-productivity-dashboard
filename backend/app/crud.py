"""
CRUD Operations for Database Access

Provides functions for:
- Event ingestion with deduplication
- Worker and workstation management
- Event querying
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from typing import List, Optional, Dict, Any
import logging

from . import models, schemas

logger = logging.getLogger(__name__)


# ========================================
# Worker Operations
# ========================================

def get_worker(db: Session, worker_id: str) -> Optional[models.Worker]:
    """Get worker by ID."""
    return db.query(models.Worker).filter(models.Worker.id == worker_id).first()


def get_workers(db: Session) -> List[models.Worker]:
    """Get all workers."""
    return db.query(models.Worker).all()


def create_worker(db: Session, worker: schemas.WorkerCreate) -> models.Worker:
    """Create a new worker."""
    db_worker = models.Worker(**worker.dict())
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker


# ========================================
# Workstation Operations
# ========================================

def get_workstation(db: Session, workstation_id: str) -> Optional[models.Workstation]:
    """Get workstation by ID."""
    return db.query(models.Workstation).filter(models.Workstation.id == workstation_id).first()


def get_workstations(db: Session) -> List[models.Workstation]:
    """Get all workstations."""
    return db.query(models.Workstation).all()


def create_workstation(db: Session, workstation: schemas.WorkstationCreate) -> models.Workstation:
    """Create a new workstation."""
    db_workstation = models.Workstation(**workstation.dict())
    db.add(db_workstation)
    db.commit()
    db.refresh(db_workstation)
    return db_workstation


# ========================================
# AI Event Operations
# ========================================

def create_ai_event(db: Session, event: schemas.AIEventCreate) -> Optional[models.AIEvent]:
    """
    Create a new AI event with deduplication.
    
    Returns:
        - AIEvent if created successfully
        - None if duplicate (based on unique constraint)
    
    Handles:
        - Duplicate events gracefully
        - Foreign key validation
    """
    try:
        db_event = models.AIEvent(**event.dict())
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event
    except IntegrityError as e:
        db.rollback()
        if "uix_event_dedup_worker_type" in str(e):
            logger.debug(f"Duplicate event ignored: {event.dict()}")
            return None
        logger.error(f"Event creation error: {e}")
        raise


def get_event_by_identity(db: Session, timestamp: datetime, worker_id: str, event_type: str) -> Optional[models.AIEvent]:
    """Fetch an event by the deduplication key."""
    return (
        db.query(models.AIEvent)
        .filter(
            models.AIEvent.timestamp == timestamp,
            models.AIEvent.worker_id == worker_id,
            models.AIEvent.event_type == event_type,
        )
        .first()
    )


def get_events(
    db: Session,
    worker_id: Optional[str] = None,
    workstation_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 1000
) -> List[models.AIEvent]:
    """
    Get AI events with optional filters.
    
    Supports filtering by worker, workstation, and time range.
    Results are ordered by timestamp (newest first).
    """
    query = db.query(models.AIEvent)
    
    if worker_id:
        query = query.filter(models.AIEvent.worker_id == worker_id)
    if workstation_id:
        query = query.filter(models.AIEvent.workstation_id == workstation_id)
    if start_time:
        query = query.filter(models.AIEvent.timestamp >= start_time)
    if end_time:
        query = query.filter(models.AIEvent.timestamp <= end_time)
    
    return query.order_by(models.AIEvent.timestamp.desc()).limit(limit).all()
