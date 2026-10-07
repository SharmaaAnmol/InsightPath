"""
backend/tests/test_health.py
----------------------------
Test suite for root and API v1 health check endpoints.
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_root_health_endpoint():
    """Verify GET /health returns 200, valid structure, and artifacts are verified."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "InsightPath API"
    assert data["version"] == "1.0.0"
    assert data["artifacts_verified"] is True
    assert "details" in data
    assert data["details"]["models"]["jds_model_loaded"] is True
    assert data["details"]["models"]["sds_model_loaded"] is True
    assert "host" in data["details"]
    assert "port" in data["details"]
    assert data["details"]["tables_count"] > 0


def test_v1_health_endpoint():
    """Verify GET /api/v1/health returns 200 and matches expected schema."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "InsightPath API"
    assert data["artifacts_verified"] is True
    assert data["details"]["tables_dir_exists"] is True
    assert "host" in data["details"]
    assert "port" in data["details"]
    assert data["details"]["tables_count"] > 0
