"""
backend/api/v1/endpoints/framework.py
-------------------------------------
Endpoints serving Phase 8 Career-Readiness Framework:
Four-Quadrant talent matrix, 4-tier career stages, competency priorities, and stakeholder blueprints.
"""

from fastapi import APIRouter, HTTPException
from backend.schemas.framework import (
    TalentMatrixResponse,
    CareerStagesResponse,
    CompetenciesResponse,
    StakeholdersResponse,
)
from backend.schemas.data import TableResponse
from backend.services.data_service import data_service

router = APIRouter()


@router.get("/talent-matrix", response_model=TalentMatrixResponse)
def get_talent_matrix() -> TalentMatrixResponse:
    """Returns the Four-Quadrant Talent Matrix (Q1 to Q4) with compensation and transition paths."""
    try:
        return data_service.get_talent_matrix()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/career-stages", response_model=CareerStagesResponse)
def get_career_stages() -> CareerStagesResponse:
    """Returns the 4-tier career progression stages with key barriers and measurable KPIs."""
    try:
        return data_service.get_career_stages()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/competencies", response_model=CompetenciesResponse)
def get_competencies() -> CompetenciesResponse:
    """Returns competency priority tiers, empirical ROI multipliers, and target audiences."""
    try:
        return data_service.get_competencies()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/stakeholders", response_model=StakeholdersResponse)
def get_stakeholders() -> StakeholdersResponse:
    """Returns synthesized stakeholder action recommendations and available blueprints."""
    try:
        return data_service.get_stakeholders()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


# --- Backward compatibility aliases ---
@router.get("/quadrants", response_model=TableResponse)
def get_four_quadrant_matrix() -> TableResponse:
    """Alias returning the Four-Quadrant Talent Matrix as TableResponse."""
    try:
        return data_service.get_four_quadrant_matrix()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/blueprints/student", response_model=TableResponse)
def get_student_blueprint() -> TableResponse:
    """Returns the student action blueprint."""
    try:
        return data_service.get_student_blueprint()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/blueprints/university", response_model=TableResponse)
def get_university_blueprint() -> TableResponse:
    """Returns the academic curriculum blueprint."""
    try:
        return data_service.get_university_blueprint()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/blueprints/mentor", response_model=TableResponse)
def get_mentor_blueprint() -> TableResponse:
    """Returns the industry mentoring blueprint."""
    try:
        return data_service.get_mentor_blueprint()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/blueprints/employer", response_model=TableResponse)
def get_employer_blueprint() -> TableResponse:
    """Returns the enterprise employer blueprint."""
    try:
        return data_service.get_employer_blueprint()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
