"""
backend/services/data_service.py
--------------------------------
Service layer for loading and serving precomputed analytical CSV outputs
from Phases 3, 4, 7, 8, and Phase 9 final traceability tables.
Implements in-memory caching for low-latency responses.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import logging
import pandas as pd

from backend.config import settings
from backend.schemas.data import TableResponse

logger = logging.getLogger(__name__)


class DataService:
    def __init__(self):
        self._cache: Dict[str, TableResponse] = {}

    def get_table(self, relative_path: str, table_name: Optional[str] = None) -> TableResponse:
        """
        Loads a CSV table relative to settings.TABLES_DIR, caches it, and returns TableResponse.
        """
        if relative_path in self._cache:
            return self._cache[relative_path]

        full_path = settings.TABLES_DIR / relative_path
        if not full_path.exists():
            raise FileNotFoundError(f"Requested table not found at: {full_path}")

        df = pd.read_csv(full_path)
        records = df.where(pd.notnull(df), None).to_dict(orient="records")
        name = table_name or Path(relative_path).stem

        response = TableResponse(
            table_name=name,
            source_path=f"outputs/tables/{relative_path}",
            row_count=len(df),
            columns=list(df.columns),
            records=records,
            metadata={"file_size_bytes": full_path.stat().st_size},
        )

        self._cache[relative_path] = response
        return response

    # --- Phase 7 Synthesis Tables ---
    def get_market_skill_matrix(self) -> TableResponse:
        return self.get_table("phase7/phase7_market_skill_matrix.csv", "market_skill_matrix")

    def get_career_stage_matrix(self) -> TableResponse:
        return self.get_table("phase7/phase7_career_stage_matrix.csv", "career_stage_matrix")

    def get_gap_analysis(self) -> TableResponse:
        return self.get_table("phase7/phase7_gap_analysis.csv", "gap_analysis")

    def get_evidence_matrix(self) -> TableResponse:
        return self.get_table("phase7/phase7_evidence_matrix.csv", "evidence_matrix")

    # --- Phase 8 Framework Tables ---
    def get_four_quadrant_matrix(self) -> TableResponse:
        return self.get_table("phase8/phase8_four_quadrant_matrix.csv", "four_quadrant_matrix")

    def get_student_blueprint(self) -> TableResponse:
        return self.get_table("phase8/phase8_student_blueprint.csv", "student_blueprint")

    def get_university_blueprint(self) -> TableResponse:
        return self.get_table("phase8/phase8_university_blueprint.csv", "university_blueprint")

    def get_mentor_blueprint(self) -> TableResponse:
        return self.get_table("phase8/phase8_mentor_blueprint.csv", "mentor_blueprint")

    def get_employer_blueprint(self) -> TableResponse:
        return self.get_table("phase8/phase8_employer_blueprint.csv", "employer_blueprint")

    # --- Phase 3 / 4 Market Tables ---
    def get_role_demand(self) -> TableResponse:
        return self.get_table("phase3/phase3_role_demand.csv", "role_demand")

    def get_skill_frequency(self) -> TableResponse:
        return self.get_table("phase3/phase3_skill_frequency.csv", "skill_frequency")

    def get_location_summary(self) -> TableResponse:
        return self.get_table("phase3/phase3_location_summary.csv", "location_summary")

    def get_hypothesis_summary(self) -> TableResponse:
        return self.get_table("phase4/phase4_hypothesis_summary.csv", "hypothesis_summary")

    # --- Final Traceability Tables ---
    def get_rq_traceability(self) -> TableResponse:
        return self.get_table("final/final_rq_traceability.csv", "rq_traceability")

    def get_evidence_to_recommendation(self) -> TableResponse:
        return self.get_table("final/final_evidence_to_recommendation.csv", "evidence_to_recommendation")


data_service = DataService()
