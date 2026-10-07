"""
data.py
-------
Data loading, validation, and anomaly auditing for JDS skill modeling:
  - Ingestion of primary cohort (N=139) and sensitivity cohort (N=137)
  - Strict leakage prevention: feature matrix X excludes ID and target
  - Audit of contradictory duplicate ID 3291
  - Generation of dataset summary metadata table
"""

from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np

JDS_FEATURES: List[str] = [
    "big_data_skills",
    "maths_stats_skills",
    "coding_skills",
    "ai_and_ml_skills",
    "dashboard_and_storytelling_skills"
]

JDS_REDUCED_FEATURES: List[str] = [
    "maths_stats_skills",
    "dashboard_and_storytelling_skills"
]

JDS_TARGET: str = "salary_hike_high_or_low"


def load_jds_primary(base_dir: Path) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    """
    Loads primary JDS analytical dataset (N=139).
    Returns (X, y, raw_df).
    Enforces strict validation assertions.
    """
    filepath = base_dir / "data" / "processed" / "jds_processed.csv"
    if not filepath.exists():
        raise FileNotFoundError(f"JDS primary dataset missing at {filepath}")
        
    df = pd.read_csv(filepath)
    if len(df) != 139:
        raise ValueError(f"Expected N=139 for JDS primary dataset, got {len(df)}")
        
    assert JDS_TARGET in df.columns, f"Target {JDS_TARGET} missing from dataframe"
    for feat in JDS_FEATURES:
        assert feat in df.columns, f"Feature {feat} missing from dataframe"
        
    y = df[JDS_TARGET].astype(int)
    X = df[JDS_FEATURES].copy().astype(float)
    
    # Assertions
    assert "id" not in X.columns, "Identifier leaked into feature matrix X"
    assert JDS_TARGET not in X.columns, "Target leaked into feature matrix X"
    assert X.isnull().sum().sum() == 0, "Missing values found in feature matrix X"
    assert set(y.unique()) == {0, 1}, f"Unexpected target classes: {set(y.unique())}"
    assert (y == 1).sum() == 73, f"Expected 73 High Hike records, got {(y == 1).sum()}"
    assert (y == 0).sum() == 66, f"Expected 66 Low Hike records, got {(y == 0).sum()}"
    
    return X, y, df


def load_jds_sensitivity(base_dir: Path) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    """
    Loads sensitivity JDS analytical dataset (N=137, ID 3291 excluded).
    Returns (X, y, raw_df).
    """
    filepath = base_dir / "data" / "processed" / "jds_sensitivity_3291_removed.csv"
    if not filepath.exists():
        raise FileNotFoundError(f"JDS sensitivity dataset missing at {filepath}")
        
    df = pd.read_csv(filepath)
    if len(df) != 137:
        raise ValueError(f"Expected N=137 for JDS sensitivity dataset, got {len(df)}")
        
    y = df[JDS_TARGET].astype(int)
    X = df[JDS_FEATURES].copy().astype(float)
    
    assert "id" not in X.columns, "Identifier leaked into feature matrix X"
    assert JDS_TARGET not in X.columns, "Target leaked into feature matrix X"
    assert X.isnull().sum().sum() == 0, "Missing values found in feature matrix X"
    assert (y == 1).sum() == 72, f"Expected 72 High Hike records, got {(y == 1).sum()}"
    assert (y == 0).sum() == 65, f"Expected 65 Low Hike records, got {(y == 0).sum()}"
    
    return X, y, df


def audit_jds_anomalies(df_primary: pd.DataFrame, df_sensitivity: pd.DataFrame) -> Dict[str, object]:
    """
    Audits duplicate ID structure, specifically examining ID 3291 contradictory targets.
    """
    dup_ids = df_primary[df_primary["id"].duplicated(keep=False)]
    dup_id_list = sorted(dup_ids["id"].unique().tolist())
    
    records_3291 = df_primary[df_primary["id"] == 3291]
    identical_features = bool(records_3291[JDS_FEATURES].iloc[0].equals(records_3291[JDS_FEATURES].iloc[1]))
    conflicting_targets = bool(records_3291[JDS_TARGET].nunique() > 1)
    
    return {
        "primary_sample_size": len(df_primary),
        "sensitivity_sample_size": len(df_sensitivity),
        "duplicate_id_count": len(dup_id_list),
        "duplicate_ids": dup_id_list,
        "id_3291_rows": len(records_3291),
        "id_3291_identical_features": identical_features,
        "id_3291_conflicting_targets": conflicting_targets,
        "id_3291_classes_present": sorted(records_3291[JDS_TARGET].tolist()),
        "audit_implication": "ID 3291 has identical skill features but contradictory labels (0 and 1). In primary analysis N=139, both are retained. In sensitivity N=137, both are excluded to verify stability."
    }


def build_dataset_summary_table(df_primary: pd.DataFrame, df_sens: pd.DataFrame) -> pd.DataFrame:
    """Builds Table 1: phase5_dataset_summary.csv."""
    records = [
        {
            "cohort": "JDS Primary Analytical Cohort",
            "source_file": "data/processed/jds_processed.csv",
            "total_records_n": len(df_primary),
            "feature_count_p": len(JDS_FEATURES),
            "target_variable": JDS_TARGET,
            "class_1_high_hike_n": int((df_primary[JDS_TARGET] == 1).sum()),
            "class_1_pct": round(float((df_primary[JDS_TARGET] == 1).mean() * 100), 2),
            "class_0_low_hike_n": int((df_primary[JDS_TARGET] == 0).sum()),
            "class_0_pct": round(float((df_primary[JDS_TARGET] == 0).mean() * 100), 2),
            "missing_values": int(df_primary[JDS_FEATURES].isnull().sum().sum()),
            "id_3291_handling": "Retained (N=139)",
            "primary_role": "Primary candidate model evaluation and benchmarking"
        },
        {
            "cohort": "JDS Sensitivity Cohort",
            "source_file": "data/processed/jds_sensitivity_3291_removed.csv",
            "total_records_n": len(df_sens),
            "feature_count_p": len(JDS_FEATURES),
            "target_variable": JDS_TARGET,
            "class_1_high_hike_n": int((df_sens[JDS_TARGET] == 1).sum()),
            "class_1_pct": round(float((df_sens[JDS_TARGET] == 1).mean() * 100), 2),
            "class_0_low_hike_n": int((df_sens[JDS_TARGET] == 0).sum()),
            "class_0_pct": round(float((df_sens[JDS_TARGET] == 0).mean() * 100), 2),
            "missing_values": int(df_sens[JDS_FEATURES].isnull().sum().sum()),
            "id_3291_handling": "Excluded both conflicting records (N=137)",
            "primary_role": "Out-of-sample robustness and ranking stability verification"
        }
    ]
    return pd.DataFrame(records)
