"""
clean_jds.py
------------
Performs Phase 2 data cleaning and standardization for Junior Data Scientist Skill Traits.
Filters only completely blank trailing rows (171 -> 139).
Standardizes column headers (maths-stats_skills -> maths_stats_skills).
Validates continuous skill scores within [1.0, 5.0].
Validates binary target in {0, 1}.
Generates both JDS Baseline (N=139) and JDS Sensitivity (N=137 with ID 3291 removed).
"""

from typing import Tuple, Dict
import pandas as pd
from src.preprocessing.transformation_log import TransformationLogger


def clean_jds_dataset(
    df_raw: pd.DataFrame,
    logger: TransformationLogger
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Clean and validate JDS dataset.
    Returns:
        df_interim: Cleaned intermediate DataFrame (N=139)
        df_baseline: Processed baseline analytical DataFrame (N=139)
        df_sensitivity: Processed sensitivity DataFrame with ID 3291 excluded (N=137)
    """
    df = df_raw.copy()
    initial_rows = len(df)
    
    # 2.1 Remove ONLY completely blank trailing rows
    df_non_blank = df.dropna(how="all").copy()
    rows_after_dropna = len(df_non_blank)
    dropped_blank_count = initial_rows - rows_after_dropna
    
    logger.log_transformation(
        dataset="JDS Skill Traits",
        operation="Remove Completely Blank Rows",
        columns=list(df.columns),
        rows_before=initial_rows,
        rows_after=rows_after_dropna,
        rows_changed=dropped_blank_count,
        values_changed=f"Dropped {dropped_blank_count} empty trailing Excel rows",
        rationale="Rows 140-171 were 100% empty trailing cells resulting from spreadsheet formatting",
        source_phase1_finding="Phase 1 Missing Value Audit: exactly 32 trailing rows are 100% null",
        output_dataset="jds_interim"
    )
    
    if rows_after_dropna != 139:
        raise ValueError(f"Expected 139 valid rows after blank row removal, but got {rows_after_dropna}")

    # 2.2 Standardize column names
    rename_map = {"maths-stats_skills": "maths_stats_skills"}
    df_non_blank = df_non_blank.rename(columns=rename_map)
    
    logger.log_transformation(
        dataset="JDS Skill Traits",
        operation="Standardize Column Header",
        columns=["maths-stats_skills"],
        rows_before=rows_after_dropna,
        rows_after=rows_after_dropna,
        rows_changed=0,
        values_changed="Renamed 'maths-stats_skills' -> 'maths_stats_skills'",
        rationale="Eliminate hyphen operator to conform to valid Python and SQL identifier standards",
        source_phase1_finding="Phase 1 Text Quality Audit: hyphen in maths-stats_skills header",
        output_dataset="jds_interim"
    )

    # 2.3 Convert and validate continuous skill scores
    skill_cols = [
        "big_data_skills",
        "maths_stats_skills",
        "coding_skills",
        "ai_and_ml_skills",
        "dashboard_and_storytelling_skills"
    ]
    
    for col in skill_cols:
        s_numeric = pd.to_numeric(df_non_blank[col], errors="raise")
        # Check boundary compliance
        min_val = s_numeric.min()
        max_val = s_numeric.max()
        if min_val < 1.0 or max_val > 5.0:
            raise ValueError(f"Skill column '{col}' has out-of-bound values: min={min_val}, max={max_val}")
        df_non_blank[col] = s_numeric.astype(float)
        
    logger.log_transformation(
        dataset="JDS Skill Traits",
        operation="Cast and Validate Skill Columns",
        columns=skill_cols,
        rows_before=rows_after_dropna,
        rows_after=rows_after_dropna,
        rows_changed=rows_after_dropna,
        values_changed="Cast 5 skill columns to float64, validated in [1.0, 5.0]",
        rationale="Convert string numbers to continuous float64 for statistical computation",
        source_phase1_finding="Phase 1 Data Type Audit: skill ratings loaded as strings from Excel XML",
        output_dataset="jds_interim"
    )

    # 2.4 Validate target variable
    s_target = pd.to_numeric(df_non_blank["salary_hike_high_or_low"], errors="raise").astype(int)
    unique_targets = set(s_target.unique())
    if not unique_targets.issubset({0, 1}):
        raise ValueError(f"Invalid target values in JDS: {unique_targets}")
    df_non_blank["salary_hike_high_or_low"] = s_target
    
    logger.log_transformation(
        dataset="JDS Skill Traits",
        operation="Validate Binary Target",
        columns=["salary_hike_high_or_low"],
        rows_before=rows_after_dropna,
        rows_after=rows_after_dropna,
        rows_changed=rows_after_dropna,
        values_changed="Cast target to int64, verified binary {0, 1}",
        rationale="Ensure binary classification target integrity without rebalancing",
        source_phase1_finding="Phase 1 Target Balance Audit: binary target with 73 Class 1 and 66 Class 0",
        output_dataset="jds_interim"
    )

    # 2.5 Ensure ID is string/int for traceability
    df_non_blank["id"] = pd.to_numeric(df_non_blank["id"], errors="raise").astype(int)

    # Interim dataset (N=139)
    df_interim = df_non_blank.copy()

    # Baseline processed dataset (N=139)
    df_baseline = df_non_blank.copy()

    # Sensitivity processed dataset: exclude conflicting ID 3291 (N=137)
    df_sensitivity = df_non_blank[df_non_blank["id"] != 3291].copy()
    rows_sensitivity = len(df_sensitivity)
    
    logger.log_transformation(
        dataset="JDS Skill Traits",
        operation="Create Robustness Sensitivity Subset",
        columns=["id", "salary_hike_high_or_low"],
        rows_before=rows_after_dropna,
        rows_after=rows_sensitivity,
        rows_changed=rows_after_dropna - rows_sensitivity,
        values_changed="Excluded 2 rows with duplicate conflicting ID 3291 (139 -> 137)",
        rationale="Isolate label conflict noise for future model sensitivity benchmarking",
        source_phase1_finding="Phase 1 Duplicate Audit: ID 3291 has target=0 in row 3 and target=1 in row 29",
        output_dataset="jds_sensitivity_3291_removed"
    )

    return df_interim, df_baseline, df_sensitivity
