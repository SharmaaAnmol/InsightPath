"""
clean_data_science_jobs.py
--------------------------
Performs Phase 2 data cleaning and feature engineering for Data Science Jobs.
Cleans company names (safe whitespace stripping).
Parses salary strings with 'L' suffix to numeric Lakhs (min_salary_lakh, avg_salary_lakh, max_salary_lakh).
Validates mathematical salary ordering (min <= avg <= max).
Computes salary spread and relative spread ratio.
Derives log10_num_of_jobs while retaining raw hiring volume outliers.
"""

from typing import Tuple
import numpy as np
import pandas as pd
from src.preprocessing.transformation_log import TransformationLogger
from src.features.salary_features import parse_lakhs_currency_string, compute_salary_spread


def clean_data_science_jobs_dataset(
    df_raw: pd.DataFrame,
    logger: TransformationLogger
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Clean and engineer features for Data Science Jobs dataset.
    Returns:
        df_interim: Cleaned intermediate DataFrame (N=1,602)
        df_processed: Processed analytical DataFrame with derived variables (N=1,602)
    """
    df = df_raw.copy()
    initial_rows = len(df)
    
    # 4.1 Clean company names (safe whitespace trimming only)
    df["company_name"] = df["company_name"].astype(str).str.strip()
    
    logger.log_transformation(
        dataset="DataScience Jobs",
        operation="Trim Company Whitespace",
        columns=["company_name"],
        rows_before=initial_rows,
        rows_after=initial_rows,
        rows_changed=0,
        values_changed="Applied .str.strip() on company names without aggressive deduplication",
        rationale="Eliminate leading/trailing spaces while preserving distinct company entities",
        source_phase1_finding="Phase 1 Text Quality Audit: minor whitespace in company names",
        output_dataset="data_science_jobs_interim"
    )

    # 4.2 Job titles verification
    unique_titles = df["job_title"].nunique()
    if unique_titles != 10:
        raise ValueError(f"Expected 10 standardized job titles, found {unique_titles}")
        
    logger.log_transformation(
        dataset="DataScience Jobs",
        operation="Verify Standardized Job Titles",
        columns=["job_title"],
        rows_before=initial_rows,
        rows_after=initial_rows,
        rows_changed=0,
        values_changed="Preserved 10 standardized role titles exactly as observed",
        rationale="Retain core role taxonomy for macro labor-market segmentation",
        source_phase1_finding="Phase 1 Categorical Audit: exactly 10 standardized titles with 0 typos",
        output_dataset="data_science_jobs_interim"
    )

    # 4.3 Salary parsing: convert 'L' text to continuous numeric float64 Lakhs
    min_sal_lakh = parse_lakhs_currency_string(df["min_salary"])
    avg_sal_lakh = parse_lakhs_currency_string(df["avg_salary"])
    max_sal_lakh = parse_lakhs_currency_string(df["max_salary"])
    
    # Validate mathematical ordering
    invalid_ordering = (min_sal_lakh > avg_sal_lakh) | (avg_sal_lakh > max_sal_lakh)
    if invalid_ordering.sum() > 0:
        raise ValueError(f"Fatal salary ordering violations found in {invalid_ordering.sum()} rows")
        
    df["min_salary_lakh"] = min_sal_lakh
    df["avg_salary_lakh"] = avg_sal_lakh
    df["max_salary_lakh"] = max_sal_lakh
    
    logger.log_transformation(
        dataset="DataScience Jobs",
        operation="Parse Currency Strings to Numeric Lakhs",
        columns=["min_salary", "avg_salary", "max_salary"],
        rows_before=initial_rows,
        rows_after=initial_rows,
        rows_changed=initial_rows,
        values_changed="Parsed 'X.XL' text to numeric float64; preserved raw columns; verified min <= avg <= max",
        rationale="Enable continuous mathematical modeling and statistical analysis of compensation",
        source_phase1_finding="Phase 1 Data Type Audit: salary fields stored as string notation with 'L'",
        output_dataset="data_science_jobs_interim"
    )

    # Interim dataset contains cleaned columns + initial parsed numeric salaries
    df_interim = df.copy()

    # 4.4 Compute salary spread and spread ratio
    spread_lakh, spread_ratio = compute_salary_spread(
        df["min_salary_lakh"],
        df["avg_salary_lakh"],
        df["max_salary_lakh"]
    )
    df["salary_spread_lakh"] = spread_lakh
    df["salary_spread_ratio"] = spread_ratio
    
    logger.log_transformation(
        dataset="DataScience Jobs",
        operation="Derive Salary Spread Metrics",
        columns=["min_salary_lakh", "avg_salary_lakh", "max_salary_lakh"],
        rows_before=initial_rows,
        rows_after=initial_rows,
        rows_changed=initial_rows,
        values_changed="Derived salary_spread_lakh (max - min) and salary_spread_ratio (spread / avg)",
        rationale="Quantify employer compensation flexibility and salary dispersion across roles",
        source_phase1_finding="Phase 0 Feature Engineering Plan: salary dispersion as a key metric",
        output_dataset="data_science_jobs_processed"
    )

    # 4.6 Derive log10_num_of_jobs while retaining raw hiring volume outliers
    # Using log10(1 + num_of_jobs) to avoid log(0) and ensure strictly positive outputs
    df["log10_num_of_jobs"] = np.log10(1.0 + df["num_of_jobs"].astype(float)).round(4)
    
    logger.log_transformation(
        dataset="DataScience Jobs",
        operation="Derive Log-Transformed Opening Volume",
        columns=["num_of_jobs"],
        rows_before=initial_rows,
        rows_after=initial_rows,
        rows_changed=initial_rows,
        values_changed="Derived log10_num_of_jobs = log10(1 + num_of_jobs); retained raw num_of_jobs intact",
        rationale="Stabilize severe positive skewness (+12.83) caused by bulk campus recruitment outliers",
        source_phase1_finding="Phase 1 Numerical Audit: 164 bulk hiring outliers peaking at 4,200 openings",
        output_dataset="data_science_jobs_processed"
    )

    df_processed = df.copy()
    return df_interim, df_processed
