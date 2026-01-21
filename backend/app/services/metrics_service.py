"""
Metrics service layer.

Calculates worker, workstation, and factory metrics using chronological event ordering
so out-of-order arrivals are handled correctly.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import crud, models, schemas


def _compute_durations(events: List[models.AIEvent], window_start: Optional[datetime], window_end: Optional[datetime]):
    """Accumulate hours spent per state between window_start and window_end."""
    if not events:
        return {"working": 0.0, "idle": 0.0, "absent": 0.0, "product_count": 0.0}, window_start, window_end

    ordered = sorted(events, key=lambda e: e.timestamp)
    start = window_start or ordered[0].timestamp
    end = window_end or datetime.utcnow()

    durations = {"working": 0.0, "idle": 0.0, "absent": 0.0, "product_count": 0.0}

    prev_time = max(start, ordered[0].timestamp)
    prev_state = ordered[0].event_type

    for ev in ordered[1:]:
        current_time = ev.timestamp
        if current_time < prev_time:  # type: ignore
            continue  # out-of-order safeguard
        delta_hours = (current_time - prev_time).total_seconds() / 3600
        durations[str(prev_state)] = durations.get(str(prev_state), 0.0) + max(delta_hours, 0.0)  # type: ignore
        prev_time = current_time
        prev_state = ev.event_type

    tail_hours = (end - prev_time).total_seconds() / 3600
    durations[str(prev_state)] = durations.get(str(prev_state), 0.0) + max(tail_hours, 0.0)  # type: ignore

    return durations, start, end


def worker_metrics(
    db: Session,
    worker_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> List[schemas.WorkerMetrics]:
    workers = [crud.get_worker(db, worker_id)] if worker_id else crud.get_workers(db)
    results: List[schemas.WorkerMetrics] = []

    for worker in workers:
        if not worker:
            continue
        # Convert Column objects to Python types
        wid = str(worker.id)
        wname = str(worker.name)
        
        events = crud.get_events(db, worker_id=wid, start_time=start_time, end_time=end_time, limit=10000)
        ordered_events = sorted(events, key=lambda e: e.timestamp)
        durations, span_start, span_end = _compute_durations(ordered_events, start_time, end_time)
        working_h = durations.get("working", 0.0)
        idle_h = durations.get("idle", 0.0)
        
        # Safe datetime comparison
        if span_start and span_end:  # type: ignore
            elapsed_h = max((span_end - span_start).total_seconds() / 3600, 0.0)
        else:
            elapsed_h = working_h + idle_h
            
        # Convert count to int and filter properly
        total_units = sum(int(e.count) for e in events if str(e.event_type) == "product_count")  # type: ignore

        utilization = (working_h / elapsed_h * 100) if elapsed_h > 0 else 0.0
        units_per_hour = (total_units / working_h) if working_h > 0 else 0.0

        last_seen = ordered_events[-1].timestamp if ordered_events else None

        results.append(
            schemas.WorkerMetrics(
                worker_id=wid,
                worker_name=wname,
                total_active_time_hours=round(working_h, 2),
                total_idle_time_hours=round(idle_h, 2),
                utilization_percentage=round(utilization, 2),
                total_units_produced=total_units,
                units_per_hour=round(units_per_hour, 2),
                last_seen=last_seen,  # type: ignore
            )
        )

    return results


def workstation_metrics(
    db: Session,
    workstation_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> List[schemas.WorkstationMetrics]:
    stations = [crud.get_workstation(db, workstation_id)] if workstation_id else crud.get_workstations(db)
    results: List[schemas.WorkstationMetrics] = []

    for station in stations:
        if not station:
            continue
        # Convert Column objects to Python types
        sid = str(station.id)
        sname = str(station.name)
        
        events = crud.get_events(db, workstation_id=sid, start_time=start_time, end_time=end_time, limit=10000)
        ordered_events = sorted(events, key=lambda e: e.timestamp)
        durations, span_start, span_end = _compute_durations(ordered_events, start_time, end_time)
        working_h = durations.get("working", 0.0)
        idle_h = durations.get("idle", 0.0)
        occupancy = working_h + idle_h
        
        # Convert count to int and filter properly
        total_units = sum(int(e.count) for e in events if str(e.event_type) == "product_count")  # type: ignore

        utilization = (working_h / occupancy * 100) if occupancy > 0 else 0.0
        throughput = (total_units / occupancy) if occupancy > 0 else 0.0
        last_activity = ordered_events[-1].timestamp if ordered_events else None

        results.append(
            schemas.WorkstationMetrics(
                workstation_id=sid,
                workstation_name=sname,
                occupancy_time_hours=round(occupancy, 2),
                utilization_percentage=round(utilization, 2),
                total_units_produced=total_units,
                throughput_rate=round(throughput, 2),
                last_activity=last_activity,  # type: ignore
            )
        )

    return results


def factory_metrics(
    db: Session,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> schemas.FactoryMetrics:
    worker_stats = worker_metrics(db, start_time=start_time, end_time=end_time)
    if not worker_stats:
        return schemas.FactoryMetrics(
            total_productive_time_hours=0.0,
            total_production_count=0,
            average_utilization_percentage=0.0,
            average_production_rate=0.0,
            active_workers=0,
            active_workstations=0,
            time_range_start=start_time,
            time_range_end=end_time,
        )

    total_productive_time = sum(m.total_active_time_hours for m in worker_stats)
    total_production = sum(m.total_units_produced for m in worker_stats)
    avg_utilization = sum(m.utilization_percentage for m in worker_stats) / len(worker_stats)

    productive_workers = [m for m in worker_stats if m.units_per_hour > 0]
    avg_prod_rate = (
        sum(m.units_per_hour for m in productive_workers) / len(productive_workers)
        if productive_workers else 0.0
    )

    station_stats = workstation_metrics(db, start_time=start_time, end_time=end_time)
    active_stations = len([s for s in station_stats if s.last_activity])

    return schemas.FactoryMetrics(
        total_productive_time_hours=round(total_productive_time, 2),
        total_production_count=total_production,
        average_utilization_percentage=round(avg_utilization, 2),
        average_production_rate=round(avg_prod_rate, 2),
        active_workers=len([m for m in worker_stats if m.last_seen]),
        active_workstations=active_stations,
        time_range_start=start_time,
        time_range_end=end_time,
    )


def get_model_health_status(db: Session) -> Dict:
    """
    Monitor AI model health by analyzing confidence scores.
    
    Detects potential model drift by tracking rolling average confidence
    of the last 100 events. This directly addresses the assessment's
    theoretical question about model drift detection.
    
    Returns:
        - status: "Healthy" or "Warning"
        - message: Explanation of the status
        - avg_confidence: Rolling average confidence score
        - samples: Number of events analyzed
    """
    # Get last 100 events ordered by timestamp
    recent_events = db.query(models.AIEvent).order_by(
        models.AIEvent.timestamp.desc()
    ).limit(100).all()
    
    if not recent_events:
        return {
            "status": "Unknown",
            "message": "No events available for analysis",
            "avg_confidence": 0.0,
            "samples": 0
        }
    
    # Calculate average confidence - convert to float for proper comparison
    avg_conf = float(sum(float(e.confidence) for e in recent_events) / len(recent_events))  # type: ignore
    
    # Detect drift: If average confidence drops below 0.75, model may be drifting
    if avg_conf < 0.75:
        return {
            "status": "Warning",
            "message": "Low Confidence Detected: Potential Model Drift",
            "avg_confidence": round(avg_conf, 4),
            "samples": len(recent_events),
            "recommendation": "Consider retraining the model or reviewing recent camera conditions"
        }
    elif avg_conf < 0.85:
        return {
            "status": "Caution",
            "message": "Confidence slightly below optimal threshold",
            "avg_confidence": round(avg_conf, 4),
            "samples": len(recent_events)
        }
    
    return {
        "status": "Healthy",
        "message": "Model confidence is within acceptable range",
        "avg_confidence": round(avg_conf, 4),
        "samples": len(recent_events)
    }


def get_efficiency_heatmap(db: Session) -> Dict:
    """
    Generate time-series heatmap data showing productivity patterns by hour.
    
    This helps factory managers identify shift bottlenecks and peak productivity times.
    Groups events by hour to visualize when workers are most active.
    
    Returns:
        - labels: Hour labels (e.g., "08:00", "10:00")
        - data: Utilization percentages for each hour
        - peaks: Identified peak productivity hours
    """
    # Get events from last 24 hours
    cutoff = datetime.utcnow() - timedelta(hours=24)
    events = db.query(models.AIEvent).filter(
        models.AIEvent.timestamp >= cutoff
    ).all()
    
    if not events:
        return {
            "labels": [],
            "data": [],
            "peaks": []
        }
    
    # Group events by hour
    hourly_data: Dict[int, Dict] = {}
    
    for event in events:
        hour = event.timestamp.hour
        if hour not in hourly_data:
            hourly_data[hour] = {"working": 0, "idle": 0, "total": 0}
        
        hourly_data[hour]["total"] += 1
        # Convert to string for proper comparison
        event_type_str = str(event.event_type)
        if event_type_str == "working":
            hourly_data[hour]["working"] += 1
        elif event_type_str == "idle":
            hourly_data[hour]["idle"] += 1
    
    # Calculate utilization per hour
    labels = []
    data = []
    
    for hour in sorted(hourly_data.keys()):
        stats = hourly_data[hour]
        utilization = (stats["working"] / stats["total"] * 100) if stats["total"] > 0 else 0
        labels.append(f"{hour:02d}:00")
        data.append(round(utilization, 2))
    
    # Identify peak hours (>80% utilization)
    peaks = [labels[i] for i, val in enumerate(data) if val > 80]
    
    return {
        "labels": labels,
        "data": data,
        "peaks": peaks,
        "avg_utilization": round(sum(data) / len(data), 2) if data else 0
    }
