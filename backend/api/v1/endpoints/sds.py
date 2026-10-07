"""
backend/api/v1/endpoints/sds.py
-------------------------------
Endpoints serving Senior Data Scientist (SDS) Phase 6 personality modeling outputs:
dataset summary, benchmark model performance, feature importance rankings, and odds ratios.
Strictly incorporates ethical non-gatekeeping guidelines.
"""

from fastapi import APIRouter, HTTPException
from backend.schemas.sds import (
    SDSSummaryResponse,
    SDSModelPerformanceResponse,
    SDSFeatureImportanceResponse,
    SDSOddsRatiosResponse,
    SDSGroupTestsResponse,
)
from backend.services.data_service import data_service

router = APIRouter()


@router.get("/summary", response_model=SDSSummaryResponse)
def get_sds_summary() -> SDSSummaryResponse:
    """Returns SDS cohort demographics, unique subject counts, and Big Five dimensionality."""
    try:
        return data_service.get_sds_summary()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/model-performance", response_model=SDSModelPerformanceResponse)
def get_sds_model_performance() -> SDSModelPerformanceResponse:
    """Returns StratifiedGroupKFold cross-validation results guarding against duplicate clone leakage."""
    try:
        return data_service.get_sds_model_performance()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/feature-importance", response_model=SDSFeatureImportanceResponse)
def get_sds_feature_importance() -> SDSFeatureImportanceResponse:
    """Returns permutation importance rankings across Big Five traits on out-of-sample folds."""
    try:
        return data_service.get_sds_feature_importance()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/odds-ratios", response_model=SDSOddsRatiosResponse)
def get_sds_odds_ratios() -> SDSOddsRatiosResponse:
    """Returns standardized odds ratios and confidence intervals from the champion Logistic L2 model."""
    try:
        return data_service.get_sds_odds_ratios()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/group-tests", response_model=SDSGroupTestsResponse)
def get_sds_group_tests() -> SDSGroupTestsResponse:
    """Returns empirical Big Five differences between high and low success senior cohorts (Phase 4 H3)."""
    try:
        return data_service.get_sds_group_tests()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))

