"""
backend/config.py
-----------------
Application configuration and path resolution for the InsightPath backend.
Locates the data science project root dynamically without hardcoded machine paths.
"""

from pathlib import Path
from typing import List
import os


def find_project_root() -> Path:
    """
    Traverse upward from this file until we locate the repository root
    containing 'data/processed' and 'outputs/models'.
    """
    current = Path(__file__).resolve().parent
    for candidate in [current, *current.parents]:
        if (candidate / "data" / "processed").exists() and (candidate / "outputs").exists():
            return candidate
    # Fallback to current working directory
    return Path.cwd().resolve()


class Settings:
    PROJECT_NAME: str = "InsightPath API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PROJECT_ROOT: Path = find_project_root()
    
    # Artifact directory paths
    MODELS_DIR: Path = PROJECT_ROOT / "outputs" / "models"
    TABLES_DIR: Path = PROJECT_ROOT / "outputs" / "tables"
    DATA_DIR: Path = PROJECT_ROOT / "data"
    
    # Specific model artifact paths
    JDS_MODEL_PATH: Path = MODELS_DIR / "phase5" / "jds_champion_logistic_l2.joblib"
    JDS_METADATA_PATH: Path = MODELS_DIR / "phase5" / "jds_champion_metadata.json"
    SDS_MODEL_PATH: Path = MODELS_DIR / "phase6" / "sds_champion_logistic_l2.joblib"
    SDS_METADATA_PATH: Path = MODELS_DIR / "phase6" / "sds_champion_metadata.json"
    
    # CORS configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]


settings = Settings()
