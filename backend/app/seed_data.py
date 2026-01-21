"""
Seed Data Generator

Creates sample workers, workstations, and AI events for testing and demonstration.
Can be called via API endpoint to populate or refresh database.
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from . import models, schemas, crud
from .constants import WORKER_IDS, WORKSTATION_IDS, SEED_INTERVAL_MINUTES


# ========================================
# Seed Data Constants
# ========================================

WORKERS_DATA = [
    {"id": "W1", "name": "John Smith", "shift": "morning", "department": "Assembly"},
    {"id": "W2", "name": "Maria Garcia", "shift": "morning", "department": "Assembly"},
    {"id": "W3", "name": "Ahmed Hassan", "shift": "evening", "department": "Quality Control"},
    {"id": "W4", "name": "Yuki Tanaka", "shift": "evening", "department": "Packaging"},
    {"id": "W5", "name": "Sarah Johnson", "shift": "night", "department": "Assembly"},
    {"id": "W6", "name": "Carlos Rodriguez", "shift": "night", "department": "Quality Control"},
]

WORKSTATIONS_DATA = [
    {"id": "S1", "name": "Assembly Line 1", "location": "Floor A", "type": "assembly"},
    {"id": "S2", "name": "Assembly Line 2", "location": "Floor A", "type": "assembly"},
    {"id": "S3", "name": "Quality Check Station", "location": "Floor B", "type": "inspection"},
    {"id": "S4", "name": "Packaging Station 1", "location": "Floor C", "type": "packaging"},
    {"id": "S5", "name": "Packaging Station 2", "location": "Floor C", "type": "packaging"},
    {"id": "S6", "name": "Final Inspection", "location": "Floor B", "type": "inspection"},
]


def seed_workers(db: Session) -> int:
    """
    Seed workers with predefined metadata.
    
    Returns: Number of workers created
    """
    created_count = 0
    for worker_data in WORKERS_DATA:
        if not crud.get_worker(db, worker_data["id"]):
            worker = schemas.WorkerCreate(**worker_data)
            crud.create_worker(db, worker)
            created_count += 1
    return created_count


def seed_workstations(db: Session) -> int:
    """
    Seed workstations with predefined metadata.
    
    Returns: Number of workstations created
    """
    created_count = 0
    for workstation_data in WORKSTATIONS_DATA:
        if not crud.get_workstation(db, workstation_data["id"]):
            workstation = schemas.WorkstationCreate(**workstation_data)
            crud.create_workstation(db, workstation)
            created_count += 1
    return created_count


def seed_sample_events(db: Session, hours_back: int = 24) -> int:
    """
    Generate sample AI events for the last N hours.
    
    Creates realistic event patterns:
    - Working, idle, and absent states
    - Product count events
    - Varying confidence scores
    - Random but realistic worker/workstation assignments
    
    Args:
        hours_back: Number of hours of historical data to generate
    
    Returns: Number of events created
    """
    events = []
    current_time = datetime.utcnow()
    
    # Generate events at intervals
    total_intervals = (hours_back * 60) // SEED_INTERVAL_MINUTES
    
    # Track last state for each worker to create realistic transitions
    worker_states = {w: "absent" for w in WORKER_IDS}
    worker_station_map = {}
    
    for i in range(total_intervals):
        timestamp = current_time - timedelta(minutes=i * SEED_INTERVAL_MINUTES)
        
        # Randomly select 3-5 workers to be active at this time
        active_workers = random.sample(WORKER_IDS, random.randint(3, 5))
        
        for worker_id in active_workers:
            # Assign worker to a workstation (sticky - stays at same station)
            if worker_id not in worker_station_map:
                worker_station_map[worker_id] = random.choice(WORKSTATION_IDS)
            
            workstation_id = worker_station_map[worker_id]
            
            # Determine event type based on previous state
            if worker_states[worker_id] == "absent":
                event_type = "working"
            else:
                # 70% working, 20% idle, 10% product_count
                rand = random.random()
                if rand < 0.7:
                    event_type = "working"
                elif rand < 0.9:
                    event_type = "idle"
                else:
                    event_type = "product_count"
            
            # Generate confidence score and count
            confidence = random.uniform(0.85, 0.99)
            count = random.randint(1, 3) if event_type == "product_count" else 1
            
            # Update worker state
            worker_states[worker_id] = event_type
            
            events.append(schemas.AIEventCreate(
                timestamp=timestamp,
                worker_id=worker_id,
                workstation_id=workstation_id,
                event_type=event_type,
                confidence=confidence,
                count=count
            ))
    
    # Insert events using the service layer
    from .services.events_service import ingest_batch
    result = ingest_batch(db, events)
    return result.success_count


def clear_all_data(db: Session):
    """
    Clear all data from database (for refresh operation).
    WARNING: This deletes all data!
    """
    db.query(models.AIEvent).delete()
    db.query(models.Worker).delete()
    db.query(models.Workstation).delete()
    db.commit()


def seed_database(db: Session, clear_existing: bool = False, hours_back: int = 24) -> dict:
    """
    Main seeding function.
    
    Args:
        clear_existing: If True, clears all existing data first
        hours_back: Number of hours of sample events to generate
    
    Returns: Dictionary with creation counts
    """
    if clear_existing:
        clear_all_data(db)
    
    workers_created = seed_workers(db)
    workstations_created = seed_workstations(db)
    events_created = seed_sample_events(db, hours_back)
    
    return {
        "workers_created": workers_created,
        "workstations_created": workstations_created,
        "events_created": events_created
    }
