"""
backend/tests/test_data_api.py
------------------------------
Test suite for data endpoints serving validated CSV outputs
from Phases 3, 4, 7, and 8.
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_market_roles_endpoint():
    """Verify macro role demand endpoint returns populated records."""
    response = client.get("/api/v1/market/roles")
    assert response.status_code == 200
    data = response.json()
    assert data["row_count"] > 0
    assert len(data["records"]) > 0
    assert "role_standardized" in data["columns"] or "role" in data["columns"] or len(data["columns"]) >= 2


def test_market_skills_endpoint():
    """Verify micro skill demand endpoint returns populated records."""
    response = client.get("/api/v1/market/skills")
    assert response.status_code == 200
    data = response.json()
    assert data["row_count"] > 0
    assert len(data["records"]) > 0


def test_synthesis_market_skill_matrix_endpoint():
    """Verify Phase 7 Asymmetric Dual-Currency matrix endpoint returns records."""
    response = client.get("/api/v1/synthesis/market-skill-matrix")
    assert response.status_code == 200
    data = response.json()
    assert data["row_count"] > 0
    assert len(data["records"]) > 0


def test_synthesis_gap_analysis_endpoint():
    """Verify Phase 7 talent gap analysis endpoint returns the 5 systemic gaps."""
    response = client.get("/api/v1/synthesis/gap-analysis")
    assert response.status_code == 200
    data = response.json()
    assert data["row_count"] == 5
    assert len(data["records"]) == 5


def test_framework_quadrants_endpoint():
    """Verify Phase 8 Four-Quadrant talent matrix endpoint returns 4 quadrants."""
    response = client.get("/api/v1/framework/quadrants")
    assert response.status_code == 200
    data = response.json()
    assert data["row_count"] == 4
    assert len(data["records"]) == 4


def test_framework_student_blueprint_endpoint():
    """Verify student blueprint endpoint returns 4-year progression plan."""
    response = client.get("/api/v1/framework/blueprints/student")
    assert response.status_code == 200
    data = response.json()
    assert data["row_count"] > 0
    assert len(data["records"]) > 0
