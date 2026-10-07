"""
backend/schemas/health.py
-------------------------
Pydantic schemas for health checks and service monitoring.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(default="ok", description="Overall system health status")
    version: str = Field(default="1.0.0", description="API version")
    service: str = Field(default="insightpath-api", description="Service identifier")
    environment: str = Field(default="development", description="Runtime environment")
    artifacts_verified: bool = Field(default=True, description="Whether core ML/data artifacts exist")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Detailed subsystem statuses")
