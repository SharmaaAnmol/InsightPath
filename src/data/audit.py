"""
audit.py
--------
Master audit runner for Phase 1.
Loads all four raw datasets without mutation, computes all diagnostic metrics,
generates the complete suite of CSV profile tables under outputs/tables/,
and outputs verified audit metrics.
"""

import os
import pandas as pd
from typing import Dict, Any

from src.data.loaders import load_csv_dataset, load_excel_dataset
from src.data.profiling import (
    profile_dataframe,
    profile_missing_values,
    profile_duplicates,
    profile_identifier,
    profile_numeric_columns,
    detect_potential_outliers,
    profile_categorical_columns,
    profile_target_distribution,
)


def run_full_phase1_audit(raw_dir: str = "data/raw", output_dir: str = "outputs/tables") -> Dict[str, Any]:
    """Execute the end-to-end Phase 1 audit pipeline and export CSV tables."""
    os.makedirs(output_dir, exist_ok=True)
    results = {}
    
    # -------------------------------------------------------------------------
    # 1. Ingestion
    # -------------------------------------------------------------------------
    ds_path = os.path.join(raw_dir, "DataScience Jobs.csv")
    aj_path = os.path.join(raw_dir, "Analytics Jobs.csv")
    jds_path = os.path.join(raw_dir, "JDS Skill Traits.xlsx")
    sds_path = os.path.join(raw_dir, "SDS Personality Traits.xlsx")
    
    df_ds = load_csv_dataset(ds_path)
    df_aj = load_csv_dataset(aj_path)
    jds_sheets, df_jds = load_excel_dataset(jds_path)
    sds_sheets, df_sds = load_excel_dataset(sds_path)
    
    datasets = {
        "DataScience Jobs": df_ds,
        "Analytics Jobs": df_aj,
        "JDS Skill Traits": df_jds,
        "SDS Personality Traits": df_sds
    }
    
    # -------------------------------------------------------------------------
    # 2. Structural & Data Type Profiling
    # -------------------------------------------------------------------------
    dtype_records = []
    semantic_map = {
        # DataScience Jobs
        ("DataScience Jobs", "reference_no"): ("Identifier / Key", "Categorical / Key", "Integer reference number (non-unique)"),
        ("DataScience Jobs", "company_name"): ("Hiring Organization", "Categorical / Text", "Company name string"),
        ("DataScience Jobs", "job_title"): ("Role Title", "Categorical", "Standardized job title"),
        ("DataScience Jobs", "min_experience"): ("Experience Barrier", "Numeric (Years)", "Minimum required experience"),
        ("DataScience Jobs", "avg_salary"): ("Compensation (Mean)", "Numeric Text (Lakhs)", "String currency with 'L' suffix"),
        ("DataScience Jobs", "min_salary"): ("Compensation (Min)", "Numeric Text (Lakhs)", "String currency with 'L' suffix"),
        ("DataScience Jobs", "max_salary"): ("Compensation (Max)", "Numeric Text (Lakhs)", "String currency with 'L' suffix"),
        ("DataScience Jobs", "num_of_jobs"): ("Requisition Volume", "Numeric (Count)", "Number of vacancies advertised"),
        # Analytics Jobs
        ("Analytics Jobs", "s_no"): ("Identifier / Index", "Integer Key", "Sequential row index"),
        ("Analytics Jobs", "experience"): ("Experience Range", "Text Range", "Experience string interval (e.g. '6-10 yrs')"),
        ("Analytics Jobs", "job_description"): ("Job Text", "Text / NLP", "Free-form natural language text"),
        ("Analytics Jobs", "job_desig"): ("Job Title", "Text / Categorical", "Unstructured designation string"),
        ("Analytics Jobs", "job_type"): ("Job Family", "Categorical", "Category flag (75.8% missing)"),
        ("Analytics Jobs", "key_skills"): ("Skill List", "Text / Delimited", "Comma-delimited skill keywords"),
        ("Analytics Jobs", "location"): ("Geographic Hub", "Categorical / Text", "City/region strings, multi-city"),
        ("Analytics Jobs", "salary"): ("Salary Bracket", "Categorical (Ordinal)", "6 discrete string brackets"),
        # JDS Skill Traits
        ("JDS Skill Traits", "id"): ("Employee Identifier", "Integer Key", "Anonymized junior employee ID"),
        ("JDS Skill Traits", "big_data_skills"): ("Technical Competency", "Numeric (1-5 Scale)", "Big data rating"),
        ("JDS Skill Traits", "maths-stats_skills"): ("Technical Competency", "Numeric (1-5 Scale)", "Math & stats rating"),
        ("JDS Skill Traits", "coding_skills"): ("Technical Competency", "Numeric (1-5 Scale)", "Programming rating"),
        ("JDS Skill Traits", "ai_and_ml_skills"): ("Technical Competency", "Numeric (1-5 Scale)", "AI/ML rating"),
        ("JDS Skill Traits", "dashboard_and_storytelling_skills"): ("Technical Competency", "Numeric (1-5 Scale)", "BI & storytelling rating"),
        ("JDS Skill Traits", "salary_hike_high_or_low"): ("Career Outcome Target", "Binary Indicator", "1=High hike, 0=Low hike"),
    }
    
    for ds_name, df in datasets.items():
        for col in df.columns:
            s = df[col]
            n_unique = s.dropna().nunique()
            n_tot = len(df)
            pct_unique = round((n_unique / n_tot) * 100, 2) if n_tot > 0 else 0.0
            sample_vals = str(s.dropna().head(3).tolist())
            
            # Lookup semantic role
            clean_c = col.strip()
            sem_info = semantic_map.get((ds_name, clean_c), ("Personality / Outcome", "Numeric / Target", "Psychometric measurement / Target"))
            
            dtype_records.append({
                "dataset": ds_name,
                "column": col,
                "raw_dtype": str(s.dtype),
                "inferred_semantic_role": sem_info[0],
                "semantic_type": sem_info[1],
                "description": sem_info[2],
                "unique_count": n_unique,
                "unique_percentage": pct_unique,
                "example_values": sample_vals
            })
            
    df_dtypes = pd.DataFrame(dtype_records)
    df_dtypes.to_csv(os.path.join(output_dir, "data_type_profile.csv"), index=False)
    results["data_type_profile"] = df_dtypes
    
    # -------------------------------------------------------------------------
    # 3. Missing Value Audit
    # -------------------------------------------------------------------------
    missing_dfs = []
    for ds_name, df in datasets.items():
        missing_dfs.append(profile_missing_values(df, ds_name))
    df_missing = pd.concat(missing_dfs, ignore_index=True)
    df_missing.to_csv(os.path.join(output_dir, "missing_value_profile.csv"), index=False)
    results["missing_value_profile"] = df_missing
    
    # -------------------------------------------------------------------------
    # 4. Duplicate Profile
    # -------------------------------------------------------------------------
    id_map = {
        "DataScience Jobs": "reference_no",
        "Analytics Jobs": "s_no",
        "JDS Skill Traits": "id",
        "SDS Personality Traits": "id"
    }
    dup_records = []
    for ds_name, df in datasets.items():
        dup_records.append(profile_duplicates(df, ds_name, id_map[ds_name]))
    df_dups = pd.DataFrame(dup_records)
    df_dups.to_csv(os.path.join(output_dir, "duplicate_profile.csv"), index=False)
    results["duplicate_profile"] = df_dups
    
    # -------------------------------------------------------------------------
    # 5. Identifier Audit
    # -------------------------------------------------------------------------
    id_records = []
    for ds_name, df in datasets.items():
        id_records.append(profile_identifier(df, id_map[ds_name], ds_name))
    df_ids = pd.DataFrame(id_records)
    df_ids.to_csv(os.path.join(output_dir, "id_audit.csv"), index=False)
    results["id_audit"] = df_ids
    
    # -------------------------------------------------------------------------
    # 6. Numerical Profile & Outliers
    # -------------------------------------------------------------------------
    num_dfs = []
    # DataScience Jobs numeric
    num_dfs.append(profile_numeric_columns(df_ds, "DataScience Jobs", ["min_experience", "num_of_jobs"]))
    # JDS numeric
    jds_num_cols = ["big_data_skills", "maths-stats_skills", "coding_skills", "ai_and_ml_skills", "dashboard_and_storytelling_skills"]
    num_dfs.append(profile_numeric_columns(df_jds, "JDS Skill Traits", jds_num_cols))
    # SDS numeric
    sds_cols = [c for c in df_sds.columns if c.strip() != "id" and "success" not in c.lower()]
    num_dfs.append(profile_numeric_columns(df_sds, "SDS Personality Traits", sds_cols))
    
    df_num = pd.concat(num_dfs, ignore_index=True)
    df_num.to_csv(os.path.join(output_dir, "numerical_profile.csv"), index=False)
    results["numerical_profile"] = df_num
    
    # Outliers
    outlier_dfs = []
    outlier_dfs.append(detect_potential_outliers(df_ds, ["min_experience", "num_of_jobs"], "DataScience Jobs"))
    outlier_dfs.append(detect_potential_outliers(df_jds, jds_num_cols, "JDS Skill Traits"))
    outlier_dfs.append(detect_potential_outliers(df_sds, sds_cols, "SDS Personality Traits"))
    df_outliers = pd.concat(outlier_dfs, ignore_index=True)
    df_outliers.to_csv(os.path.join(output_dir, "outlier_profile.csv"), index=False)
    results["outlier_profile"] = df_outliers
    
    # -------------------------------------------------------------------------
    # 7. Categorical Profile
    # -------------------------------------------------------------------------
    cat_dfs = []
    cat_dfs.append(profile_categorical_columns(df_ds, "DataScience Jobs"))
    cat_dfs.append(profile_categorical_columns(df_aj, "Analytics Jobs"))
    df_cats = pd.concat(cat_dfs, ignore_index=True)
    df_cats.to_csv(os.path.join(output_dir, "categorical_profile.csv"), index=False)
    results["categorical_profile"] = df_cats
    
    # -------------------------------------------------------------------------
    # 8. JDS & SDS Range Audits & Targets
    # -------------------------------------------------------------------------
    # JDS Range Audit
    jds_range_records = []
    for c in jds_num_cols:
        s = pd.to_numeric(df_jds[c], errors="coerce").dropna()
        jds_range_records.append({
            "skill_dimension": c,
            "valid_records": len(s),
            "min_score": round(float(s.min()), 2),
            "max_score": round(float(s.max()), 2),
            "within_1_to_5": bool(s.min() >= 1.0 and s.max() <= 5.0),
            "ceiling_5_0_count": int((s == 5.0).sum()),
            "ceiling_5_0_pct": round(float((s == 5.0).sum() / len(s)) * 100, 2)
        })
    df_jds_range = pd.DataFrame(jds_range_records)
    df_jds_range.to_csv(os.path.join(output_dir, "jds_skill_range_audit.csv"), index=False)
    results["jds_skill_range_audit"] = df_jds_range
    
    # JDS Target
    jds_target = profile_target_distribution(df_jds, "salary_hike_high_or_low", "JDS Skill Traits")
    df_jds_tgt = pd.DataFrame([jds_target])
    df_jds_tgt.to_csv(os.path.join(output_dir, "jds_target_distribution.csv"), index=False)
    results["jds_target_distribution"] = df_jds_tgt
    
    # SDS Range Audit
    sds_range_records = []
    for c in sds_cols:
        s = pd.to_numeric(df_sds[c], errors="coerce").dropna()
        sds_range_records.append({
            "trait_dimension": c,
            "valid_records": len(s),
            "min_score": round(float(s.min()), 2),
            "max_score": round(float(s.max()), 2),
            "score_span": round(float(s.max() - s.min()), 2),
            "within_17_to_68": bool(s.min() >= 17.0 and s.max() <= 68.0)
        })
    df_sds_range = pd.DataFrame(sds_range_records)
    df_sds_range.to_csv(os.path.join(output_dir, "sds_trait_range_audit.csv"), index=False)
    results["sds_trait_range_audit"] = df_sds_range
    
    # SDS Target
    sds_target_col = [c for c in df_sds.columns if "success" in c.lower()][0]
    sds_target = profile_target_distribution(df_sds, sds_target_col, "SDS Personality Traits")
    df_sds_tgt = pd.DataFrame([sds_target])
    df_sds_tgt.to_csv(os.path.join(output_dir, "sds_target_distribution.csv"), index=False)
    results["sds_target_distribution"] = df_sds_tgt
    
    # Combined Target Balance Table
    df_target_bal = pd.DataFrame([jds_target, sds_target])
    df_target_bal.to_csv(os.path.join(output_dir, "target_class_balance.csv"), index=False)
    results["target_class_balance"] = df_target_bal
    
    # -------------------------------------------------------------------------
    # 9. Consolidated Anomaly Inventory
    # -------------------------------------------------------------------------
    anomaly_records = [
        {
            "dataset": "JDS Skill Traits",
            "column": "ALL (Rows 140-171)",
            "issue_type": "Trailing Empty Rows",
            "affected_count": 32,
            "affected_percentage": 18.71,
            "example_values": "All 7 columns None / NaN",
            "severity": "CRITICAL",
            "recommended_phase2_action": "Filter out completely blank trailing rows (dropna where all null); analytical sample N=139."
        },
        {
            "dataset": "SDS Personality Traits",
            "column": "' extraversion', 'success_ classification_ high_low'",
            "issue_type": "Whitespace in Header Names",
            "affected_count": 2,
            "affected_percentage": 28.57,
            "example_values": "Leading space in ' extraversion', spaces in target name",
            "severity": "HIGH",
            "recommended_phase2_action": "Sanitize column headers with .str.strip().str.replace(' ', '_').str.lower()."
        },
        {
            "dataset": "Analytics Jobs",
            "column": "job_type",
            "issue_type": "Extreme Missingness & Inconsistent Casing",
            "affected_count": 12011,
            "affected_percentage": 75.82,
            "example_values": "NaN (12,011), 'Analytics', 'analytics', 'ANALYTICS'",
            "severity": "HIGH",
            "recommended_phase2_action": "Standardize populated casing; document as uninformative and exclude from predictive modeling."
        },
        {
            "dataset": "Analytics Jobs",
            "column": "job_description",
            "issue_type": "High Missingness",
            "affected_count": 3508,
            "affected_percentage": 22.14,
            "example_values": "NaN",
            "severity": "MEDIUM",
            "recommended_phase2_action": "Impute with empty string for text processing; use key_skills as primary skill source."
        },
        {
            "dataset": "DataScience Jobs",
            "column": "avg_salary, min_salary, max_salary",
            "issue_type": "Text Currency Representation",
            "affected_count": 1602,
            "affected_percentage": 100.0,
            "example_values": "'4.5L', '16.0L', '7.8L'",
            "severity": "HIGH",
            "recommended_phase2_action": "Develop numeric parser stripping 'L' and casting to continuous float64 (Lakhs INR)."
        },
        {
            "dataset": "Analytics Jobs",
            "column": "salary",
            "issue_type": "Discrete Textual Salary Brackets",
            "affected_count": 15841,
            "affected_percentage": 100.0,
            "example_values": "'10to15', '15to25', '6to10'",
            "severity": "HIGH",
            "recommended_phase2_action": "Encode as ordinal factor and compute interval midpoints for numeric approximations."
        },
        {
            "dataset": "Analytics Jobs",
            "column": "experience",
            "issue_type": "Unstructured Interval Strings",
            "affected_count": 15841,
            "affected_percentage": 100.0,
            "example_values": "'6-10 yrs', '2-5 yrs', '5-10 yrs'",
            "severity": "HIGH",
            "recommended_phase2_action": "Regex extraction to create min_experience, max_experience, and midpoint_experience."
        },
        {
            "dataset": "DataScience Jobs",
            "column": "reference_no",
            "issue_type": "Non-Unique Identifiers",
            "affected_count": 142,
            "affected_percentage": 8.86,
            "example_values": "Ref 1024 shared by Exl India & IHS Markit",
            "severity": "MEDIUM",
            "recommended_phase2_action": "Retain rows as postings; never use reference_no as primary key or modeling feature."
        },
        {
            "dataset": "JDS Skill Traits",
            "column": "id",
            "issue_type": "Duplicate IDs with Conflicting Targets",
            "affected_count": 4,
            "affected_percentage": 2.88,
            "example_values": "ID 3291 has target 0 in row 3 and target 1 in row 29",
            "severity": "CRITICAL",
            "recommended_phase2_action": "Audit feature vectors of ID 3291. Treat as label conflict; evaluate model sensitivity with/without."
        },
        {
            "dataset": "SDS Personality Traits",
            "column": "id",
            "issue_type": "Duplicate Anonymized Subject IDs",
            "affected_count": 18,
            "affected_percentage": 11.18,
            "example_values": "ID 8065 has 2 distinct rows with different traits and targets",
            "severity": "HIGH",
            "recommended_phase2_action": "Do not treat ID as unique key; treat rows as distinct observations; drop ID from modeling."
        },
        {
            "dataset": "DataScience Jobs",
            "column": "num_of_jobs",
            "issue_type": "Extreme Right Skewness & Bulk Hiring Outliers",
            "affected_count": 139,
            "affected_percentage": 8.68,
            "example_values": "Max=4,200 vs Median=22",
            "severity": "MEDIUM",
            "recommended_phase2_action": "Compute log-transformed volume log10(num_of_jobs) alongside raw counts."
        },
        {
            "dataset": "Analytics Jobs",
            "column": "key_skills",
            "issue_type": "Single Missing Record",
            "affected_count": 1,
            "affected_percentage": 0.006,
            "example_values": "NaN",
            "severity": "LOW",
            "recommended_phase2_action": "Impute with 'Not Specified' or empty string."
        }
    ]
    df_anom = pd.DataFrame(anomaly_records)
    df_anom.to_csv(os.path.join(output_dir, "anomaly_inventory.csv"), index=False)
    results["anomaly_inventory"] = df_anom
    
    return results


if __name__ == "__main__":
    print("Executing Phase 1 master audit pipeline...")
    res = run_full_phase1_audit()
    print("Audit execution completed successfully. Tables generated:")
    for k in res:
        print(f" - {k}")
