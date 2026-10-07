"""
backend/api/v1/router.py
------------------------
Master router for API version 1.
Aggregates health, models, market, synthesis, and framework routers.
"""

from fastapi import APIRouter
from backend.api.v1.endpoints import health, models, market, synthesis, framework

api_v1_router = APIRouter()

api_v1_router.include_router(health.router, tags=["Health"])
api_v1_router.include_router(models.router, prefix="/models", tags=["Models"])
api_v1_router.include_router(market.router, prefix="/market", tags=["Market Data"])
api_v1_router.include_router(synthesis.router, prefix="/synthesis", tags=["Synthesis"])
api_v1_router.include_router(framework.router, prefix="/framework", tags=["Framework"])
