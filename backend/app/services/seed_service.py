"""
Admin seeding service using Faker to generate realistic 24h telemetry.
"""

from datetime import datetime, timedelta
import random
from typing import Dict

from faker import Faker
from sqlalchemy.orm import Session

from .. import schemas, models
from .events_service import ingest_batch
from ..seed_data import seed_workers, seed_workstations
from ..constants import WORKER_IDS, WORKSTATION_IDS

fake = Faker()


def admin_seed(db: Session, clear_existing: bool = False) -> Dict[str, int]:
    """
    Generate 24h of INDUSTRY-REALISTIC events with:
    - Lunch Dip: 45min of 0% productivity at 1:00 PM
    - Slow Start: Lower productivity in first 30min of shift
    - Correlation: product_count ONLY during 'working' state
    """
    if clear_existing:
        db.query(models.AIEvent).delete()
        db.commit()

    # Ensure base data using shared seed functions
    seed_workers(db)
    seed_workstations(db)

    # generate events
    now = datetime.utcnow()
    interval_minutes = 5
    total_intervals = int(24 * 60 / interval_minutes)

    worker_states = {w: "absent" for w in WORKER_IDS}
    worker_station_map = {w: random.choice(WORKSTATION_IDS) for w in WORKER_IDS}

    events = []
    for i in range(total_intervals):
        ts = now - timedelta(minutes=interval_minutes * (total_intervals - i))
        hour_of_day = ts.hour
        minute_of_day = ts.hour * 60 + ts.minute
        
        # ELITE FEATURE 1: "Lunch Dip" - 45min break at 1:00 PM (13:00)
        is_lunch_break = (hour_of_day == 13 and ts.minute < 45)
        
        # ELITE FEATURE 2: "Slow Start" - First 30min of shift (morning 6-6:30 AM)
        is_slow_start = (hour_of_day == 6 and ts.minute < 30)
        
        for worker_id in WORKER_IDS:
            # Lunch break overrides all - everyone goes absent/idle
            if is_lunch_break:
                state = "absent" if random.random() < 0.7 else "idle"
                worker_states[worker_id] = state
            # Slow start - reduced productivity, more idle time
            elif is_slow_start:
                prev = worker_states[worker_id]
                if prev == "absent":
                    state = "idle" if random.random() < 0.6 else "working"
                else:
                    state = "idle" if random.random() < 0.5 else "working"
                worker_states[worker_id] = state
            # Normal operation - weighted state transitions
            else:
                prev = worker_states[worker_id]
                rand = random.random()
                if prev == "absent":
                    state = "working" if rand < 0.8 else "idle"
                else:
                    if rand < 0.65:
                        state = "working"
                    elif rand < 0.9:
                        state = "idle"
                    else:
                        state = "absent"
                worker_states[worker_id] = state

            station_id = worker_station_map[worker_id]

            events.append(
                schemas.AIEventCreate(
                    timestamp=ts,
                    worker_id=worker_id,
                    workstation_id=station_id,
                    event_type=state,
                    confidence=round(random.uniform(0.88, 0.99), 3),
                    count=1,
                )
            )

            # ELITE FEATURE 3: STRICT CORRELATION - product_count ONLY during 'working'
            # Never emit production during absent/idle (this was a red flag!)
            if state == "working" and not is_lunch_break:
                # Reduce production during slow start
                production_chance = 0.3 if is_slow_start else 0.6
                if random.random() < production_chance:
                    events.append(
                        schemas.AIEventCreate(
                            timestamp=ts,
                            worker_id=worker_id,
                            workstation_id=station_id,
                            event_type="product_count",
                            confidence=round(random.uniform(0.9, 0.99), 3),
                            count=random.randint(1, 2 if is_slow_start else 3),
                        )
                    )

    batch_result = ingest_batch(db, events)
    return {
        "events_created": batch_result.success_count,
        "duplicates": batch_result.duplicate_count,
        "errors": batch_result.error_count,
    }
