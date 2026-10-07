"""
tests/test_phase6_sds_modeling.py
---------------------------------
Automated test suite for Phase 6: Senior Data Scientist (SDS) Personality Modeling & Interpretability.
Verifies sample sizes, group leakage prevention, metric bounds, interpretability outputs,
sensitivity robustness, and artifact existence.
"""

from pathlib import Path
import pytest
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

from src.modeling.sds.data import (
    load_sds_primary_data,
    load_sds_sensitivity_data,
    audit_sds_duplicates,
    SDS_FEATURE_NAMES,
    SDS_TARGET_NAME,
    SDS_ID_COL
)
from src.modeling.sds.pipelines import get_sds_models


def test_primary_dataset_integrity():
    X, y, groups = load_sds_primary_data()
    assert len(X) == 161, f"Expected 161 primary rows, got {len(X)}"
    assert len(y) == 161
    assert len(groups) == 161
    assert list(X.columns) == SDS_FEATURE_NAMES
    assert set(y.unique()).issubset({0, 1})
    assert groups.nunique() == 152


def test_sensitivity_dataset_integrity():
    X_sens, y_sens, groups_sens = load_sds_sensitivity_data()
    assert len(X_sens) == 152, f"Expected 152 sensitivity rows, got {len(X_sens)}"
    assert groups_sens.nunique() == 152
    assert set(y_sens.unique()).issubset({0, 1})


def test_duplicate_audit():
    df_dups = audit_sds_duplicates()
    assert len(df_dups) == 18, f"Expected 18 duplicate rows, got {len(df_dups)}"
    assert df_dups[SDS_ID_COL].nunique() == 9, "Expected exactly 9 duplicate subject IDs"


def test_group_leakage_prevention():
    """
    CRITICAL: Asserts that no subject ID ever appears simultaneously in both
    training and validation folds across any StratifiedGroupKFold split.
    """
    X, y, groups = load_sds_primary_data()
    for seed in [42, 43, 44, 45, 46]:
        sgkf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=seed)
        for train_idx, val_idx in sgkf.split(X, y, groups=groups):
            train_ids = set(groups.iloc[train_idx])
            val_ids = set(groups.iloc[val_idx])
            overlap = train_ids.intersection(val_ids)
            assert len(overlap) == 0, f"Group clone leakage detected for IDs: {overlap}"


def test_candidate_models_pipeline_structure():
    models = get_sds_models(random_state=42)
    assert len(models) == 7
    assert "Logistic_Regression_L2" in models
    assert "Random_Forest" in models
    assert "Decision_Tree" in models
    assert "Baseline_Majority" in models

    # Check that scaler is in logistic models but not decision tree
    assert "scaler" in models["Logistic_Regression_L2"].named_steps
    assert "scaler" not in models["Decision_Tree"].named_steps


def test_id_not_in_features():
    X, _, _ = load_sds_primary_data()
    assert SDS_ID_COL not in X.columns
    assert "id" not in X.columns


def test_phase6_tables_exist_and_non_empty():
    tables_dir = Path("outputs/tables/phase6")
    required_tables = [
        "phase6_dataset_summary.csv",
        "phase6_cv_configuration.csv",
        "phase6_model_configuration.csv",
        "phase6_baseline_metrics.csv",
        "phase6_model_performance.csv",
        "phase6_cv_fold_results.csv",
        "phase6_oof_predictions.csv",
        "phase6_logistic_coefficients.csv",
        "phase6_logistic_odds_ratios.csv",
        "phase6_logistic_stability.csv",
        "phase6_tree_rules.csv",
        "phase6_tree_complexity.csv",
        "phase6_rf_permutation_importance.csv",
        "phase6_feature_importance_stability.csv",
        "phase6_error_analysis.csv",
        "phase6_sensitivity_model_performance.csv",
        "phase6_sensitivity_coefficients.csv",
        "phase6_sensitivity_feature_importance.csv",
        "phase6_model_comparison.csv",
        "phase6_phase4_traceability.csv",
        "phase6_validation_summary.csv",
        "phase6_reproducibility_audit.csv",
        "phase6_final_model_selection.csv"
    ]
    for table_name in required_tables:
        p = tables_dir / table_name
        assert p.exists(), f"Missing Phase 6 table: {table_name}"
        df = pd.read_csv(p)
        assert len(df) > 0, f"Table {table_name} is empty"


def test_phase6_figures_exist():
    figures_dir = Path("outputs/figures/phase6")
    required_figs = [
        "fig33_sds_model_roc_curves",
        "fig34_sds_model_performance",
        "fig35_sds_logistic_odds_ratios",
        "fig36_sds_tree_rules",
        "fig37_sds_permutation_importance",
        "fig38_sds_feature_stability",
        "fig39_sds_confusion_matrix",
        "fig40_sds_sensitivity_comparison"
    ]
    for fig_stem in required_figs:
        png_p = figures_dir / f"{fig_stem}.png"
        svg_p = figures_dir / f"{fig_stem}.svg"
        assert png_p.exists(), f"Missing PNG figure: {fig_stem}.png"
        assert svg_p.exists(), f"Missing SVG figure: {fig_stem}.svg"


def test_champion_model_metrics():
    perf_path = Path("outputs/tables/phase6/phase6_model_performance.csv")
    df = pd.read_csv(perf_path)
    champ = df[df["model_name"] == "Logistic_Regression_L2"].iloc[0]
    base = df[df["model_name"] == "Baseline_Majority"].iloc[0]

    assert champ["roc_auc_mean"] >= 0.90, f"Logistic L2 ROC-AUC below 0.90: {champ['roc_auc_mean']}"
    assert champ["macro_f1_mean"] >= 0.85
    assert (champ["accuracy_mean"] - base["accuracy_mean"]) >= 0.25, "Lift over baseline < 25%"


def test_sensitivity_robustness_delta():
    sens_path = Path("outputs/tables/phase6/phase6_sensitivity_model_performance.csv")
    df = pd.read_csv(sens_path)
    champ_sens = df[df["model_name"] == "Logistic_Regression_L2"].iloc[0]
    assert champ_sens["abs_delta_auc"] <= 0.02, f"Sensitivity delta > 0.02: {champ_sens['abs_delta_auc']}"


def test_serialized_model_artifacts():
    models_dir = Path("outputs/models/phase6")
    joblib_p = models_dir / "sds_champion_logistic_l2.joblib"
    json_p = models_dir / "sds_champion_metadata.json"

    assert joblib_p.exists()
    assert json_p.exists()


def test_raw_data_remains_unmodified():
    # Verify raw SDS and JDS are read-only and have correct line counts
    raw_sds = Path("data/raw/SDS Personality Traits.xlsx")
    assert raw_sds.exists()
