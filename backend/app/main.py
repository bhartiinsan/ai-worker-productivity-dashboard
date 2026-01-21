"""
FastAPI Application - AI-Powered Worker Productivity Dashboard

Production-ready REST API for ingesting AI-generated CCTV events
and querying worker/workstation/factory-level productivity metrics.

Features:
- Rate limiting for API protection
- CORS security with configurable origins
- Comprehensive logging
- Health check endpoints
- Bitemporal event tracking
"""

from fastapi import FastAPI, HTTPException, Depends, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from datetime import datetime
import uvicorn
import logging

from . import models, schemas, crud
from .database import engine, get_db
from .seed_data import seed_database
from .services import events_service, metrics_service, seed_service
from .config import settings
from .middleware import limiter

try:
    from slowapi.errors import RateLimitExceeded  # type: ignore
except ImportError:
    # Fallback if slowapi not installed
    class RateLimitExceeded(Exception):  # type: ignore
        pass

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.api_title,
    description="Production-grade API for tracking worker productivity via AI-powered CCTV events",
    version=settings.api_version,
    docs_url="/docs" if settings.environment == "development" else None,
    redoc_url="/redoc" if settings.environment == "development" else None
)

# Rate limiting
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."}
    )

# CORS middleware - secure configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"],
    max_age=600,
)


# ========================================
# Health & Info Endpoints
# ========================================

@app.get("/")
@limiter.limit("60/minute")
async def read_root(request: Request):
    """API information endpoint."""
    client_ip = request.client.host if request.client else "unknown"
    logger.info(f"Root endpoint accessed from {client_ip}")
    return {
        "name": settings.api_title,
        "version": settings.api_version,
        "status": "operational",
        "environment": settings.environment,
        "documentation": "/docs" if settings.environment == "development" else "Contact admin"
    }


@app.get("/health")
@limiter.limit("120/minute")
async def health_check(request: Request, db: Session = Depends(get_db)):
    """Health check endpoint for monitoring and load balancers."""
    try:
        # Check database connectivity
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
        
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": datetime.utcnow(),
        "database": db_status,
        "environment": settings.environment
    }


# ========================================
# AI Event Ingestion Endpoints
# ========================================

@app.post("/api/events", response_model=schemas.AIEventResponse, status_code=201)
@limiter.limit("100/minute")
async def ingest_event(request: Request, event: schemas.AIEventCreate, db: Session = Depends(get_db)):
    """Ingest a single AI-generated event from CCTV system."""
    try:
        logger.info(f"Ingesting event: {event.worker_id}@{event.workstation_id} - {event.event_type}")
        result = events_service.ingest_event(db, event)
        if result["duplicate"]:
            logger.debug(f"Duplicate event detected: {event.worker_id}@{event.workstation_id}")
            return {"message": "Duplicate event ignored", "event": event.dict()}
        return result["event"]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Event ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/events/batch", response_model=schemas.AIEventBatchResponse)
@limiter.limit("20/minute")
async def ingest_events_batch(request: Request, batch: schemas.AIEventBatchCreate, db: Session = Depends(get_db)):
    """Batch ingest multiple AI events."""
    logger.info(f"Batch ingesting {len(batch.events)} events")
    result = events_service.ingest_batch(db, batch.events)
    logger.info(f"Batch complete: {result.success_count} success, {result.duplicate_count} duplicates, {result.error_count} errors")
    return result


@app.get("/api/events", response_model=List[schemas.AIEventResponse])
def get_events(
    worker_id: Optional[str] = Query(None),
    workstation_id: Optional[str] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    limit: int = Query(1000, ge=1, le=10000),
    db: Session = Depends(get_db)
):
    """Query AI events with optional filters."""
    return crud.get_events(db, worker_id, workstation_id, start_time, end_time, limit)


# ========================================
# Metrics Endpoints
# ========================================

@app.get("/api/metrics/workers", response_model=List[schemas.WorkerMetrics])
def get_worker_metrics(
    worker_id: Optional[str] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Get worker-level productivity metrics."""
    return metrics_service.worker_metrics(db, worker_id, start_time, end_time)


@app.get("/api/metrics/workstations", response_model=List[schemas.WorkstationMetrics])
def get_workstation_metrics(
    workstation_id: Optional[str] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Get workstation-level productivity metrics."""
    return metrics_service.workstation_metrics(db, workstation_id, start_time, end_time)


@app.get("/api/metrics/factory", response_model=schemas.FactoryMetrics)
def get_factory_metrics(
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Get factory-level aggregate metrics."""
    return metrics_service.factory_metrics(db, start_time, end_time)


@app.get("/api/metrics/model-health")
def get_model_health(db: Session = Depends(get_db)):
    """
    Monitor AI model health and detect potential model drift.
    
    Analyzes confidence scores from recent events to identify degradation.
    Returns status (Healthy/Warning) and recommendations.
    """
    return metrics_service.get_model_health_status(db)


@app.get("/api/metrics/efficiency-heatmap")
def get_efficiency_heatmap(db: Session = Depends(get_db)):
    """
    Get time-series heatmap showing productivity patterns by hour.
    
    Helps identify shift bottlenecks and peak productivity times.
    Returns hourly utilization data for the last 24 hours.
    """
    return metrics_service.get_efficiency_heatmap(db)


# ========================================
# Data Management Endpoints
# ========================================

@app.get("/api/workers", response_model=List[schemas.Worker])
def list_workers(db: Session = Depends(get_db)):
    """List all workers."""
    return crud.get_workers(db)


@app.get("/api/workstations", response_model=List[schemas.Workstation])
def list_workstations(db: Session = Depends(get_db)):
    """List all workstations."""
    return crud.get_workstations(db)


@app.post("/api/seed", response_model=schemas.SeedResponse)
def seed_data(
    clear_existing: bool = Query(False),
    hours_back: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """Seed or refresh database with sample data."""
    result = seed_database(db, clear_existing, hours_back)
    message = "Database refreshed successfully" if clear_existing else "Data seeded successfully"
    return schemas.SeedResponse(message=message, **result)


@app.post("/api/admin/seed", response_model=schemas.SeedResponse)
def admin_seed(
    clear_existing: bool = Query(False),
    db: Session = Depends(get_db),
):
    """Dynamic Faker-driven seeding for the last 24 hours with realistic constraints."""
    result = seed_service.admin_seed(db, clear_existing)
    return schemas.SeedResponse(
        message="Admin seed completed",
        workers_created=6,
        workstations_created=6,
        events_created=result["events_created"],
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
