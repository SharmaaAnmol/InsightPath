"""
backend/tests/test_sds_api.py
-----------------------------
Unit tests for Senior Data Scientist (SDS) API endpoints:
summary, model-performance, feature-importance, odds-ratios, and ethical notice enforcement.
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_sds_summary_endpoint():
    """Verify GET /api/v1/sds/summary returns primary cohort N=161 and unique subjects N=152."""
    response = client.get("/api/v1/sds/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["sample_size_n"] == 161
    assert data["unique_subjects_n"] == 152
    assert data["traits_evaluated"] == 5
    assert data["target_variable"] == "success_high_or_low"
    assert "ethical_safeguard_notice" in data
    assert "NEVER be used as automated hiring" in data["ethical_safeguard_notice"]
    assert len(data["records"]) > 0


def test_sds_model_performance_endpoint():
    """Verify GET /api/v1/sds/model-performance returns StratifiedGroupKFold metrics."""
    response = client.get("/api/v1/sds/model-performance")
    assert response.status_code == 200
    data = response.json()
    assert data["champion_model"] == "Logistic_Regression_L2"
    assert data["champion_roc_auc"] > 0.95
    assert "ethical_safeguard_notice" in data
    assert len(data["records"]) >= 6
    model_names = [r["model_name"] for r in data["records"]]
    assert "Logistic_Regression_L2" in model_names
    assert "Random_Forest" in model_names


def test_sds_feature_importance_endpoint():
    """Verify GET /api/v1/sds/feature-importance returns Openness as top driver."""
    response = client.get("/api/v1/sds/feature-importance")
    assert response.status_code == 200
    data = response.json()
    assert data["top_feature"] == "openness_to_experience"
    assert len(data["records"]) == 5
    assert "ethical_safeguard_notice" in data
    first_record = data["records"][0]
    assert "trait_dimension" in first_record
    assert "mean_permutation_importance" in first_record


def test_sds_odds_ratios_endpoint():
    """Verify GET /api/v1/sds/odds-ratios returns Conscientiousness & Openness with AOR > 7.0."""
    response = client.get("/api/v1/sds/odds-ratios")
    assert response.status_code == 200
    data = response.json()
    assert data["highest_odds_ratio_trait"] == "conscientiousness"
    assert data["highest_odds_ratio_value"] > 7.5
    assert len(data["records"]) == 5
    assert "ethical_safeguard_notice" in data
    first_record = data["records"][0]
    assert "adjusted_odds_ratio" in first_record
    assert "standardized_coef_beta" in first_record


def test_sds_group_tests_endpoint():
    """Verify GET /api/v1/sds/group-tests returns Big Five comparisons with ethical notice."""
    response = client.get("/api/v1/sds/group-tests")
    assert response.status_code == 200
    data = response.json()
    assert data["table_name"] == "sds_group_tests"
    assert data["cohort_high_success_n"] == 85
    assert data["cohort_low_success_n"] == 76
    assert "ethical_safeguard_notice" in data
    assert len(data["records"]) == 5
    # Confirm conscientiousness, openness, extraversion, agreeableness, neuroticism
    traits = [r["variable"] for r in data["records"]]
    assert "conscientiousness" in traits
    assert "openness_to_experience" in traits
    assert "neuroticism" in traits

