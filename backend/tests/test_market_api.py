"""
backend/tests/test_market_api.py
--------------------------------
Unit tests for Market Intelligence API endpoints:
overview, roles, companies, locations, skills, and premium skills.
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_market_overview_endpoint():
    """Verify GET /api/v1/market/overview returns macro metrics matching 17,443 postings."""
    response = client.get("/api/v1/market/overview")
    assert response.status_code == 200
    data = response.json()
    assert data["total_postings"] == 17443
    assert data["analytics_jobs_count"] == 15841
    assert data["datascience_jobs_count"] == 1602
    assert data["median_experience_years"] > 0
    assert data["median_salary_lakh"] > 0
    assert len(data["salary_breakdowns"]) > 0
    assert len(data["macro_descriptives"]) > 0


def test_market_roles_endpoint():
    """Verify GET /api/v1/market/roles returns standardized role demand distribution."""
    response = client.get("/api/v1/market/roles")
    assert response.status_code == 200
    data = response.json()
    assert data["table_name"] == "role_demand"
    assert data["row_count"] >= 10
    assert len(data["records"]) >= 10
    assert data["top_role_by_openings"] is not None
    # Check structure of records
    first_record = data["records"][0]
    assert "job_title" in first_record
    assert "total_openings" in first_record
    assert "demand_rank" in first_record


def test_market_companies_endpoint():
    """Verify GET /api/v1/market/companies returns employer vacancy rankings."""
    response = client.get("/api/v1/market/companies")
    assert response.status_code == 200
    data = response.json()
    assert data["table_name"] == "company_demand"
    assert data["row_count"] > 0
    assert len(data["records"]) > 0
    assert data["top_employer"] == "TCS"
    first_record = data["records"][0]
    assert "company_name" in first_record
    assert "postings_count" in first_record
    assert "total_openings" in first_record


def test_market_locations_endpoint():
    """Verify GET /api/v1/market/locations returns 7 geo-cluster breakdown."""
    response = client.get("/api/v1/market/locations")
    assert response.status_code == 200
    data = response.json()
    assert data["table_name"] == "location_summary"
    assert data["row_count"] == 7
    assert len(data["records"]) == 7
    assert data["highest_density_cluster"] == "Bengaluru"
    clusters = [r["location_cluster"] for r in data["records"]]
    assert "Bengaluru" in clusters
    assert "NCR" in clusters
    assert "Mumbai" in clusters


def test_market_skills_endpoint():
    """Verify GET /api/v1/market/skills returns frequency rankings across requisitions."""
    response = client.get("/api/v1/market/skills")
    assert response.status_code == 200
    data = response.json()
    assert data["table_name"] == "skill_frequency"
    assert data["row_count"] > 0
    assert len(data["records"]) > 0
    first_record = data["records"][0]
    assert "skill_name" in first_record
    assert "frequency_count" in first_record
    assert "prevalence_pct" in first_record


def test_market_premium_skills_endpoint():
    """Verify GET /api/v1/market/premium-skills returns relative prevalence ratios."""
    response = client.get("/api/v1/market/premium-skills")
    assert response.status_code == 200
    data = response.json()
    assert data["table_name"] == "skill_salary_comparison"
    assert data["row_count"] > 0
    assert len(data["records"]) > 0
    first_record = data["records"][0]
    assert "skill_name" in first_record
    assert "relative_prevalence_ratio" in first_record
    assert "premium_rank" in first_record
