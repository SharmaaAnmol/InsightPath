"""
backend/tests/test_assessment_api.py
------------------------------------
Unit tests for the Career-Readiness Assessment endpoint:
valid payloads, quadrant mapping, ethical language constraints, and validation errors.
"""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_assessment_evaluate_high_alignment():
    """Verify evaluation for high-performing dual-currency profile (Q1)."""
    payload = {
        "career_goal": "Machine Learning Engineer",
        "experience_level": "Junior (2-4 years)",
        "maths_stats_skills": 4.6,
        "coding_skills": 4.5,
        "ai_and_ml_skills": 4.8,
        "big_data_skills": 4.2,
        "dashboard_and_storytelling_skills": 4.5,
    }
    response = client.post("/api/v1/assessment/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()

    # Core response structure
    assert data["career_goal"] == "Machine Learning Engineer"
    assert data["experience_level"] == "Junior (2-4 years)"
    assert data["quadrant_assigned"] == "Q1"
    assert 0.0 <= data["model_probability"] <= 1.0
    assert "Observed-model signal" in data["model_signal"]

    # Radar data completeness
    assert len(data["radar_data"]) == 5
    skill_keys = [p["skill_key"] for p in data["radar_data"]]
    assert "maths_stats_skills" in skill_keys
    assert "dashboard_and_storytelling_skills" in skill_keys

    # Recommendations and learning sequence
    assert len(data["recommendations"]) == 5
    assert len(data["learning_sequence"]) == 3
    assert len(data["strengths"]) > 0

    # Strict Ethical Requirements
    disclaimer = data["methodology_disclaimer"]
    assert "METHODOLOGY & ETHICAL NOTICE" in disclaimer
    assert "not constitute a guarantee" in disclaimer.lower() or "does not provide any guarantee" in disclaimer.lower()

    # Disallowed deterministic language check
    full_text = str(data)
    assert "You will get a high salary" not in full_text
    assert "You are guaranteed to succeed" not in full_text
    assert "You are suitable for hiring" not in full_text


def test_assessment_evaluate_execution_specialist_q2():
    """Verify evaluation for technically strong candidate with storytelling gap (Q2)."""
    payload = {
        "career_goal": "Data Scientist",
        "experience_level": "Entry-Level (0-2 years)",
        "maths_stats_skills": 4.5,
        "coding_skills": 4.5,
        "ai_and_ml_skills": 4.2,
        "big_data_skills": 4.0,
        "dashboard_and_storytelling_skills": 2.2,  # Noticeable gap
    }
    response = client.post("/api/v1/assessment/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["quadrant_assigned"] == "Q2"
    assert "Pure Execution Specialist" in data["quadrant_title"]
    assert any("Dashboarding & Storytelling" in g for g in data["development_gaps"])
    assert "Dashboarding & Storytelling" in data["priority_skills"]


def test_assessment_evaluate_foundational_q4():
    """Verify evaluation for candidate with foundational development opportunities (Q4)."""
    payload = {
        "career_goal": "Data Analyst",
        "experience_level": "Entry-Level (0-2 years)",
        "maths_stats_skills": 2.2,
        "coding_skills": 2.5,
        "ai_and_ml_skills": 2.0,
        "big_data_skills": 2.2,
        "dashboard_and_storytelling_skills": 2.0,
    }
    response = client.post("/api/v1/assessment/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["quadrant_assigned"] == "Q4"
    assert "Foundational Development" in data["quadrant_title"]
    assert data["model_classification"] == "Developing Foundation Alignment"
    assert len(data["development_gaps"]) >= 3


def test_assessment_validation_bounds():
    """Verify input validation rejects scores outside [1.0, 5.0]."""
    invalid_payload = {
        "career_goal": "Data Scientist",
        "experience_level": "Entry-Level (0-2 years)",
        "maths_stats_skills": 5.5,  # Invalid: > 5.0
        "coding_skills": 4.0,
        "ai_and_ml_skills": 3.5,
        "big_data_skills": 3.0,
        "dashboard_and_storytelling_skills": 3.5,
    }
    response = client.post("/api/v1/assessment/evaluate", json=invalid_payload)
    assert response.status_code == 422
