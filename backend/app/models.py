"""
Database Models for AI-Powered Worker Productivity Dashboard

This module defines SQLAlchemy models for:
- Workers: Individual workers with metadata
- Workstations: Physical workstations in the factory
- AIEvents: Time-series events from AI-powered CCTV cameras

All events are append-only for audit trail and time-series analysis.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class Worker(Base):
    """
    Worker metadata table.
    
    Stores information about factory workers.
    Assumption: Workers have unique IDs (e.g., W1, W2, etc.)
    """
    __tablename__ = "workers"

    id = Column(String, primary_key=True)  # e.g., "W1", "W2"
    name = Column(String, nullable=False)
    shift = Column(String)  # e.g., "morning", "evening", "night"
    department = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to events
    events = relationship("AIEvent", back_populates="worker", cascade="all, delete-orphan")


class Workstation(Base):
    """
    Workstation metadata table.
    
    Stores information about physical workstations in the factory.
    Assumption: Workstations have unique IDs (e.g., S1, S2, etc.)
    """
    __tablename__ = "workstations"

    id = Column(String, primary_key=True)  # e.g., "S1", "S2"
    name = Column(String, nullable=False)
    location = Column(String)  # e.g., "Assembly Line 1", "Quality Check"
    type = Column(String)  # e.g., "assembly", "inspection", "packaging"
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to events
    events = relationship("AIEvent", back_populates="workstation", cascade="all, delete-orphan")


class AIEvent(Base):
    """
    AI-generated events from CCTV cameras.
    
    This is an append-only table storing all worker activity events.
    Events are timestamped and include confidence scores from AI models.
    
    Event Types:
    - 'working': Worker is actively working
    - 'idle': Worker is idle/not working
    - 'absent': Worker is not present at workstation
    - 'product_count': Product completion event
    
    Assumptions:
    - Events may arrive out of order (handled by timestamp indexing)
    - Duplicate events possible (handled by unique constraint)
    - AI confidence threshold should be >= 0.7 (validated at API level)
    """
    __tablename__ = "ai_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, index=True)  # Indexed for time-range queries
    worker_id = Column(String, ForeignKey("workers.id"), nullable=False, index=True)
    workstation_id = Column(String, ForeignKey("workstations.id"), nullable=False, index=True)
    event_type = Column(String, nullable=False, index=True)  # working, idle, absent, product_count - indexed for filtering
    confidence = Column(Float, nullable=False)  # AI model confidence (0.0 - 1.0)
    count = Column(Integer, default=1)  # Product count for product_count events
    created_at = Column(DateTime, default=datetime.utcnow)  # When record was inserted
    
    # Relationships
    worker = relationship("Worker", back_populates="events")
    workstation = relationship("Workstation", back_populates="events")
    
    # Composite index for efficient time-series queries
    __table_args__ = (
        Index('idx_worker_timestamp', 'worker_id', 'timestamp'),
        Index('idx_workstation_timestamp', 'workstation_id', 'timestamp'),
        # Prevent duplicates per worker + event type at same timestamp
        UniqueConstraint('timestamp', 'worker_id', 'event_type', name='uix_event_dedup_worker_type'),
    )
