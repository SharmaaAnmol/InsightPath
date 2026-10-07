"""
backend/schemas/jds.py
----------------------
Pydantic schemas for Junior Data Scientist (JDS) skill scoring, model metrics,
feature importance rankings, odds ratios, and prediction inference.
"""

from typing import List, Dict, Any, Optional
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


class JDSSummaryResponse(BaseModel):
    cohort_name: str = Field(default="Junior Data Scientist (JDS) Primary Cohort")
    sample_size_n: int = Field(default=139, description="Validated sample size")
    features_count: int = Field(default=5, description="Technical skill feature count")
    target_variable: str = Field(default="salary_hike_high_or_low")
    source_path: str = Field(default="outputs/tables/phase5/phase5_dataset_summary.csv")
    columns: List[str] = Field(default=[], description="Column headers")
    records: List[Dict[str, Any]]


class JDSModelPerformanceResponse(BaseModel):
    champion_model: str = Field(default="Logistic_Regression_L2")
    champion_roc_auc: float = Field(default=0.9035)
    validation_strategy: str = Field(default="25 Out-of-Sample Validation Splits (RepeatedStratifiedKFold)")
    source_path: str = Field(default="outputs/tables/phase5/phase5_model_performance.csv")
    columns: List[str] = Field(default=[], description="Column headers")
    records: List[Dict[str, Any]]


class JDSFeatureImportanceResponse(BaseModel):
    method: str = Field(default="Permutation Importance on Out-of-Fold Splits")
    top_feature: str = Field(default="dashboard_and_storytelling_skills")
    source_path: str = Field(default="outputs/tables/phase5/phase5_rf_permutation_importance.csv")
    columns: List[str] = Field(default=[], description="Column headers")
    records: List[Dict[str, Any]]


class JDSOddsRatiosResponse(BaseModel):
    model: str = Field(default="Logistic Regression L2 Regularized")
    highest_odds_ratio_feature: str = Field(default="maths_stats_skills")
    highest_odds_ratio_value: float = Field(default=3.612)
    source_path: str = Field(default="outputs/tables/phase5/phase5_logistic_odds_ratios.csv")
    columns: List[str] = Field(default=[], description="Column headers")
    records: List[Dict[str, Any]]


class JDSReducedFeaturesResponse(BaseModel):
    table_name: str = Field(default="full_vs_reduced_features", description="Table identifier")
    source_path: str = Field(default="outputs/tables/phase5/phase5_full_vs_reduced_features.csv")
    top_2_features: List[str] = Field(
        default=["maths_stats_skills", "dashboard_and_storytelling_skills"],
        description="Top two parsimonious skill drivers",
    )
    pct_auc_retained: float = Field(default=96.75, description="Percentage of full discrimination power retained")
    full_roc_auc: float = Field(default=0.9035, description="5-feature full model ROC-AUC")
    reduced_roc_auc: float = Field(default=0.8741, description="2-feature parsimonious model ROC-AUC")
    parsimony_takeaway: str = Field(
        default="Retains 96.7% of full discrimination with 60% fewer features.",
        description="Summary parsimony assessment",
    )
    records: List[Dict[str, Any]] = Field(default=[], description="Full comparison records across algorithms")

