"""
backend/schemas/framework.py
----------------------------
Pydantic schemas for the Phase 8 Career-Readiness Framework:
Four-Quadrant talent matrix, 4-tier career stages, competency priorities, and stakeholder blueprints.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class TalentMatrixResponse(BaseModel):
    table_name: str = Field(default="four_quadrant_matrix", description="Table identifier")
    source_path: str = Field(default="outputs/tables/phase8/phase8_four_quadrant_matrix.csv")
    row_count: int = Field(default=4, description="Four readiness quadrants Q1 to Q4")
    columns: List[str] = Field(default=[], description="Column headers")
    quadrants: List[str] = Field(
        default=["Q1", "Q2", "Q3", "Q4"],
        description="Standard quadrant codes"
    )
    records: List[Dict[str, Any]]


class CareerStagesResponse(BaseModel):
    table_name: str = Field(default="career_stage_framework", description="Table identifier")
    source_path: str = Field(default="outputs/tables/phase8/phase8_career_stage_framework.csv")
    row_count: int = Field(default=4, description="Stages STAGE-1 to STAGE-4")
    columns: List[str] = Field(default=[], description="Column headers")
    stages: List[str] = Field(
        default=[
            "STAGE-1: Entry / Foundation",
            "STAGE-2: Junior / Velocity",
            "STAGE-3: Mid-Career / Expansion",
            "STAGE-4: Senior / Consulting Leadership",
        ],
        description="Career stage progression tracks",
    )
    records: List[Dict[str, Any]]


class CompetenciesResponse(BaseModel):
    table_name: str = Field(default="competency_priorities", description="Table identifier")
    source_path: str = Field(default="outputs/tables/phase8/phase8_competency_priorities.csv")
    row_count: int
    columns: List[str] = Field(default=[], description="Column headers")
    top_velocity_competency: Optional[str] = Field(
        default="Executive Data Storytelling & Dashboarding",
        description="Top empirical salary velocity lever",
    )
    records: List[Dict[str, Any]]


class StakeholdersResponse(BaseModel):
    table_name: str = Field(default="stakeholder_blueprints", description="Table identifier")
    source_path: str = Field(default="outputs/tables/phase8/phase8_evidence_to_action.csv")
    row_count: int
    columns: List[str] = Field(default=[], description="Column headers")
    stakeholders: List[str] = Field(
        default=["Students & Candidates", "Universities & Academia", "Industry Mentors", "Enterprise Employers"],
        description="Target stakeholder cohorts",
    )
    blueprints_available: Dict[str, str] = Field(
        default={
            "student": "outputs/tables/phase8/phase8_student_blueprint.csv",
            "university": "outputs/tables/phase8/phase8_university_blueprint.csv",
            "mentor": "outputs/tables/phase8/phase8_mentor_blueprint.csv",
            "employer": "outputs/tables/phase8/phase8_employer_blueprint.csv",
        }
    )
    records: List[Dict[str, Any]]
