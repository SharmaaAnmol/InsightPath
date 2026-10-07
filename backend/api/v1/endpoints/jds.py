"""
backend/api/v1/endpoints/jds.py
-------------------------------
Endpoints serving Junior Data Scientist (JDS) Phase 5 modeling outputs:
dataset summary, benchmark model performance, feature importance rankings, and odds ratios.
"""

from fastapi import APIRouter, HTTPException
from backend.schemas.jds import (
    JDSSummaryResponse,
    JDSModelPerformanceResponse,
    JDSFeatureImportanceResponse,
    JDSOddsRatiosResponse,
    JDSReducedFeaturesResponse,
)
from backend.services.data_service import data_service

router = APIRouter()


@router.get("/summary", response_model=JDSSummaryResponse)
def get_jds_summary() -> JDSSummaryResponse:
    """Returns JDS cohort summary, feature dimensionality, and target balance."""
    try:
        return data_service.get_jds_summary()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/model-performance", response_model=JDSModelPerformanceResponse)
def get_jds_model_performance() -> JDSModelPerformanceResponse:
    """Returns cross-validated performance metrics across 25 splits for all evaluated algorithms."""
    try:
        return data_service.get_jds_model_performance()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/feature-importance", response_model=JDSFeatureImportanceResponse)
def get_jds_feature_importance() -> JDSFeatureImportanceResponse:
    """Returns out-of-fold permutation importance rankings identifying top skill drivers."""
    try:
        return data_service.get_jds_feature_importance()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/odds-ratios", response_model=JDSOddsRatiosResponse)
def get_jds_odds_ratios() -> JDSOddsRatiosResponse:
    """Returns standardized odds ratios and coefficient weights from the champion Logistic L2 model."""
    try:
        return data_service.get_jds_odds_ratios()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/reduced-features", response_model=JDSReducedFeaturesResponse)
def get_jds_reduced_features() -> JDSReducedFeaturesResponse:
    """Returns parsimonious 2-feature model performance retaining 96.75% AUC."""
    try:
        return data_service.get_jds_reduced_features()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))

