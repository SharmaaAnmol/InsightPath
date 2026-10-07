"""
backend/api/v1/endpoints/synthesis.py
-------------------------------------
Endpoints serving cross-dataset synthesis tables (Methodological Triangulation).
"""

from fastapi import APIRouter, HTTPException
from backend.schemas.data import TableResponse
from backend.services.data_service import data_service

router = APIRouter()


@router.get("/market-skill-matrix", response_model=TableResponse)
def get_market_skill_matrix() -> TableResponse:
    """Returns the Asymmetric Dual-Currency skill progression matrix."""
    try:
        return data_service.get_market_skill_matrix()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/career-stage-matrix", response_model=TableResponse)
def get_career_stage_matrix() -> TableResponse:
    """Returns the 4-tier career stage progression matrix."""
    try:
        return data_service.get_career_stage_matrix()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/gap-analysis", response_model=TableResponse)
def get_gap_analysis() -> TableResponse:
    """Returns the 5 systemic labor market talent gaps."""
    try:
        return data_service.get_gap_analysis()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/evidence-matrix", response_model=TableResponse)
def get_evidence_matrix() -> TableResponse:
    """Returns multi-lens cross-evidence synthesis matrix."""
    try:
        return data_service.get_evidence_matrix()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
