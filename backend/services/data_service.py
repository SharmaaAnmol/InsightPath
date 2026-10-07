"""
backend/services/data_service.py
--------------------------------
Service layer for loading, parsing, and serving precomputed analytical CSV outputs
from Phases 3, 4, 5, 6, 7, 8, and Phase 9 final traceability tables.
Implements robust pathlib resolution and in-memory caching for sub-millisecond responses.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import logging
import pandas as pd

from backend.config import settings
from backend.schemas.data import TableResponse
from backend.schemas.market import (
    MarketOverviewResponse,
    RoleDemandResponse,
    CompanyDemandResponse,
    LocationDemandResponse,
    SkillFrequencyResponse,
    PremiumSkillsResponse,
)
from backend.schemas.jds import (
    JDSSummaryResponse,
    JDSModelPerformanceResponse,
    JDSFeatureImportanceResponse,
    JDSOddsRatiosResponse,
)
from backend.schemas.sds import (
    SDSSummaryResponse,
    SDSModelPerformanceResponse,
    SDSFeatureImportanceResponse,
    SDSOddsRatiosResponse,
)
from backend.schemas.framework import (
    TalentMatrixResponse,
    CareerStagesResponse,
    CompetenciesResponse,
    StakeholdersResponse,
)

logger = logging.getLogger(__name__)


class DataService:
    def __init__(self):
        self._table_cache: Dict[str, TableResponse] = {}
        self._typed_cache: Dict[str, Any] = {}

    def _read_csv(self, relative_path: str) -> pd.DataFrame:
        """Safely resolves and reads a CSV artifact using pathlib relative to TABLES_DIR."""
        full_path = (settings.TABLES_DIR / relative_path).resolve()
        if not full_path.exists():
            raise FileNotFoundError(f"Requested analytical table not found at: {full_path}")
        return pd.read_csv(full_path)

    def get_table(self, relative_path: str, table_name: Optional[str] = None) -> TableResponse:
        """Loads a generic CSV table, caches it in memory, and returns TableResponse."""
        if relative_path in self._table_cache:
            return self._table_cache[relative_path]

        df = self._read_csv(relative_path)
        records = df.where(pd.notnull(df), None).to_dict(orient="records")
        name = table_name or Path(relative_path).stem
        full_path = settings.TABLES_DIR / relative_path

        response = TableResponse(
            table_name=name,
            source_path=f"outputs/tables/{relative_path}",
            row_count=len(df),
            columns=list(df.columns),
            records=records,
            metadata={"file_size_bytes": full_path.stat().st_size if full_path.exists() else 0},
        )
        self._table_cache[relative_path] = response
        return response

    # =========================================================================
    # MARKET INTELLIGENCE (PHASE 3)
    # =========================================================================

    def get_market_overview(self) -> MarketOverviewResponse:
        cache_key = "market_overview"
        if cache_key in self._typed_cache:
            return self._typed_cache[cache_key]

        df_salary = self._read_csv("phase3/phase3_salary_summary.csv")
        df_desc = self._read_csv("phase3/phase3_descriptive_summary.csv")

        salary_records = df_salary.where(pd.notnull(df_salary), None).to_dict(orient="records")
        desc_records = df_desc.where(pd.notnull(df_desc), None).to_dict(orient="records")

        response = MarketOverviewResponse(
            total_postings=17443,
            analytics_jobs_count=15841,
            datascience_jobs_count=1602,
            median_experience_years=5.5,
            median_salary_lakh=12.2,
            salary_breakdowns=salary_records,
            macro_descriptives=desc_records,
        )
        self._typed_cache[cache_key] = response
        return response

    def get_role_demand(self) -> RoleDemandResponse:
        cache_key = "role_demand"
        if cache_key in self._typed_cache:
            return self._typed_cache[cache_key]

        df = self._read_csv("phase3/phase3_role_demand.csv")
        records = df.where(pd.notnull(df), None).to_dict(orient="records")
        top_role = str(records[0].get("job_title", "Business Analyst")) if records else None

        response = RoleDemandResponse(
            table_name="role_demand",
            source_path="outputs/tables/phase3/phase3_role_demand.csv",
            row_count=len(df),
            columns=list(df.columns),
            top_role_by_openings=top_role,
            records=records,
        )
        self._typed_cache[cache_key] = response
        return response

    def get_company_demand(self) -> CompanyDemandResponse:
        cache_key = "company_demand"
        if cache_key in self._typed_cache:
            return self._typed_cache[cache_key]

        df = self._read_csv("phase3/phase3_company_demand.csv")
        records = df.where(pd.notnull(df), None).to_dict(orient="records")
        top_company = str(records[0].get("company_name", "TCS")) if records else None

        response = CompanyDemandResponse(
            table_name="company_demand",
            source_path="outputs/tables/phase3/phase3_company_demand.csv",
            row_count=len(df),
            columns=list(df.columns),
            top_employer=top_company,
            records=records,
        )
        self._typed_cache[cache_key] = response
        return response

    def get_location_summary(self) -> LocationDemandResponse:
        cache_key = "location_summary"
        if cache_key in self._typed_cache:
            return self._typed_cache[cache_key]

        df = self._read_csv("phase3/phase3_location_summary.csv")
        records = df.where(pd.notnull(df), None).to_dict(orient="records")
        top_cluster = str(records[0].get("location_cluster", "Bengaluru")) if records else None

        response = LocationDemandResponse(
            table_name="location_summary",
            source_path="outputs/tables/phase3/phase3_location_summary.csv",
            row_count=len(df),
            columns=list(df.columns),
            highest_density_cluster=top_cluster,
            records=records,
        )
        self._typed_cache[cache_key] = response
        return response

    def get_skill_frequency(self) -> SkillFrequencyResponse:
        cache_key = "skill_frequency"
        if cache_key in self._typed_cache:
            return self._typed_cache[cache_key]

        df = self._read_csv("phase3/phase3_skill_frequency.csv")
        records = df.where(pd.notnull(df), None).to_dict(orient="records")
        top_skill = str(records[0].get("skill_name", "Sql")) if records else None

        response = SkillFrequencyResponse(
            table_name="skill_frequency",
            source_path="outputs/tables/phase3/phase3_skill_frequency.csv",
            row_count=len(df),
            columns=list(df.columns),
            most_frequent_skill=top_skill,
            records=records,
        )
        self._typed_cache[cache_key] = response
        return response

    def get_premium_skills(self) -> PremiumSkillsResponse:
        cache_key = "premium_skills"
        if cache_key in self._typed_cache:
            return self._typed_cache[cache_key]

        df = self._read_csv("phase3/phase3_skill_salary_comparison.csv")
        records = df.where(pd.notnull(df), None).to_dict(orient="records")
        top_skill = str(records[0].get("skill_name", "R")) if records else None

        response = PremiumSkillsResponse(
            table_name="skill_salary_comparison",
            source_path="outputs/tables/phase3/phase3_skill_salary_comparison.csv",
            row_count=len(df),
            columns=list(df.columns),
            top_premium_skill=top_skill,
            records=records,
        )
        self._typed_cache[cache_key] = response
        return response

    # =========================================================================
    # JUNIOR DATA SCIENTIST MODELING (PHASE 5)
    # =========================================================================

    def get_jds_summary(self) -> JDSSummaryResponse:
        cache_key = "jds_summary"
        if cache_key in self._typed_cache:
            return self._typed_cache[cache_key]

        df = self._read_csv("phase5/phase5_dataset_summary.csv")
        records = df.where(pd.notnull(df), None).to_dict(orient="records")

        response = JDSSummaryResponse(
            cohort_name="Junior Data Scientist (JDS) Analytical Cohort",
            sample_size_n=139,
            features_count=5,
            target_variable="salary_hike_high_or_low",
            source_path="outputs/tables/phase5/phase5_dataset_summary.csv",
            columns=list(df.columns),
            records=records,
        )
        self._typed_cache[cache_key] = response
        return response

    def get_jds_model_performance(self) -> JDSModelPerformanceResponse:
        cache_key = "jds_model_performance"
        if cache_key in self._typed_cache:
            return self._typed_cache[cache_key]

        df = self._read_csv("phase5/phase5_model_performance.csv")
        records = df.where(pd.notnull(df), None).to_dict(orient="records")

        response = JDSModelPerformanceResponse(
            champion_model="Logistic_Regression_L2",
            champion_roc_auc=0.9035,
            validation_strategy="25 Out-of-Sample Validation Splits (RepeatedStratifiedKFold)",
            source_path="outputs/tables/phase5/phase5_model_performance.csv",
            columns=list(df.columns),
            records=records,
        )
        self._typed_cache[cache_key] = response
        return response

    def get_jds_feature_importance(self) -> JDSFeatureImportanceResponse:
        cache_key = "jds_feature_importance"
        if cache_key in self._typed_cache:
            return self._typed_cache[cache_key]

        df = self._read_csv("phase5/phase5_rf_permutation_importance.csv")
        records = df.where(pd.notnull(df), None).to_dict(orient="records")
        top_feature = str(records[0].get("feature", "dashboard_and_storytelling_skills")) if records else "dashboard_and_storytelling_skills"

        response = JDSFeatureImportanceResponse(
            method="Permutation Importance on Out-of-Fold Splits",
            top_feature=top_feature,
            source_path="outputs/tables/phase5/phase5_rf_permutation_importance.csv",
            columns=list(df.columns),
            records=records,
        )
        self._typed_cache[cache_key] = response
        return response

    def get_jds_odds_ratios(self) -> JDSOddsRatiosResponse:
        cache_key = "jds_odds_ratios"
        if cache_key in self._typed_cache:
            return self._typed_cache[cache_key]

        df = self._read_csv("phase5/phase5_logistic_odds_ratios.csv")
        records = df.where(pd.notnull(df), None).to_dict(orient="records")
        highest_feature = str(records[0].get("feature", "maths_stats_skills")) if records else "maths_stats_skills"
        highest_or = float(records[0].get("odds_ratio", 3.612)) if records else 3.612

        response = JDSOddsRatiosResponse(
            model="Logistic Regression L2 Regularized",
            highest_odds_ratio_feature=highest_feature,
            highest_odds_ratio_value=highest_or,
            source_path="outputs/tables/phase5/phase5_logistic_odds_ratios.csv",
            columns=list(df.columns),
            records=records,
        )
        self._typed_cache[cache_key] = response
        return response

    # =========================================================================
    # SENIOR DATA SCIENTIST MODELING (PHASE 6)
    # =========================================================================

    def get_sds_summary(self) -> SDSSummaryResponse:
        cache_key = "sds_summary"
        if cache_key in self._typed_cache:
            return self._typed_cache[cache_key]

        df = self._read_csv("phase6/phase6_dataset_summary.csv")
        records = df.where(pd.notnull(df), None).to_dict(orient="records")

        response = SDSSummaryResponse(
            cohort_name="Senior Data Scientist (SDS) Primary Cohort",
            sample_size_n=161,
            unique_subjects_n=152,
            traits_evaluated=5,
            target_variable="success_high_or_low",
            source_path="outputs/tables/phase6/phase6_dataset_summary.csv",
            columns=list(df.columns),
            records=records,
        )
        self._typed_cache[cache_key] = response
        return response

    def get_sds_model_performance(self) -> SDSModelPerformanceResponse:
        cache_key = "sds_model_performance"
        if cache_key in self._typed_cache:
            return self._typed_cache[cache_key]

        df = self._read_csv("phase6/phase6_model_performance.csv")
        records = df.where(pd.notnull(df), None).to_dict(orient="records")

        response = SDSModelPerformanceResponse(
            champion_model="Logistic_Regression_L2",
            champion_roc_auc=0.9699,
            validation_strategy="StratifiedGroupKFold on Subject ID (Zero Clone Leakage)",
            source_path="outputs/tables/phase6/phase6_model_performance.csv",
            columns=list(df.columns),
            records=records,
        )
        self._typed_cache[cache_key] = response
        return response

    def get_sds_feature_importance(self) -> SDSFeatureImportanceResponse:
        cache_key = "sds_feature_importance"
        if cache_key in self._typed_cache:
            return self._typed_cache[cache_key]

        df = self._read_csv("phase6/phase6_rf_permutation_importance.csv")
        records = df.where(pd.notnull(df), None).to_dict(orient="records")
        top_trait = str(records[0].get("trait_dimension", "openness_to_experience")) if records else "openness_to_experience"

        response = SDSFeatureImportanceResponse(
            method="Permutation Importance on Out-of-Fold Splits",
            top_feature=top_trait,
            source_path="outputs/tables/phase6/phase6_rf_permutation_importance.csv",
            columns=list(df.columns),
            records=records,
        )
        self._typed_cache[cache_key] = response
        return response

    def get_sds_odds_ratios(self) -> SDSOddsRatiosResponse:
        cache_key = "sds_odds_ratios"
        if cache_key in self._typed_cache:
            return self._typed_cache[cache_key]

        df = self._read_csv("phase6/phase6_logistic_odds_ratios.csv")
        records = df.where(pd.notnull(df), None).to_dict(orient="records")
        highest_trait = str(records[0].get("trait_dimension", "conscientiousness")) if records else "conscientiousness"
        highest_or = float(records[0].get("adjusted_odds_ratio", 8.1143)) if records else 8.1143

        response = SDSOddsRatiosResponse(
            model="Logistic Regression L2 Regularized",
            highest_odds_ratio_trait=highest_trait,
            highest_odds_ratio_value=highest_or,
            source_path="outputs/tables/phase6/phase6_logistic_odds_ratios.csv",
            columns=list(df.columns),
            records=records,
        )
        self._typed_cache[cache_key] = response
        return response

    # =========================================================================
    # CAREER-READINESS FRAMEWORK (PHASE 8)
    # =========================================================================

    def get_talent_matrix(self) -> TalentMatrixResponse:
        cache_key = "talent_matrix"
        if cache_key in self._typed_cache:
            return self._typed_cache[cache_key]

        df = self._read_csv("phase8/phase8_four_quadrant_matrix.csv")
        records = df.where(pd.notnull(df), None).to_dict(orient="records")

        response = TalentMatrixResponse(
            table_name="four_quadrant_matrix",
            source_path="outputs/tables/phase8/phase8_four_quadrant_matrix.csv",
            row_count=len(df),
            columns=list(df.columns),
            quadrants=["Q1", "Q2", "Q3", "Q4"],
            records=records,
        )
        self._typed_cache[cache_key] = response
        return response

    def get_career_stages(self) -> CareerStagesResponse:
        cache_key = "career_stages"
        if cache_key in self._typed_cache:
            return self._typed_cache[cache_key]

        df = self._read_csv("phase8/phase8_career_stage_framework.csv")
        records = df.where(pd.notnull(df), None).to_dict(orient="records")

        response = CareerStagesResponse(
            table_name="career_stage_framework",
            source_path="outputs/tables/phase8/phase8_career_stage_framework.csv",
            row_count=len(df),
            columns=list(df.columns),
            records=records,
        )
        self._typed_cache[cache_key] = response
        return response

    def get_competencies(self) -> CompetenciesResponse:
        cache_key = "competencies"
        if cache_key in self._typed_cache:
            return self._typed_cache[cache_key]

        df = self._read_csv("phase8/phase8_competency_priorities.csv")
        records = df.where(pd.notnull(df), None).to_dict(orient="records")

        response = CompetenciesResponse(
            table_name="competency_priorities",
            source_path="outputs/tables/phase8/phase8_competency_priorities.csv",
            row_count=len(df),
            columns=list(df.columns),
            records=records,
        )
        self._typed_cache[cache_key] = response
        return response

    def get_stakeholders(self) -> StakeholdersResponse:
        cache_key = "stakeholders"
        if cache_key in self._typed_cache:
            return self._typed_cache[cache_key]

        df = self._read_csv("phase8/phase8_evidence_to_action.csv")
        records = df.where(pd.notnull(df), None).to_dict(orient="records")

        response = StakeholdersResponse(
            table_name="stakeholder_blueprints",
            source_path="outputs/tables/phase8/phase8_evidence_to_action.csv",
            row_count=len(df),
            columns=list(df.columns),
            records=records,
        )
        self._typed_cache[cache_key] = response
        return response

    # --- Backward compatibility methods for existing routes ---
    def get_market_skill_matrix(self) -> TableResponse:
        return self.get_table("phase7/phase7_market_skill_matrix.csv", "market_skill_matrix")

    def get_career_stage_matrix(self) -> TableResponse:
        return self.get_table("phase7/phase7_career_stage_matrix.csv", "career_stage_matrix")

    def get_gap_analysis(self) -> TableResponse:
        return self.get_table("phase7/phase7_gap_analysis.csv", "gap_analysis")

    def get_evidence_matrix(self) -> TableResponse:
        return self.get_table("phase7/phase7_evidence_matrix.csv", "evidence_matrix")

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

    def get_hypothesis_summary(self) -> TableResponse:
        return self.get_table("phase4/phase4_hypothesis_summary.csv", "hypothesis_summary")

    def get_rq_traceability(self) -> TableResponse:
        return self.get_table("final/final_rq_traceability.csv", "rq_traceability")

    def get_evidence_to_recommendation(self) -> TableResponse:
        return self.get_table("final/final_evidence_to_recommendation.csv", "evidence_to_recommendation")


data_service = DataService()
