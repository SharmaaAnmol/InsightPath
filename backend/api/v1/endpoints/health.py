"""
backend/api/v1/endpoints/health.py
----------------------------------
Health check endpoint for API v1.
"""

from fastapi import APIRouter
from backend.config import settings
from backend.schemas.health import HealthResponse
from backend.services.model_service import model_service

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def get_v1_health() -> HealthResponse:
    """
    Returns API health status, environment, and verification of core artifacts.
    """
    model_status = model_service.check_status()
    artifacts_ok = (
        model_status["jds_model_loaded"]
        and model_status["sds_model_loaded"]
        and settings.TABLES_DIR.exists()
    )

    tables_count = (
        len(list(settings.TABLES_DIR.glob("**/*.csv")))
        if settings.TABLES_DIR.exists()
        else 0
    )

    return HealthResponse(
        status="ok" if artifacts_ok else "degraded",
        version=settings.VERSION,
        service=settings.PROJECT_NAME,
        environment=settings.ENVIRONMENT,
        artifacts_verified=artifacts_ok,
        details={
            "models": model_status,
            "project_root": str(settings.PROJECT_ROOT),
            "tables_dir_exists": settings.TABLES_DIR.exists(),
            "tables_count": tables_count,
            "host": settings.HOST,
            "port": settings.PORT,
        },
    )
