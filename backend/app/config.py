"""
Configuration Management using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Database
    database_url: str = "sqlite:///./productivity.db"
    
    # API
    api_title: str = "AI Worker Productivity Dashboard API"
    api_version: str = "2.0.0"
    api_rate_limit: int = 100
    
    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://frontend:3000",
        "http://localhost:80"
    ]
    
    # Security
    api_key: str = "dev-api-key-change-in-production"
    secret_key: str = "your-secret-key-change-in-production"
    
    # Environment
    environment: str = "development"
    log_level: str = "INFO"
    
    # Metrics
    min_confidence: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
