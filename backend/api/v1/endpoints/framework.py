"""
backend/api/v1/endpoints/framework.py
-------------------------------------
Endpoints serving Phase 8 Career-Readiness Framework and Stakeholder Blueprints.
"""

from fastapi import APIRouter, HTTPException
from backend.schemas.data import TableResponse
from backend.services.data_service import data_service

router = APIRouter()


@router.get("/quadrants", response_model=TableResponse)
def get_four_quadrant_matrix() -> TableResponse:
    """Returns the Four-Quadrant Talent Matrix (Q1 to Q4)."""
    try:
        return data_service.get_four_quadrant_matrix()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/blueprints/student", response_model=TableResponse)
def get_student_blueprint() -> TableResponse:
    """Returns the 4-year student & aspiring data scientist action blueprint."""
    try:
        return data_service.get_student_blueprint()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/blueprints/university", response_model=TableResponse)
def get_university_blueprint() -> TableResponse:
    """Returns the academic curriculum modernization blueprint."""
    try:
        return data_service.get_university_blueprint()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/blueprints/mentor", response_model=TableResponse)
def get_mentor_blueprint() -> TableResponse:
    """Returns the industry mentoring & talent development blueprint."""
    try:
        return data_service.get_mentor_blueprint()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/blueprints/employer", response_model=TableResponse)
def get_employer_blueprint() -> TableResponse:
    """Returns the enterprise employer & talent acquisition blueprint."""
    try:
        return data_service.get_employer_blueprint()
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
