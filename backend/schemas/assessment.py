"""
backend/schemas/assessment.py
-----------------------------
Pydantic schemas for the Interactive Career-Readiness Assessment.
Enforces strict ethical constraints: non-deterministic, observed-cohort diagnostic language.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


ETHICAL_ASSESSMENT_DISCLAIMER = (
    "METHODOLOGY & ETHICAL NOTICE: This development profile is derived from the empirical patterns "
    "observed in the N=139 Junior Data Scientist cohort of the SAS CU Hackathon research dataset. "
    "All outputs represent observed-model signals and evidence-supported development priorities. "
    "This assessment does NOT constitute a guarantee of salary, compensation, promotion, hiring eligibility, "
    "or deterministic career success. It is strictly an educational self-reflection and coaching diagnostic."
)


class AssessmentRequest(BaseModel):
    career_goal: str = Field(
        default="Data Scientist",
        description="Target professional role (e.g., Data Scientist, ML Engineer, Analytics Consultant)",
    )
    experience_level: str = Field(
        default="Entry-Level (0-2 years)",
        description="Current experience bracket",
    )
    maths_stats_skills: float = Field(
        ..., ge=1.0, le=5.0, description="Mathematics & Statistics rating (1.0 to 5.0)"
    )
    coding_skills: float = Field(
        ..., ge=1.0, le=5.0, description="Coding (Python/R) rating (1.0 to 5.0)"
    )
    ai_and_ml_skills: float = Field(
        ..., ge=1.0, le=5.0, description="AI & Machine Learning rating (1.0 to 5.0)"
    )
    big_data_skills: float = Field(
        ..., ge=1.0, le=5.0, description="Big Data & Cloud rating (1.0 to 5.0)"
    )
    dashboard_and_storytelling_skills: float = Field(
        ..., ge=1.0, le=5.0, description="Dashboarding & Storytelling rating (1.0 to 5.0)"
    )


class SkillRadarPoint(BaseModel):
    skill_key: str
    skill_name: str
    user_score: float
    cohort_benchmark: float
    importance_rank: int


class RecommendationItem(BaseModel):
    skill_name: str
    priority_level: str  # "Immediate Priority" | "Secondary Focus" | "Maintain Strength"
    current_score: float
    target_benchmark: float
    gap_delta: float
    evidence_rationale: str
    roi_multiplier: str


class LearningStage(BaseModel):
    step: int
    title: str
    timeline: str
    milestone: str
    empirical_justification: str


class AssessmentResponse(BaseModel):
    career_goal: str
    experience_level: str
    career_readiness_summary: str
    model_signal: str
    model_probability: float = Field(..., description="Observed-cohort probability [0.0, 1.0]")
    model_classification: str
    quadrant_assigned: str
    quadrant_title: str
    radar_data: List[SkillRadarPoint]
    priority_skills: List[str]
    strengths: List[str]
    development_gaps: List[str]
    recommendations: List[RecommendationItem]
    learning_sequence: List[LearningStage]
    methodology_disclaimer: str = Field(default=ETHICAL_ASSESSMENT_DISCLAIMER)
