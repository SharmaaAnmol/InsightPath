"""
backend/schemas/sds.py
----------------------
Pydantic schemas for Senior Data Scientist (SDS) personality scoring and prediction.
Strictly incorporates Phase 6 ethical guardrails: personality traits serve exclusively
as self-reflection, coaching, and mentoring diagnostics, NEVER as hiring/termination gates.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class SDSPredictRequest(BaseModel):
    neuroticism: float = Field(..., ge=17.0, le=68.0, description="Neuroticism score (17.0 to 68.0)")
    extraversion: float = Field(..., ge=17.0, le=68.0, description="Extraversion score (17.0 to 68.0)")
    openness_to_experience: float = Field(..., ge=17.0, le=68.0, description="Openness to Experience score (17.0 to 68.0)")
    agreeableness: float = Field(..., ge=17.0, le=68.0, description="Agreeableness score (17.0 to 68.0)")
    conscientiousness: float = Field(..., ge=17.0, le=68.0, description="Conscientiousness score (17.0 to 68.0)")


class SDSPredictResponse(BaseModel):
    prediction: int = Field(..., description="Binary prediction: 1 (High Success) or 0 (Low Success)")
    prediction_label: str = Field(..., description="Human-readable outcome: 'High Success' or 'Low Success'")
    probability_high: float = Field(..., description="Predicted probability of High Consulting Success [0.0, 1.0]")
    probability_low: float = Field(..., description="Predicted probability of Low Consulting Success [0.0, 1.0]")
    model_name: str = Field(default="Logistic_Regression_L2", description="Champion model algorithm")
    model_roc_auc: float = Field(default=0.9699, description="Group-aware cross-validated ROC-AUC on held-out folds")
    dominant_drivers: List[str] = Field(
        default=["openness_to_experience", "conscientiousness"],
        description="Top empirical predictive drivers verified via permutation importance"
    )
    ethical_safeguard_notice: str = Field(
        default=(
            "MANDATORY GOVERNANCE NOTICE: This model reflects empirical statistical associations with "
            "observed consulting performance in a senior cohort. In accordance with project ethical guardrails, "
            "personality traits must NEVER be used as automated hiring, filtering, promotion, or termination gates. "
            "This output is strictly intended for mentoring, professional coaching, and self-awareness."
        ),
        description="Mandatory ethical boundary statement"
    )
    feature_contributions: Optional[Dict[str, float]] = Field(
        default=None, description="Standardized odds ratio or coefficient weights"
    )
