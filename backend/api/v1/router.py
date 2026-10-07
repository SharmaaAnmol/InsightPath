"""
backend/api/v1/router.py
------------------------
Master router for API version 1.
Aggregates health, market, jds, sds, framework, models, and synthesis routers.
"""

from fastapi import APIRouter
from backend.api.v1.endpoints import health, market, jds, sds, framework, models, synthesis

api_v1_router = APIRouter()

api_v1_router.include_router(health.router, tags=["Health"])
api_v1_router.include_router(market.router, prefix="/market", tags=["Market Data"])
api_v1_router.include_router(jds.router, prefix="/jds", tags=["Junior Data Scientist (Phase 5)"])
api_v1_router.include_router(sds.router, prefix="/sds", tags=["Senior Data Scientist (Phase 6)"])
api_v1_router.include_router(framework.router, prefix="/framework", tags=["Career-Readiness Framework (Phase 8)"])
api_v1_router.include_router(models.router, prefix="/models", tags=["Models & Inference"])
api_v1_router.include_router(synthesis.router, prefix="/synthesis", tags=["Synthesis (Phase 7)"])
