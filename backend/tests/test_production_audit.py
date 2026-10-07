"""
backend/tests/test_production_audit.py
--------------------------------------
Comprehensive production-readiness verification tests for InsightPath backend:
1. Security headers & CORS validation
2. Model reproducibility, feature ordering, and preservation of preprocessing
3. Request boundary validation (1.0 to 5.0 constraints)
4. Graceful handling of missing artifacts (404 instead of unhandled 500)
5. Zero leakage: no identifier inputs into machine learning pipelines
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.services.model_service import model_service, JDS_FEATURES, SDS_FEATURES
from backend.config import settings

client = TestClient(app)


def test_security_headers_present_on_all_responses():
    """Verifies standard enterprise security headers on responses."""
    response = client.get("/health")
    assert response.status_code == 200
    headers = response.headers
    assert headers.get("X-Content-Type-Options") == "nosniff"
    assert headers.get("X-Frame-Options") == "DENY"
    assert headers.get("X-XSS-Protection") == "1; mode=block"
    assert headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"


def test_cors_headers_on_cross_origin_requests():
    """Verifies CORS headers respond appropriately for frontend origins."""
    response = client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    # Status can be 200 on successful preflight
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers


def test_jds_champion_model_integrity_and_feature_order():
    """Verifies that the serialized JDS champion model maintains exact feature order and steps."""
    model_service.load_artifacts()
    jds_model = model_service._jds_model
    assert jds_model is not None, "JDS champion model must be loaded"

    # Verify pipeline encapsulation
    assert hasattr(jds_model, "named_steps"), "JDS model must be an encapsulated Pipeline"
    assert "scaler" in jds_model.named_steps, "Pipeline must contain 'scaler' step"
    assert "clf" in jds_model.named_steps, "Pipeline must contain 'clf' step"

    # Verify exact feature order
    expected_order = [
        "big_data_skills",
        "maths_stats_skills",
        "coding_skills",
        "ai_and_ml_skills",
        "dashboard_and_storytelling_skills",
    ]
    assert JDS_FEATURES == expected_order

    # Verify known test input inference
    from backend.schemas.jds import JDSPredictRequest

    # High mastery input
    high_req = JDSPredictRequest(
        maths_stats_skills=4.8,
        coding_skills=4.7,
        ai_and_ml_skills=4.8,
        big_data_skills=4.5,
        dashboard_and_storytelling_skills=4.6,
    )
    high_resp = model_service.predict_jds(high_req)
    assert high_resp.prediction == 1
    assert high_resp.probability_high > 0.5
    assert high_resp.model_name == "Logistic_Regression_L2"
    assert high_resp.model_roc_auc >= 0.90

    # Low mastery input
    low_req = JDSPredictRequest(
        maths_stats_skills=2.0,
        coding_skills=2.0,
        ai_and_ml_skills=2.0,
        big_data_skills=2.0,
        dashboard_and_storytelling_skills=2.0,
    )
    low_resp = model_service.predict_jds(low_req)
    assert low_resp.prediction == 0
    assert low_resp.probability_low > 0.5


def test_assessment_request_validation_boundary_enforcement():
    """Verifies that invalid scores (<1.0 or >5.0) are rejected with 422."""
    # Test score above 5.0
    invalid_high = {
        "career_goal": "Data Scientist",
        "experience_level": "Junior (2-4 years)",
        "maths_stats_skills": 6.0,  # Invalid: > 5.0
        "coding_skills": 4.0,
        "ai_and_ml_skills": 4.0,
        "big_data_skills": 4.0,
        "dashboard_and_storytelling_skills": 4.0,
    }
    resp = client.post("/api/v1/assessment/evaluate", json=invalid_high)
    assert resp.status_code == 422

    # Test score below 1.0
    invalid_low = {
        "career_goal": "Data Scientist",
        "experience_level": "Junior (2-4 years)",
        "maths_stats_skills": 0.5,  # Invalid: < 1.0
        "coding_skills": 4.0,
        "ai_and_ml_skills": 4.0,
        "big_data_skills": 4.0,
        "dashboard_and_storytelling_skills": 4.0,
    }
    resp = client.post("/api/v1/assessment/evaluate", json=invalid_low)
    assert resp.status_code == 422


def test_zero_leakage_and_identifier_isolation():
    """Verifies that the API design prevents using identifiers as prediction inputs."""
    from backend.schemas.assessment import AssessmentRequest

    fields = AssessmentRequest.model_fields.keys()
    assert "user_id" not in fields, "Identifier 'user_id' must not be in model input"
    assert "id" not in fields, "Identifier 'id' must not be in model input"
    assert "email" not in fields, "Identifier 'email' must not be in model input"
    assert "name" not in fields, "Identifier 'name' must not be in model input"


def test_missing_artifact_graceful_handling():
    """Verifies that requesting an invalid table returns 404 rather than unhandled 500."""
    response = client.get("/api/v1/models/nonexistent_table")
    assert response.status_code == 404
