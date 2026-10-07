"""
backend/schemas/__init__.py
---------------------------
Exports for backend Pydantic schemas.
"""

from backend.schemas.health import HealthResponse
from backend.schemas.data import TableResponse
from backend.schemas.jds import (
    JDSPredictRequest,
    JDSPredictResponse,
    JDSSummaryResponse,
    JDSModelPerformanceResponse,
    JDSFeatureImportanceResponse,
    JDSOddsRatiosResponse,
)
from backend.schemas.sds import (
    SDSPredictRequest,
    SDSPredictResponse,
    SDSSummaryResponse,
    SDSModelPerformanceResponse,
    SDSFeatureImportanceResponse,
    SDSOddsRatiosResponse,
)
from backend.schemas.market import (
    MarketOverviewResponse,
    RoleDemandResponse,
    CompanyDemandResponse,
    LocationDemandResponse,
    SkillFrequencyResponse,
    PremiumSkillsResponse,
)
from backend.schemas.framework import (
    TalentMatrixResponse,
    CareerStagesResponse,
    CompetenciesResponse,
    StakeholdersResponse,
)

__all__ = [
    "HealthResponse",
    "TableResponse",
    "JDSPredictRequest",
    "JDSPredictResponse",
    "JDSSummaryResponse",
    "JDSModelPerformanceResponse",
    "JDSFeatureImportanceResponse",
    "JDSOddsRatiosResponse",
    "SDSPredictRequest",
    "SDSPredictResponse",
    "SDSSummaryResponse",
    "SDSModelPerformanceResponse",
    "SDSFeatureImportanceResponse",
    "SDSOddsRatiosResponse",
    "MarketOverviewResponse",
    "RoleDemandResponse",
    "CompanyDemandResponse",
    "LocationDemandResponse",
    "SkillFrequencyResponse",
    "PremiumSkillsResponse",
    "TalentMatrixResponse",
    "CareerStagesResponse",
    "CompetenciesResponse",
    "StakeholdersResponse",
]
