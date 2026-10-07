"""
backend/tests/test_models_api.py
--------------------------------
Test suite for ML inference endpoints (JDS Skill & SDS Personality).
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_jds_predict_valid_payload():
    """Verify JDS model scoring with valid skill ratings [1.0 to 5.0]."""
    payload = {
        "big_data_skills": 4.0,
        "maths_stats_skills": 4.5,
        "coding_skills": 4.0,
        "ai_and_ml_skills": 3.5,
        "dashboard_and_storytelling_skills": 4.5,
    }
    response = client.post("/api/v1/models/jds/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] in [0, 1]
    assert data["prediction_label"] in ["High Salary Hike", "Low Salary Hike"]
    assert 0.0 <= data["probability_high"] <= 1.0
    assert 0.0 <= data["probability_low"] <= 1.0
    assert abs((data["probability_high"] + data["probability_low"]) - 1.0) < 0.01
    assert data["model_name"] == "Logistic_Regression_L2"
    assert "dashboard_and_storytelling_skills" in data["key_differentiators"]


def test_jds_predict_validation_error():
    """Verify input validation rejects skill scores outside [1.0, 5.0]."""
    payload = {
        "big_data_skills": 6.0,  # Invalid: > 5.0
        "maths_stats_skills": 4.5,
        "coding_skills": 4.0,
        "ai_and_ml_skills": 3.5,
        "dashboard_and_storytelling_skills": 4.5,
    }
    response = client.post("/api/v1/models/jds/predict", json=payload)
    assert response.status_code == 422


def test_sds_predict_valid_payload():
    """Verify SDS personality scoring and presence of mandatory ethical warning."""
    payload = {
        "neuroticism": 35.0,
        "extraversion": 42.0,
        "openness_to_experience": 52.0,
        "agreeableness": 45.0,
        "conscientiousness": 50.0,
    }
    response = client.post("/api/v1/models/sds/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] in [0, 1]
    assert data["prediction_label"] in ["High Success", "Low Success"]
    assert 0.0 <= data["probability_high"] <= 1.0
    assert 0.0 <= data["probability_low"] <= 1.0
    assert abs((data["probability_high"] + data["probability_low"]) - 1.0) < 0.01
    assert "ethical_safeguard_notice" in data
    assert "NEVER be used as automated hiring" in data["ethical_safeguard_notice"]
    assert "openness_to_experience" in data["dominant_drivers"]


def test_sds_predict_validation_error():
    """Verify input validation rejects personality scores outside [17.0, 68.0]."""
    payload = {
        "neuroticism": 10.0,  # Invalid: < 17.0
        "extraversion": 42.0,
        "openness_to_experience": 52.0,
        "agreeableness": 45.0,
        "conscientiousness": 50.0,
    }
    response = client.post("/api/v1/models/sds/predict", json=payload)
    assert response.status_code == 422


def test_models_status_endpoint():
    """Verify model status endpoint confirms champion models are loaded."""
    response = client.get("/api/v1/models/status")
    assert response.status_code == 200
    data = response.json()
    assert data["jds_model_loaded"] is True
    assert data["sds_model_loaded"] is True
