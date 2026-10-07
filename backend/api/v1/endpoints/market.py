"""
backend/api/v1/endpoints/market.py
----------------------------------
Endpoints serving macro and micro job market data derived from
Phases 3 and 4 analyses (DS Jobs: 1,602, Analytics Jobs: 15,841).
"""

from fastapi import APIRouter, HTTPException
from backend.schemas.market import (
    MarketOverviewResponse,
    RoleDemandResponse,
    CompanyDemandResponse,
    LocationDemandResponse,
    SkillFrequencyResponse,
    PremiumSkillsResponse,
    ExperienceCompensationResponse,
)
from backend.schemas.data import TableResponse
from backend.services.data_service import data_service

router = APIRouter()


@router.get("/overview", response_model=MarketOverviewResponse)
def get_market_overview() -> MarketOverviewResponse:
    """Returns high-level macro market statistics, sample sizes, and descriptive distributions."""
    try:
        return data_service.get_market_overview()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/roles", response_model=RoleDemandResponse)
def get_role_demand() -> RoleDemandResponse:
    """Returns macro market demand distribution across standardized data roles."""
    try:
        return data_service.get_role_demand()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/companies", response_model=CompanyDemandResponse)
def get_company_demand() -> CompanyDemandResponse:
    """Returns hiring demand volume, vacancy share, and average salaries across enterprise employers."""
    try:
        return data_service.get_company_demand()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/locations", response_model=LocationDemandResponse)
def get_location_summary() -> LocationDemandResponse:
    """Returns regional demand concentration across the 7 geographic clusters."""
    try:
        return data_service.get_location_summary()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/skills", response_model=SkillFrequencyResponse)
def get_skill_frequency() -> SkillFrequencyResponse:
    """Returns top technical skill frequencies and prevalence across 15,841 requisitions."""
    try:
        return data_service.get_skill_frequency()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/premium-skills", response_model=PremiumSkillsResponse)
def get_premium_skills() -> PremiumSkillsResponse:
    """Returns skills with highest relative prevalence ratios in upper-bracket salaries."""
    try:
        return data_service.get_premium_skills()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/hypotheses", response_model=TableResponse)
def get_hypotheses_summary() -> TableResponse:
    """Returns empirical decisions and p-values for pre-registered hypotheses H1–H6."""
    try:
        return data_service.get_hypothesis_summary()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/experience-compensation", response_model=ExperienceCompensationResponse)
def get_experience_compensation() -> ExperienceCompensationResponse:
    """Returns OLS regression and empirical experience distributions from Phase 4 H5 and Phase 3."""
    try:
        return data_service.get_experience_compensation()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))

