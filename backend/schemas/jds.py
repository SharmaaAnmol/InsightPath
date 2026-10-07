"""
backend/schemas/jds.py
----------------------
Pydantic schemas for Junior Data Scientist (JDS) skill scoring and prediction.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class JDSPredictRequest(BaseModel):
    big_data_skills: float = Field(..., ge=1.0, le=5.0, description="Big data skill rating (1.0 to 5.0)")
    maths_stats_skills: float = Field(..., ge=1.0, le=5.0, description="Maths & Statistics skill rating (1.0 to 5.0)")
    coding_skills: float = Field(..., ge=1.0, le=5.0, description="Coding skill rating (1.0 to 5.0)")
    ai_and_ml_skills: float = Field(..., ge=1.0, le=5.0, description="AI & Machine Learning skill rating (1.0 to 5.0)")
    dashboard_and_storytelling_skills: float = Field(
        ..., ge=1.0, le=5.0, description="Dashboarding & Storytelling skill rating (1.0 to 5.0)"
    )


class JDSPredictResponse(BaseModel):
    prediction: int = Field(..., description="Binary prediction: 1 (High Hike) or 0 (Low Hike)")
    prediction_label: str = Field(..., description="Human-readable outcome: 'High Salary Hike' or 'Low Salary Hike'")
    probability_high: float = Field(..., description="Predicted probability of High Salary Hike [0.0, 1.0]")
    probability_low: float = Field(..., description="Predicted probability of Low Salary Hike [0.0, 1.0]")
    model_name: str = Field(default="Logistic_Regression_L2", description="Champion model algorithm")
    model_roc_auc: float = Field(default=0.9035, description="Cross-validated ROC-AUC on held-out folds")
    key_differentiators: List[str] = Field(
        default=["dashboard_and_storytelling_skills", "maths_stats_skills"],
        description="Top empirical predictive drivers identified in Phase 5"
    )
    feature_contributions: Optional[Dict[str, float]] = Field(
        default=None, description="Standardized odds ratio or coefficient weights"
    )
