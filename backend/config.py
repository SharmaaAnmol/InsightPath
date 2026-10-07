"""
backend/config.py
-----------------
Application configuration and path resolution for the InsightPath backend.
Locates the data science project root dynamically without hardcoded machine paths.
Supports flexible environment variables for cloud deployment (Render, Vercel, Docker).
"""

from pathlib import Path
from typing import List
import os
import json


def find_project_root() -> Path:
    """
    Locates the project root:
    1. Checks if PROJECT_ROOT environment variable is provided.
    2. Traverses upward from this file until we locate the directory
       containing 'data/processed' and 'outputs/tables'.
    3. Falls back to current working directory.
    """
    env_root = os.getenv("PROJECT_ROOT")
    if env_root and Path(env_root).exists():
        return Path(env_root).resolve()

    current = Path(__file__).resolve().parent
    for candidate in [current, *current.parents]:
        if (candidate / "data" / "processed").exists() and (candidate / "outputs").exists():
            return candidate

    return Path.cwd().resolve()


def parse_cors_origins() -> List[str]:
    """
    Parses CORS_ALLOWED_ORIGINS or CORS_ORIGINS from environment.
    Supports comma-separated strings, wildcard '*', or JSON arrays.
    """
    raw_origins = os.getenv("CORS_ALLOWED_ORIGINS") or os.getenv("CORS_ORIGINS")
    if not raw_origins:
        return [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ]

    raw_origins = raw_origins.strip()
    if raw_origins == "*":
        return ["*"]

    # Try JSON array parsing (e.g. '["https://insightpath.vercel.app"]')
    if raw_origins.startswith("[") and raw_origins.endswith("]"):
        try:
            parsed = json.loads(raw_origins)
            if isinstance(parsed, list):
                return [str(o).strip() for o in parsed if str(o).strip()]
        except Exception:
            pass

    # Comma-separated parsing
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "InsightPath API")
    VERSION: str = os.getenv("VERSION", "1.0.0")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Host & Port configuration for container / PaaS deployment
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))

    # Project Root & Path resolution
    PROJECT_ROOT: Path = find_project_root()

    # Artifact directory paths (overridable via env)
    MODELS_DIR: Path = Path(os.getenv("MODELS_DIR", PROJECT_ROOT / "outputs" / "models"))
    TABLES_DIR: Path = Path(os.getenv("TABLES_DIR", PROJECT_ROOT / "outputs" / "tables"))
    DATA_DIR: Path = Path(os.getenv("DATA_DIR", PROJECT_ROOT / "data"))

    # Specific champion model artifact paths
    JDS_MODEL_PATH: Path = Path(
        os.getenv(
            "JDS_MODEL_PATH",
            MODELS_DIR / "phase5" / "jds_champion_logistic_l2.joblib",
        )
    )
    JDS_METADATA_PATH: Path = Path(
        os.getenv(
            "JDS_METADATA_PATH",
            MODELS_DIR / "phase5" / "jds_champion_metadata.json",
        )
    )
    SDS_MODEL_PATH: Path = Path(
        os.getenv(
            "SDS_MODEL_PATH",
            MODELS_DIR / "phase6" / "sds_champion_logistic_l2.joblib",
        )
    )
    SDS_METADATA_PATH: Path = Path(
        os.getenv(
            "SDS_METADATA_PATH",
            MODELS_DIR / "phase6" / "sds_champion_metadata.json",
        )
    )

    # CORS configuration
    CORS_ORIGINS: List[str] = parse_cors_origins()


settings = Settings()
