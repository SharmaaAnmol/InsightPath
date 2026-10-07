"""
backend/services/model_service.py
---------------------------------
Service layer for loading, caching, and serving inferences from the
validated JDS and SDS champion machine learning models.
"""

from typing import Dict, Any, Tuple
import json
import logging
from pathlib import Path
import joblib
import pandas as pd
import numpy as np

from backend.config import settings
from backend.schemas.jds import JDSPredictRequest, JDSPredictResponse
from backend.schemas.sds import SDSPredictRequest, SDSPredictResponse

logger = logging.getLogger(__name__)

# Feature column ordering required by scikit-learn pipelines
JDS_FEATURES = [
    "big_data_skills",
    "maths_stats_skills",
    "coding_skills",
    "ai_and_ml_skills",
    "dashboard_and_storytelling_skills",
]

SDS_FEATURES = [
    "neuroticism",
    "extraversion",
    "openness_to_experience",
    "agreeableness",
    "conscientiousness",
]


class ModelService:
    def __init__(self):
        self._jds_model = None
        self._jds_metadata = None
        self._sds_model = None
        self._sds_metadata = None
        self._is_loaded = False

    def load_artifacts(self) -> None:
        """Loads both champion models and metadata from outputs/models/"""
        if self._is_loaded:
            return

        # 1. JDS Model
        if settings.JDS_MODEL_PATH.exists():
            self._jds_model = joblib.load(settings.JDS_MODEL_PATH)
            logger.info("Loaded JDS model from %s", settings.JDS_MODEL_PATH)
        else:
            logger.warning("JDS model artifact not found at %s", settings.JDS_MODEL_PATH)

        if settings.JDS_METADATA_PATH.exists():
            with open(settings.JDS_METADATA_PATH, "r", encoding="utf-8") as f:
                self._jds_metadata = json.load(f)

        # 2. SDS Model
        if settings.SDS_MODEL_PATH.exists():
            self._sds_model = joblib.load(settings.SDS_MODEL_PATH)
            logger.info("Loaded SDS model from %s", settings.SDS_MODEL_PATH)
        else:
            logger.warning("SDS model artifact not found at %s", settings.SDS_MODEL_PATH)

        if settings.SDS_METADATA_PATH.exists():
            with open(settings.SDS_METADATA_PATH, "r", encoding="utf-8") as f:
                self._sds_metadata = json.load(f)

        self._is_loaded = True

    def check_status(self) -> Dict[str, Any]:
        """Returns health verification status of models."""
        self.load_artifacts()
        return {
            "jds_model_loaded": self._jds_model is not None,
            "jds_model_path": str(settings.JDS_MODEL_PATH),
            "sds_model_loaded": self._sds_model is not None,
            "sds_model_path": str(settings.SDS_MODEL_PATH),
        }

    def predict_jds(self, request: JDSPredictRequest) -> JDSPredictResponse:
        """Predicts Junior Data Scientist salary hike classification."""
        self.load_artifacts()
        if self._jds_model is None:
            raise RuntimeError("JDS champion model is not loaded.")

        df_input = pd.DataFrame([{
            "big_data_skills": request.big_data_skills,
            "maths_stats_skills": request.maths_stats_skills,
            "coding_skills": request.coding_skills,
            "ai_and_ml_skills": request.ai_and_ml_skills,
            "dashboard_and_storytelling_skills": request.dashboard_and_storytelling_skills,
        }])[JDS_FEATURES]

        pred = int(self._jds_model.predict(df_input)[0])
        probas = self._jds_model.predict_proba(df_input)[0]
        prob_high = float(probas[1])
        prob_low = float(probas[0])

        label = "High Salary Hike" if pred == 1 else "Low Salary Hike"

        # Coefficients from champion model
        clf_step = getattr(self._jds_model, "named_steps", {}).get("clf")
        contributions = None
        if clf_step and hasattr(clf_step, "coef_"):
            coefs = clf_step.coef_[0]
            contributions = {feat: round(float(coefs[i]), 4) for i, feat in enumerate(JDS_FEATURES)}

        return JDSPredictResponse(
            prediction=pred,
            prediction_label=label,
            probability_high=round(prob_high, 4),
            probability_low=round(prob_low, 4),
            model_name="Logistic_Regression_L2",
            model_roc_auc=0.9035,
            key_differentiators=["dashboard_and_storytelling_skills", "maths_stats_skills"],
            feature_contributions=contributions,
        )

    def predict_sds(self, request: SDSPredictRequest) -> SDSPredictResponse:
        """Predicts Senior Data Scientist consulting success classification."""
        self.load_artifacts()
        if self._sds_model is None:
            raise RuntimeError("SDS champion model is not loaded.")

        df_input = pd.DataFrame([{
            "neuroticism": request.neuroticism,
            "extraversion": request.extraversion,
            "openness_to_experience": request.openness_to_experience,
            "agreeableness": request.agreeableness,
            "conscientiousness": request.conscientiousness,
        }])[SDS_FEATURES]

        pred = int(self._sds_model.predict(df_input)[0])
        probas = self._sds_model.predict_proba(df_input)[0]
        prob_high = float(probas[1])
        prob_low = float(probas[0])

        label = "High Success" if pred == 1 else "Low Success"

        # Coefficients from champion model
        clf_step = getattr(self._sds_model, "named_steps", {}).get("clf")
        contributions = None
        if clf_step and hasattr(clf_step, "coef_"):
            coefs = clf_step.coef_[0]
            contributions = {feat: round(float(coefs[i]), 4) for i, feat in enumerate(SDS_FEATURES)}

        return SDSPredictResponse(
            prediction=pred,
            prediction_label=label,
            probability_high=round(prob_high, 4),
            probability_low=round(prob_low, 4),
            model_name="Logistic_Regression_L2",
            model_roc_auc=0.9699,
            dominant_drivers=["openness_to_experience", "conscientiousness"],
            feature_contributions=contributions,
        )


model_service = ModelService()
