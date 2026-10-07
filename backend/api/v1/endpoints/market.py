"""
backend/api/v1/endpoints/market.py
----------------------------------
Endpoints serving macro and micro job market data derived from
Phases 3 and 4 analyses (DS Jobs: 1,602, Analytics Jobs: 15,841).
"""

from fastapi import APIRouter, HTTPException
from backend.schemas.data import TableResponse
from backend.services.data_service import data_service

router = APIRouter()


@router.get("/roles", response_model=TableResponse)
def get_role_demand() -> TableResponse:
    """Returns macro market demand distribution across standardized data roles."""
    try:
        return data_service.get_role_demand()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/skills", response_model=TableResponse)
def get_skill_frequency() -> TableResponse:
    """Returns top technical skill frequencies and co-occurrences in job requisitions."""
    try:
        return data_service.get_skill_frequency()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/locations", response_model=TableResponse)
def get_location_summary() -> TableResponse:
    """Returns regional demand concentration across the 7 geographic clusters."""
    try:
        return data_service.get_location_summary()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/hypotheses", response_model=TableResponse)
def get_hypotheses_summary() -> TableResponse:
    """Returns empirical decisions and p-values for pre-registered hypotheses H1–H6."""
    try:
        return data_service.get_hypothesis_summary()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
