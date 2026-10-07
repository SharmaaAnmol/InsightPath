"""
src/modeling/sds/data.py
------------------------
Data ingestion and validation module for Senior Data Scientist (SDS) personality modeling.
Handles primary cohort (N=161) and deduplicated sensitivity cohort (N=152).
Strictly enforces group-aware tracking of subject IDs for leakage prevention.
"""

from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np

SDS_FEATURE_NAMES = [
    "neuroticism",
    "extraversion",
    "openness_to_experience",
    "agreeableness",
    "conscientiousness"
]

SDS_TARGET_NAME = "success_classification_high_low"
SDS_ID_COL = "id"


def load_sds_primary_data(data_path: str = "data/processed/sds_processed.csv") -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
    """
    Loads primary SDS processed dataset (N=161).
    Returns:
        X: pd.DataFrame of 5 Big Five personality features
        y: pd.Series of binary target (1 = High Success, 0 = Low Success)
        groups: pd.Series of subject IDs for GroupKFold splitting
    """
    path = Path(data_path)
    if not path.exists():
        raise FileNotFoundError(f"Primary SDS data not found at: {path}")

    df = pd.read_csv(path)

    # Validations
    assert len(df) == 161, f"Expected 161 rows for primary SDS, got {len(df)}"
    assert SDS_TARGET_NAME in df.columns, f"Target '{SDS_TARGET_NAME}' not found in dataset"
    assert SDS_ID_COL in df.columns, f"ID column '{SDS_ID_COL}' not found in dataset"
    for col in SDS_FEATURE_NAMES:
        assert col in df.columns, f"Feature '{col}' not found in dataset"

    # Check missingness
    assert df[SDS_FEATURE_NAMES + [SDS_TARGET_NAME, SDS_ID_COL]].isna().sum().sum() == 0, (
        "Unexpected missing values in SDS primary dataset"
    )

    # Check trait bounds [17, 68]
    for col in SDS_FEATURE_NAMES:
        assert df[col].min() >= 17.0, f"Trait {col} has values < 17.0"
        assert df[col].max() <= 68.0, f"Trait {col} has values > 68.0"

    # Check target domain {0, 1}
    target_vals = set(df[SDS_TARGET_NAME].unique())
    assert target_vals.issubset({0, 1}), f"Unexpected target classes: {target_vals}"

    X = df[SDS_FEATURE_NAMES].copy()
    y = df[SDS_TARGET_NAME].copy()
    groups = df[SDS_ID_COL].copy()

    return X, y, groups


def load_sds_sensitivity_data(
    data_path: str = "data/processed/sds_sensitivity_deduplicated.csv",
    fallback_primary: str = "data/processed/sds_processed.csv"
) -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
    """
    Loads deduplicated sensitivity SDS dataset (N=152).
    If file doesn't exist, derives it from primary by dropping duplicate IDs.
    Returns:
        X: pd.DataFrame of 5 Big Five personality features
        y: pd.Series of binary target
        groups: pd.Series of unique subject IDs
    """
    path = Path(data_path)
    if path.exists():
        df = pd.read_csv(path)
    else:
        df_prim = pd.read_csv(fallback_primary)
        df = df_prim.drop_duplicates(subset=[SDS_ID_COL], keep="first").copy()
        df.to_csv(path, index=False)

    assert len(df) == 152, f"Expected 152 rows for deduplicated SDS, got {len(df)}"
    assert df[SDS_ID_COL].nunique() == 152, "Duplicate IDs still present in sensitivity cohort"

    X = df[SDS_FEATURE_NAMES].copy()
    y = df[SDS_TARGET_NAME].copy()
    groups = df[SDS_ID_COL].copy()

    return X, y, groups


def audit_sds_duplicates(data_path: str = "data/processed/sds_processed.csv") -> pd.DataFrame:
    """
    Audits the exact 9 duplicate subject IDs (18 rows) in the SDS primary dataset.
    """
    df = pd.read_csv(data_path)
    dup_mask = df.duplicated(subset=[SDS_ID_COL], keep=False)
    df_dups = df[dup_mask].sort_values(SDS_ID_COL).copy()
    return df_dups
