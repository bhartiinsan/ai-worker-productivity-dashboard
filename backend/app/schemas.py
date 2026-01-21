"""
Pydantic Schemas for API Request/Response Validation

Defines data validation models for:
- AI Event ingestion
- Worker and Workstation metadata
- Metrics responses
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal
from datetime import datetime


# ========================================
# AI Event Schemas
# ========================================

class AIEventCreate(BaseModel):
    """Schema for creating a new AI event from CCTV system."""
    timestamp: datetime = Field(..., description="Event timestamp in ISO format")
    worker_id: str = Field(..., pattern="^W[0-9]+$", description="Worker ID (e.g., W1, W2)")
    workstation_id: str = Field(..., pattern="^S[0-9]+$", description="Workstation ID (e.g., S1, S2)")
    event_type: Literal["working", "idle", "absent", "product_count"] = Field(..., description="Type of event")
    confidence: float = Field(..., ge=0.0, le=1.0, description="AI model confidence score")
    count: int = Field(default=1, ge=0, description="Count for product_count events")
    
    @field_validator('confidence')
    @classmethod
    def validate_confidence(cls, v):
        """Ensure confidence meets minimum threshold."""
        if v < 0.7:
            raise ValueError('Confidence must be >= 0.7 for event acceptance')
        return v


class AIEventResponse(BaseModel):
    """Schema for AI event responses."""
    id: int
    timestamp: datetime
    worker_id: str
    workstation_id: str
    event_type: str
    confidence: float
    count: int
    created_at: datetime

    class Config:
        from_attributes = True


class AIEventBatchCreate(BaseModel):
    """Schema for batch event ingestion."""
    events: List[AIEventCreate] = Field(..., description="List of events to ingest")


class AIEventBatchResponse(BaseModel):
    """Response for batch event ingestion."""
    success_count: int
    duplicate_count: int
    error_count: int
    errors: List[str] = []


# ========================================
# Worker Schemas
# ========================================

class WorkerBase(BaseModel):
    """Base worker schema."""
    id: str = Field(..., pattern="^W[0-9]+$")
    name: str
    shift: Optional[str] = None
    department: Optional[str] = None


class WorkerCreate(WorkerBase):
    """Schema for creating a worker."""
    pass


class Worker(WorkerBase):
    """Full worker response schema."""
    created_at: datetime

    class Config:
        from_attributes = True


# ========================================
# Workstation Schemas
# ========================================

class WorkstationBase(BaseModel):
    """Base workstation schema."""
    id: str = Field(..., pattern="^S[0-9]+$")
    name: str
    location: Optional[str] = None
    type: Optional[str] = None


class WorkstationCreate(WorkstationBase):
    """Schema for creating a workstation."""
    pass


class Workstation(WorkstationBase):
    """Full workstation response schema."""
    created_at: datetime

    class Config:
        from_attributes = True


# ========================================
# Metrics Schemas
# ========================================

class WorkerMetrics(BaseModel):
    """Worker-level productivity metrics."""
    worker_id: str
    worker_name: str
    total_active_time_hours: float = Field(..., description="Total time in 'working' state (hours)")
    total_idle_time_hours: float = Field(..., description="Total time in 'idle' state (hours)")
    utilization_percentage: float = Field(..., description="Active time / (Active + Idle) * 100")
    total_units_produced: int = Field(..., description="Sum of product_count events")
    units_per_hour: float = Field(..., description="Production rate (units/hour)")
    last_seen: Optional[datetime] = Field(None, description="Last event timestamp")


class WorkstationMetrics(BaseModel):
    """Workstation-level productivity metrics."""
    workstation_id: str
    workstation_name: str
    occupancy_time_hours: float = Field(..., description="Total time with worker present (hours)")
    utilization_percentage: float = Field(..., description="Productive time / Occupancy time * 100")
    total_units_produced: int = Field(..., description="Sum of product_count events")
    throughput_rate: float = Field(..., description="Production rate (units/hour)")
    last_activity: Optional[datetime] = Field(None, description="Last event timestamp")


class FactoryMetrics(BaseModel):
    """Factory-level aggregate metrics."""
    total_productive_time_hours: float = Field(..., description="Sum of all worker productive time")
    total_production_count: int = Field(..., description="Sum of all product_count events")
    average_utilization_percentage: float = Field(..., description="Average worker utilization")
    average_production_rate: float = Field(..., description="Average units per hour across workers")
    active_workers: int = Field(..., description="Number of workers with recent activity")
    active_workstations: int = Field(..., description="Number of workstations with recent activity")
    time_range_start: Optional[datetime] = None
    time_range_end: Optional[datetime] = None


class SeedResponse(BaseModel):
    """Response for seed data operation."""
    message: str
    workers_created: int
    workstations_created: int
    events_created: int
