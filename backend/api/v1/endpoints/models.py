"""
backend/api/v1/endpoints/models.py
----------------------------------
Inference endpoints for Junior Data Scientist (JDS) and Senior Data Scientist (SDS)
champion classification pipelines.
"""

from fastapi import APIRouter, HTTPException
from backend.schemas.jds import JDSPredictRequest, JDSPredictResponse
from backend.schemas.sds import SDSPredictRequest, SDSPredictResponse
from backend.services.model_service import model_service

router = APIRouter()


@router.post("/jds/predict", response_model=JDSPredictResponse)
def predict_junior_skill_hike(request: JDSPredictRequest) -> JDSPredictResponse:
    """
    Predicts whether a Junior Data Scientist profile is classified into High vs Low
    salary-hike outcomes based on the 5 validated technical skill traits.
    """
    try:
        return model_service.predict_jds(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"JDS Model evaluation error: {str(exc)}")


@router.post("/sds/predict", response_model=SDSPredictResponse)
def predict_senior_personality_success(request: SDSPredictRequest) -> SDSPredictResponse:
    """
    Evaluates Big Five personality scores to determine high consulting performance alignment.
    Enforces mandatory ethical guardrail notice prohibiting employment gatekeeping.
    """
    try:
        return model_service.predict_sds(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"SDS Model evaluation error: {str(exc)}")


@router.get("/status")
def get_model_registry_status():
    """
    Returns current load status and paths of the champion models.
    """
    return model_service.check_status()
