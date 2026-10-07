"""
src/modeling/sds/evaluation.py
------------------------------
Model performance aggregation, scorecard compilation, and baseline lift analysis
for Senior Data Scientist (SDS) personality classification.
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import confusion_matrix, classification_report


def build_model_performance_summary(fold_results_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates fold-level metrics across all 25 splits into a comprehensive performance table.
    """
    records = []
    models = fold_results_df["model_name"].unique()

    for model_name in models:
        sub = fold_results_df[fold_results_df["model_name"] == model_name]
        n_splits = len(sub)

        auc_vals = sub["roc_auc"].values
        auc_mean = float(np.mean(auc_vals))
        auc_std = float(np.std(auc_vals, ddof=1)) if n_splits > 1 else 0.0
        auc_se = auc_std / np.sqrt(n_splits) if n_splits > 1 else 0.0
        ci_lower = max(0.0, auc_mean - 1.96 * auc_se)
        ci_upper = min(1.0, auc_mean + 1.96 * auc_se)

        f1_vals = sub["macro_f1"].values
        bal_acc_vals = sub["balanced_accuracy"].values
        acc_vals = sub["accuracy"].values
        prec_vals = sub["precision"].values
        rec_vals = sub["recall"].values
        loss_vals = sub["log_loss"].dropna().values
        brier_vals = sub["brier_score"].values

        records.append({
            "model_name": model_name,
            "validation_splits_n": n_splits,
            "roc_auc_mean": round(auc_mean, 4),
            "roc_auc_std": round(auc_std, 4),
            "roc_auc_ci_lower": round(ci_lower, 4),
            "roc_auc_ci_upper": round(ci_upper, 4),
            "roc_auc_min": round(float(np.min(auc_vals)), 4),
            "roc_auc_max": round(float(np.max(auc_vals)), 4),
            "macro_f1_mean": round(float(np.mean(f1_vals)), 4),
            "macro_f1_std": round(float(np.std(f1_vals, ddof=1)), 4) if n_splits > 1 else 0.0,
            "balanced_accuracy_mean": round(float(np.mean(bal_acc_vals)), 4),
            "balanced_accuracy_std": round(float(np.std(bal_acc_vals, ddof=1)), 4) if n_splits > 1 else 0.0,
            "accuracy_mean": round(float(np.mean(acc_vals)), 4),
            "accuracy_std": round(float(np.std(acc_vals, ddof=1)), 4) if n_splits > 1 else 0.0,
            "precision_mean": round(float(np.mean(prec_vals)), 4),
            "recall_mean": round(float(np.mean(rec_vals)), 4),
            "log_loss_mean": round(float(np.mean(loss_vals)), 4) if len(loss_vals) > 0 else np.nan,
            "brier_score_mean": round(float(np.mean(brier_vals)), 4)
        })

    summary_df = pd.DataFrame(records).sort_values("roc_auc_mean", ascending=False).reset_index(drop=True)
    return summary_df


def build_model_comparison_table(perf_df: pd.DataFrame, champion_name: str) -> pd.DataFrame:
    """
    Constructs head-to-head comparison against Baseline and Champion.
    """
    baseline_row = perf_df[perf_df["model_name"] == "Baseline_Majority"].iloc[0]
    champ_row = perf_df[perf_df["model_name"] == champion_name].iloc[0]

    records = []
    for _, row in perf_df.iterrows():
        m_name = row["model_name"]
        lift_acc = (row["accuracy_mean"] - baseline_row["accuracy_mean"]) * 100
        auc_delta = row["roc_auc_mean"] - baseline_row["roc_auc_mean"]
        delta_to_champ = row["roc_auc_mean"] - champ_row["roc_auc_mean"]

        records.append({
            "model_name": m_name,
            "roc_auc_mean": row["roc_auc_mean"],
            "roc_auc_95_ci": f"[{row['roc_auc_ci_lower']}, {row['roc_auc_ci_upper']}]",
            "macro_f1_mean": row["macro_f1_mean"],
            "accuracy_pct": round(row["accuracy_mean"] * 100, 2),
            "accuracy_lift_vs_baseline_pct": round(lift_acc, 2),
            "roc_auc_gain_vs_baseline": round(auc_delta, 4),
            "roc_auc_delta_vs_champion": round(delta_to_champ, 4),
            "brier_score": row["brier_score_mean"],
            "is_champion": bool(m_name == champion_name)
        })

    return pd.DataFrame(records)


def compute_oof_confusion_matrix(
    oof_predictions_df: pd.DataFrame,
    model_name: str
) -> Tuple[np.ndarray, Dict[str, float]]:
    """
    Calculates aggregated confusion matrix and classification metrics from out-of-fold predictions.
    """
    sub = oof_predictions_df[oof_predictions_df["model_name"] == model_name]
    cm = confusion_matrix(sub["true_label"], sub["pred_class"])

    tn, fp, fn, tp = cm.ravel()
    total = len(sub)

    stats_dict = {
        "total_evaluations": total,
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
        "tn_pct": round(tn / total * 100, 2),
        "fp_pct": round(fp / total * 100, 2),
        "fn_pct": round(fn / total * 100, 2),
        "tp_pct": round(tp / total * 100, 2),
        "overall_accuracy_pct": round((tp + tn) / total * 100, 2)
    }

    return cm, stats_dict
