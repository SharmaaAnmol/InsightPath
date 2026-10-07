"""
backend/api/v1/endpoints/assessment.py
--------------------------------------
Endpoints for the Interactive Career-Readiness Assessment.
Accepts self-assessment ratings, evaluates against the serialized JDS champion model,
combines with Phase 5 feature importance and Phase 8 competencies,
and returns an evidence-backed development profile.
"""

from fastapi import APIRouter, HTTPException, status
from backend.schemas.assessment import AssessmentRequest, AssessmentResponse
from backend.services.assessment_service import assessment_service

router = APIRouter()


@router.post(
    "/evaluate",
    response_model=AssessmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Evaluate Career-Readiness Self-Assessment",
    description=(
        "Processes user technical skill ratings through the serialized JDS champion model, "
        "synthesizes out-of-fold feature importance and Phase 8 competency priorities, "
        "and produces an ethical diagnostic development profile."
    ),
)
def evaluate_assessment(request: AssessmentRequest) -> AssessmentResponse:
    """Evaluates user self-assessment against observed cohort models."""
    try:
        return assessment_service.evaluate_assessment(request)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error evaluating career assessment: {str(err)}",
        )
