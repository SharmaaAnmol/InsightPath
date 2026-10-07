"""
backend/main.py
---------------
Main FastAPI application entrypoint for the InsightPath / RUSTY WOLVES web platform.
Serves validated data science artifacts, machine learning inference, and health checks.
"""

from contextlib import asynccontextmanager
from typing import Dict, Any
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.schemas.health import HealthResponse
from backend.services.model_service import model_service
from backend.api.v1.router import api_v1_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("insightpath.api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup & shutdown lifecycle:
    Pre-loads and validates champion models and artifact availability.
    """
    logger.info("Initializing InsightPath API (v%s)...", settings.VERSION)
    logger.info("Project root resolved to: %s", settings.PROJECT_ROOT)
    try:
        model_service.load_artifacts()
        logger.info("Champion models loaded successfully.")
    except Exception as exc:
        logger.error("Error pre-loading models: %s", exc)
    yield
    logger.info("InsightPath API shutting down.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "Production API consuming validated Phase 0–9 data science outputs: "
        "JDS Skill Modeling, SDS Personality Modeling, Methodological Triangulation, "
        "and Career-Readiness Framework."
    ),
    lifespan=lifespan,
)

# CORS middleware for Next.js frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_security_headers(request, call_next):
    """Enforces standard HTTP security response headers."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


from fastapi.responses import JSONResponse


@app.exception_handler(FileNotFoundError)
async def file_not_found_exception_handler(request, exc: FileNotFoundError):
    """Handles missing analytical artifacts gracefully with a 404 response."""
    return JSONResponse(
        status_code=404,
        content={"detail": f"Analytical artifact not found: {str(exc)}"},
    )


# Mount API v1 router
app.include_router(api_v1_router, prefix=settings.API_V1_STR)


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def get_root_health() -> HealthResponse:
    """
    Root health check endpoint: GET /health.
    Verifies API availability and core ML artifact status.
    """
    model_status = model_service.check_status()
    artifacts_ok = (
        model_status["jds_model_loaded"]
        and model_status["sds_model_loaded"]
        and settings.TABLES_DIR.exists()
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
        },
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
