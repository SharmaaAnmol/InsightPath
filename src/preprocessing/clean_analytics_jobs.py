"""
clean_analytics_jobs.py
-----------------------
Performs Phase 2 data cleaning, standardization, and feature engineering for Analytics Jobs.
Parses experience intervals (min, max, midpoint).
Transforms discrete salary brackets (salary_rank, salary_midpoint, is_high_salary).
Cleans job_type (Analytics vs Unspecified).
Cleans job_description and computes char/word count metadata.
Cleans key_skills and derives top-K multi-hot skill indicators.
Normalizes locations into 7 macro clusters.
Maps designations into 6 standardized role families.
Preserves all raw attributes intact.
"""

from typing import Tuple, Optional, List
import pandas as pd
from src.preprocessing.transformation_log import TransformationLogger
from src.features.experience_features import parse_experience_interval
from src.features.salary_features import transform_salary_brackets
from src.features.skill_features import build_skill_frequency_profile, generate_top_k_skill_indicators
from src.features.location_features import clean_location_string, map_location_clusters
from src.features.role_features import map_role_families


def clean_analytics_jobs_dataset(
    df_raw: pd.DataFrame,
    logger: TransformationLogger,
    top_k_skills: int = 50,
    skill_output_path: str = "outputs/tables/skill_frequency_profile.csv"
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Clean and engineer analytical features for Analytics Jobs.
    Returns:
        df_interim: Cleaned intermediate DataFrame (N=15,841)
        df_processed: Processed analytical DataFrame with derived variables (N=15,841)
    """
    df = df_raw.copy()
    initial_rows = len(df)
    
    # 5.1 Experience Parsing
    min_exp, max_exp, mid_exp = parse_experience_interval(df["experience"])
    df["min_experience"] = min_exp
    df["max_experience"] = max_exp
    df["midpoint_experience"] = mid_exp
    
    logger.log_transformation(
        dataset="Analytics Jobs",
        operation="Parse Experience Intervals",
        columns=["experience"],
        rows_before=initial_rows,
        rows_after=initial_rows,
        rows_changed=initial_rows,
        values_changed="Extracted min_experience, max_experience, midpoint_experience; verified min <= max",
        rationale="Convert text intervals ('6-10 yrs') into continuous variables for tenure elasticity analysis",
        source_phase1_finding="Phase 1 Data Type Audit: experience stored as text intervals across 128 formats",
        output_dataset="analytics_jobs_interim"
    )

    # 5.2 Salary Bracket Transformation
    sal_rank, sal_mid, is_high_sal = transform_salary_brackets(df["salary"])
    df["salary_rank"] = sal_rank
    df["salary_midpoint"] = sal_mid
    df["is_high_salary"] = is_high_sal
    
    logger.log_transformation(
        dataset="Analytics Jobs",
        operation="Transform Discrete Salary Brackets",
        columns=["salary"],
        rows_before=initial_rows,
        rows_after=initial_rows,
        rows_changed=initial_rows,
        values_changed="Mapped to salary_rank (1-6), salary_midpoint (1.5-37.5L), is_high_salary (binary >=15L)",
        rationale="Enable ordinal rank correlation, interval midpoint approximation, and high-wage odds modeling",
        source_phase1_finding="Phase 1 Categorical Audit: 6 discrete salary brackets covering 100% of rows",
        output_dataset="analytics_jobs_interim"
    )

    # 5.3 Clean job_type: preserve raw, normalize populated to 'Analytics', missing to 'Unspecified'
    # Descriptive only, excluded from predictive modeling
    clean_jt = df["job_type"].fillna("Unspecified").astype(str).str.strip()
    clean_jt = clean_jt.apply(lambda x: "Analytics" if x.lower() in ["analytics", "analytic"] else "Unspecified")
    df["job_type_clean"] = clean_jt
    
    logger.log_transformation(
        dataset="Analytics Jobs",
        operation="Standardize Job Type & Impute Missing",
        columns=["job_type"],
        rows_before=initial_rows,
        rows_after=initial_rows,
        rows_changed=initial_rows,
        values_changed="Normalized populated entries to 'Analytics'; missing to 'Unspecified' (75.8% missing)",
        rationale="Retain all rows; create clean descriptive label; exclude from predictive models",
        source_phase1_finding="Phase 1 Missing Value Audit: job_type is 75.82% missing with 5 casing variants",
        output_dataset="analytics_jobs_interim"
    )

    # Step 6: Clean job_description and compute char/word count metadata
    desc_clean = df["job_description"].fillna("").astype(str).str.strip()
    df["job_description_clean"] = desc_clean
    df["job_description_char_count"] = desc_clean.str.len()
    df["job_description_word_count"] = desc_clean.apply(lambda x: len(x.split()) if x else 0)
    
    logger.log_transformation(
        dataset="Analytics Jobs",
        operation="Clean Job Description & Compute Length Metadata",
        columns=["job_description"],
        rows_before=initial_rows,
        rows_after=initial_rows,
        rows_changed=3508,
        values_changed="Imputed 3,508 missing values with ''; computed char_count and word_count",
        rationale="Preserve all postings; establish text length bounds without NLP model fitting",
        source_phase1_finding="Phase 1 Missing Value Audit: 22.14% missing in job_description snippets",
        output_dataset="analytics_jobs_interim"
    )

    # Step 7: Clean key_skills
    skills_clean = df["key_skills"].fillna("Not Specified").astype(str).str.strip()
    df["key_skills_clean"] = skills_clean
    
    logger.log_transformation(
        dataset="Analytics Jobs",
        operation="Clean Key Skills & Impute Single Missing Value",
        columns=["key_skills"],
        rows_before=initial_rows,
        rows_after=initial_rows,
        rows_changed=1,
        values_changed="Imputed 1 missing record as 'Not Specified'; trimmed whitespace",
        rationale="Guarantee 100% complete text string for skill tokenization",
        source_phase1_finding="Phase 1 Missing Value Audit: 1 missing record in key_skills",
        output_dataset="analytics_jobs_interim"
    )

    # Interim dataset contains cleaned columns + primary numeric parses
    df_interim = df.copy()

    # Step 8: Build Skill Frequency Profile and extract Top-K multi-hot indicators
    df_skill_profile = build_skill_frequency_profile(
        df["key_skills_clean"],
        total_postings=initial_rows,
        output_path=skill_output_path
    )
    
    top_skills_list = df_skill_profile.head(top_k_skills)["skill"].tolist()
    df_indicators = generate_top_k_skill_indicators(df["key_skills_clean"], top_skills_list)
    
    # Merge indicator features into processed DataFrame
    df_processed = pd.concat([df, df_indicators], axis=1)
    
    logger.log_transformation(
        dataset="Analytics Jobs",
        operation="Generate Top-K Multi-Hot Skill Indicators",
        columns=["key_skills_clean"],
        rows_before=initial_rows,
        rows_after=initial_rows,
        rows_changed=initial_rows,
        values_changed=f"Derived {len(top_skills_list)} binary indicator features from empirical vocabulary",
        rationale="Enable quantitative skill co-occurrence and salary association modeling",
        source_phase1_finding="Phase 0 Research Questions: RQ4 and RQ5 skill demand and compensation analysis",
        output_dataset="analytics_jobs_processed"
    )

    # Step 9: Location cleaning and macro clustering
    df_processed["location_clean"] = clean_location_string(df_processed["location"])
    df_processed["location_cluster"] = map_location_clusters(df_processed["location_clean"])
    
    logger.log_transformation(
        dataset="Analytics Jobs",
        operation="Map Locations to 7 Macro Clusters",
        columns=["location"],
        rows_before=initial_rows,
        rows_after=initial_rows,
        rows_changed=initial_rows,
        values_changed="Aggregated 1,355 locations into 7 macro clusters: Bengaluru, NCR, Mumbai, Pune, Hyderabad, Chennai, Other/Tier-2",
        rationale="Reduce extreme geographic cardinality while capturing major tech employment corridors",
        source_phase1_finding="Phase 1 Categorical Audit: 1,355 location strings with frequent multi-city combinations",
        output_dataset="analytics_jobs_processed"
    )

    # Step 10: Designation role family mapping
    df_processed["job_role_family"] = map_role_families(df_processed["job_desig"])
    
    logger.log_transformation(
        dataset="Analytics Jobs",
        operation="Map Designations to 6 Role Families",
        columns=["job_desig"],
        rows_before=initial_rows,
        rows_after=initial_rows,
        rows_changed=initial_rows,
        values_changed="Classified 10,097 titles into: Data Scientist, Data Analyst, Business Analyst, Data Engineer, BI Developer, Non-Analytics/Other",
        rationale="Filter scraping noise and harmonize role families with DataScience Jobs taxonomy",
        source_phase1_finding="Phase 1 Categorical Audit: 10,097 free-text titles with non-analytics noise",
        output_dataset="analytics_jobs_processed"
    )

    return df_interim, df_processed
