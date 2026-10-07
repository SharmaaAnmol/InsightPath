"""
backend/schemas/market.py
-------------------------
Pydantic schemas for Market Intelligence endpoints, covering macro job demand,
company rankings, geographic clusters, skill frequencies, and premium salary drivers.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class MarketOverviewResponse(BaseModel):
    total_postings: int = Field(default=17443, description="Total audited job postings across both datasets")
    analytics_jobs_count: int = Field(default=15841, description="Macro analytics requisitions")
    datascience_jobs_count: int = Field(default=1602, description="Employer-level data science postings")
    median_experience_years: float = Field(default=5.5, description="Median midpoint required experience")
    median_salary_lakh: float = Field(default=12.2, description="Median benchmark salary in INR Lakhs")
    source_artifacts: List[str] = Field(
        default=[
            "outputs/tables/phase3/phase3_descriptive_summary.csv",
            "outputs/tables/phase3/phase3_salary_summary.csv",
        ],
        description="Originating Phase 3 empirical tables",
    )
    salary_breakdowns: List[Dict[str, Any]] = Field(default=[], description="Segmented salary distributions")
    macro_descriptives: List[Dict[str, Any]] = Field(default=[], description="Variable distribution metrics")


class RoleDemandResponse(BaseModel):
    table_name: str = Field(default="role_demand", description="Table identifier")
    source_path: str = Field(default="outputs/tables/phase3/phase3_role_demand.csv")
    row_count: int
    columns: List[str] = Field(default=[], description="Column headers")
    top_role_by_openings: Optional[str] = None
    records: List[Dict[str, Any]]


class CompanyDemandResponse(BaseModel):
    table_name: str = Field(default="company_demand", description="Table identifier")
    source_path: str = Field(default="outputs/tables/phase3/phase3_company_demand.csv")
    row_count: int
    columns: List[str] = Field(default=[], description="Column headers")
    top_employer: Optional[str] = None
    records: List[Dict[str, Any]]


class LocationDemandResponse(BaseModel):
    table_name: str = Field(default="location_summary", description="Table identifier")
    source_path: str = Field(default="outputs/tables/phase3/phase3_location_summary.csv")
    row_count: int
    columns: List[str] = Field(default=[], description="Column headers")
    highest_density_cluster: Optional[str] = None
    records: List[Dict[str, Any]]


class SkillFrequencyResponse(BaseModel):
    table_name: str = Field(default="skill_frequency", description="Table identifier")
    source_path: str = Field(default="outputs/tables/phase3/phase3_skill_frequency.csv")
    row_count: int
    columns: List[str] = Field(default=[], description="Column headers")
    most_frequent_skill: Optional[str] = None
    records: List[Dict[str, Any]]


class PremiumSkillsResponse(BaseModel):
    table_name: str = Field(default="skill_salary_comparison", description="Table identifier")
    source_path: str = Field(default="outputs/tables/phase3/phase3_skill_salary_comparison.csv")
    row_count: int
    columns: List[str] = Field(default=[], description="Column headers")
    top_premium_skill: Optional[str] = None
    records: List[Dict[str, Any]]


class ExperienceCompensationResponse(BaseModel):
    table_name: str = Field(default="experience_compensation_regression", description="Table identifier")
    source_path: str = Field(default="outputs/tables/phase4/phase4_h5_regression.csv")
    linear_slope_beta: float = Field(default=1.9766, description="Lakh INR salary increase per year of experience")
    linear_intercept: float = Field(default=7.7024, description="Base starting salary intercept in Lakh INR")
    linear_r_squared: float = Field(default=0.3521, description="Coefficient of determination")
    linear_p_value: float = Field(default=2.25e-135, description="Significance p-value with HC3 robust standard errors")
    sample_size_n: int = Field(default=1602, description="DataScience Jobs sample size")
    regression_models: List[Dict[str, Any]] = Field(default=[], description="All fitted regression specifications")
    experience_summary: List[Dict[str, Any]] = Field(default=[], description="Summary statistics by dataset")

