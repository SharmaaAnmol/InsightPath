"""
backend/tests/test_jds_api.py
-----------------------------
Unit tests for Junior Data Scientist (JDS) API endpoints:
summary, model-performance, feature-importance, and odds-ratios.
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_jds_summary_endpoint():
    """Verify GET /api/v1/jds/summary returns primary cohort N=139 and 5 features."""
    response = client.get("/api/v1/jds/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["sample_size_n"] == 139
    assert data["features_count"] == 5
    assert data["target_variable"] == "salary_hike_high_or_low"
    assert len(data["records"]) > 0


def test_jds_model_performance_endpoint():
    """Verify GET /api/v1/jds/model-performance returns Logistic L2 as champion."""
    response = client.get("/api/v1/jds/model-performance")
    assert response.status_code == 200
    data = response.json()
    assert data["champion_model"] == "Logistic_Regression_L2"
    assert data["champion_roc_auc"] > 0.88
    assert len(data["records"]) >= 6
    # Ensure champion is evaluated across models
    model_names = [r["model_name"] for r in data["records"]]
    assert "Logistic_Regression_L2" in model_names
    assert "Random_Forest" in model_names


def test_jds_feature_importance_endpoint():
    """Verify GET /api/v1/jds/feature-importance returns permutation ranks."""
    response = client.get("/api/v1/jds/feature-importance")
    assert response.status_code == 200
    data = response.json()
    assert data["top_feature"] == "dashboard_and_storytelling_skills"
    assert len(data["records"]) == 5
    first_record = data["records"][0]
    assert "mean_permutation_importance" in first_record
    assert "importance_rank" in first_record


def test_jds_odds_ratios_endpoint():
    """Verify GET /api/v1/jds/odds-ratios returns odds ratios and beta coefficients."""
    response = client.get("/api/v1/jds/odds-ratios")
    assert response.status_code == 200
    data = response.json()
    assert data["highest_odds_ratio_feature"] == "maths_stats_skills"
    assert data["highest_odds_ratio_value"] > 3.0
    assert len(data["records"]) == 5
    first_record = data["records"][0]
    assert "odds_ratio" in first_record
    assert "standardized_coef_beta" in first_record


def test_jds_reduced_features_endpoint():
    """Verify GET /api/v1/jds/reduced-features returns 2-feature parsimony model."""
    response = client.get("/api/v1/jds/reduced-features")
    assert response.status_code == 200
    data = response.json()
    assert data["table_name"] == "full_vs_reduced_features"
    assert "maths_stats_skills" in data["top_2_features"]
    assert "dashboard_and_storytelling_skills" in data["top_2_features"]
    assert data["pct_auc_retained"] > 95.0
    assert len(data["records"]) > 0

