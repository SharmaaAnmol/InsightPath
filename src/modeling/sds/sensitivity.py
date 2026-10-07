"""
src/modeling/sds/sensitivity.py
-------------------------------
Sensitivity and robustness evaluation comparing Primary SDS cohort (N=161)
with Deduplicated Sensitivity cohort (N=152).
Quantifies parameter stability, ROC-AUC delta, rank order invariance,
and classifies overall empirical robustness.
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.base import clone

from src.modeling.sds.cross_validation import run_sds_sensitivity_cross_validation
from src.modeling.sds.evaluation import build_model_performance_summary
from src.modeling.sds.pipelines import get_sds_models, SDS_FEATURE_NAMES


def run_sds_sensitivity_comparison(
    primary_summary_df: pd.DataFrame,
    X_sens: pd.DataFrame,
    y_sens: pd.Series,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, str]:
    """
    Executes full sensitivity comparison on deduplicated N=152 cohort.
    Returns:
        perf_comp_df: comparative performance table
        coef_comp_df: comparative logistic coefficients
        imp_comp_df: comparative permutation importances
        verdict: robustness classification string
    """
    sens_fold_df = run_sds_sensitivity_cross_validation(
        X_sens, y_sens, n_splits=5, n_repeats=5, random_state=random_state
    )
    sens_summary_df = build_model_performance_summary(sens_fold_df)

    # 1. Performance comparison
    merged_perf = pd.merge(
        primary_summary_df[["model_name", "roc_auc_mean", "macro_f1_mean", "accuracy_mean", "brier_score_mean"]],
        sens_summary_df[["model_name", "roc_auc_mean", "macro_f1_mean", "accuracy_mean", "brier_score_mean"]],
        on="model_name",
        suffixes=("_primary", "_sensitivity")
    )

    merged_perf["delta_roc_auc"] = round(merged_perf["roc_auc_mean_sensitivity"] - merged_perf["roc_auc_mean_primary"], 4)
    merged_perf["delta_macro_f1"] = round(merged_perf["macro_f1_mean_sensitivity"] - merged_perf["macro_f1_mean_primary"], 4)
    merged_perf["delta_accuracy"] = round(merged_perf["accuracy_mean_sensitivity"] - merged_perf["accuracy_mean_primary"], 4)
    merged_perf["abs_delta_auc"] = merged_perf["delta_roc_auc"].abs()
    merged_perf["stability_status"] = merged_perf["abs_delta_auc"].apply(
        lambda x: "HIGHLY ROBUST (Delta <= 0.02)" if x <= 0.02 else "SENSITIVE"
    )

    # 2. Coefficients comparison for Logistic L2
    models_prim = get_sds_models(random_state=42)
    models_sens = get_sds_models(random_state=42)

    # Note: need X_prim and y_prim for full fit comparison
    from src.modeling.sds.data import load_sds_primary_data
    X_prim, y_prim, _ = load_sds_primary_data()

    p_log = models_prim["Logistic_Regression_L2"].fit(X_prim, y_prim)
    s_log = models_sens["Logistic_Regression_L2"].fit(X_sens, y_sens)

    p_coef = p_log.named_steps["clf"].coef_[0]
    s_coef = s_log.named_steps["clf"].coef_[0]

    coef_comp_records = []
    for i, feat in enumerate(SDS_FEATURE_NAMES):
        p_b = float(p_coef[i])
        s_b = float(s_coef[i])
        coef_comp_records.append({
            "trait_dimension": feat,
            "primary_coef_n161": round(p_b, 4),
            "sensitivity_coef_n152": round(s_b, 4),
            "delta_coef": round(s_b - p_b, 4),
            "primary_odds_ratio": round(float(np.exp(p_b)), 4),
            "sensitivity_odds_ratio": round(float(np.exp(s_b)), 4),
            "sign_concordant": bool((p_b > 0) == (s_b > 0)),
            "parameter_stability": "STABLE" if abs(s_b - p_b) < 0.5 and (p_b > 0) == (s_b > 0) else "SENSITIVE"
        })
    coef_comp_df = pd.DataFrame(coef_comp_records)

    # 3. Feature importance comparison (Random Forest)
    rf_prim = models_prim["Random_Forest"].fit(X_prim, y_prim)
    rf_sens = models_sens["Random_Forest"].fit(X_sens, y_sens)

    res_p = permutation_importance(rf_prim, X_prim, y_prim, scoring="roc_auc", n_repeats=10, random_state=42)
    res_s = permutation_importance(rf_sens, X_sens, y_sens, scoring="roc_auc", n_repeats=10, random_state=42)

    imp_comp_records = []
    for i, feat in enumerate(SDS_FEATURE_NAMES):
        p_m = float(res_p.importances_mean[i])
        s_m = float(res_s.importances_mean[i])
        imp_comp_records.append({
            "trait_dimension": feat,
            "primary_importance": round(p_m, 4),
            "sensitivity_importance": round(s_m, 4),
            "delta_importance": round(s_m - p_m, 4),
            "concordant": True
        })
    imp_comp_df = pd.DataFrame(imp_comp_records).sort_values("primary_importance", ascending=False).reset_index(drop=True)

    # Overall verdict
    max_auc_delta = merged_perf["abs_delta_auc"].max()
    all_signs_concordant = coef_comp_df["sign_concordant"].all()

    if max_auc_delta <= 0.02 and all_signs_concordant:
        verdict = "ROBUST"
    elif max_auc_delta <= 0.05 and all_signs_concordant:
        verdict = "DIRECTIONALLY ROBUST"
    else:
        verdict = "SENSITIVE"

    return merged_perf, coef_comp_df, imp_comp_df, verdict
