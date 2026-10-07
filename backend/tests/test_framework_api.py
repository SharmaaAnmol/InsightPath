"""
backend/tests/test_framework_api.py
-----------------------------------
Unit tests for Career-Readiness Framework API endpoints:
talent-matrix, career-stages, competencies, and stakeholders.
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_framework_talent_matrix_endpoint():
    """Verify GET /api/v1/framework/talent-matrix returns 4 readiness quadrants Q1 to Q4."""
    response = client.get("/api/v1/framework/talent-matrix")
    assert response.status_code == 200
    data = response.json()
    assert data["table_name"] == "four_quadrant_matrix"
    assert data["row_count"] == 4
    assert len(data["records"]) == 4
    assert data["quadrants"] == ["Q1", "Q2", "Q3", "Q4"]
    quadrant_ids = [r["quadrant_id"] for r in data["records"]]
    assert "Q1" in quadrant_ids
    assert "Q2" in quadrant_ids
    assert "Q3" in quadrant_ids
    assert "Q4" in quadrant_ids


def test_framework_career_stages_endpoint():
    """Verify GET /api/v1/framework/career-stages returns 4 progression tiers."""
    response = client.get("/api/v1/framework/career-stages")
    assert response.status_code == 200
    data = response.json()
    assert data["table_name"] == "career_stage_framework"
    assert data["row_count"] == 4
    assert len(data["records"]) == 4
    first_record = data["records"][0]
    assert "stage_id" in first_record
    assert "stage_name" in first_record
    assert "priority_competencies" in first_record
    assert "measurable_success_indicator" in first_record


def test_framework_competencies_endpoint():
    """Verify GET /api/v1/framework/competencies returns priority tiers and ROI multipliers."""
    response = client.get("/api/v1/framework/competencies")
    assert response.status_code == 200
    data = response.json()
    assert data["table_name"] == "competency_priorities"
    assert data["row_count"] > 0
    assert len(data["records"]) > 0
    first_record = data["records"][0]
    assert "competency" in first_record
    assert "priority_tier" in first_record
    assert "roi_multiplier" in first_record


def test_framework_stakeholders_endpoint():
    """Verify GET /api/v1/framework/stakeholders returns action blueprints and recommendations."""
    response = client.get("/api/v1/framework/stakeholders")
    assert response.status_code == 200
    data = response.json()
    assert data["table_name"] == "stakeholder_blueprints"
    assert data["row_count"] > 0
    assert len(data["records"]) > 0
    assert "student" in data["blueprints_available"]
    assert "university" in data["blueprints_available"]
    assert "mentor" in data["blueprints_available"]
    assert "employer" in data["blueprints_available"]
