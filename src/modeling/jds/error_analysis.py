"""
error_analysis.py
------------------
Out-of-fold error analysis for the primary champion model:
  - Aggregates per-sample out-of-fold predictions across 5 cross-validation repeats
  - Classifies records into True Positives, True Negatives, False Positives, False Negatives
  - Diagnoses boundary uncertainty (probabilities in [0.35, 0.65])
  - Computes mean skill profiles across confusion matrix quadrants
  - Generates Table 15: phase5_error_analysis.csv
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd


def run_error_analysis(
    df_oof: pd.DataFrame,
    X: pd.DataFrame,
    y: pd.Series,
    model_name: str = "Logistic_Regression_L2"
) -> Tuple[pd.DataFrame, Dict[str, object]]:
    """
    Executes comprehensive error analysis on out-of-fold predictions.
    Returns:
      1. df_error_summary: skill profiles and error rates by confusion matrix quadrant
      2. diagnostic_meta: high-level error breakdown metrics
    """
    sub = df_oof[df_oof["model_name"] == model_name].copy()
    
    # Aggregate per sample across the 5 validation repeats
    sample_records = []
    for sample_idx, grp in sub.groupby("sample_index"):
        true_c = int(grp["true_class"].iloc[0])
        pred_c = int(pd.Series(grp["predicted_class"]).mode().iloc[0])
        mean_prob = float(grp["predicted_prob_class_1"].mean())
        err_freq = float((grp["is_correct"] == False).sum() / len(grp))
        
        # Quadrant classification
        if true_c == 1 and pred_c == 1:
            quad = "True Positive"
        elif true_c == 0 and pred_c == 0:
            quad = "True Negative"
        elif true_c == 0 and pred_c == 1:
            quad = "False Positive"
        else:
            quad = "False Negative"
            
        boundary = bool(0.35 <= mean_prob <= 0.65)
        
        rec = {
            "sample_index": int(sample_idx),
            "true_class": true_c,
            "predicted_class": pred_c,
            "mean_pred_prob_class_1": round(mean_prob, 4),
            "error_rate_across_repeats": round(err_freq, 2),
            "quadrant": quad,
            "is_boundary_case": boundary
        }
        for feat in X.columns:
            rec[feat] = float(X.loc[sample_idx, feat])
        sample_records.append(rec)
        
    df_samples = pd.DataFrame(sample_records)
    
    # 1. Quadrant summary table (Table 15)
    quad_records = []
    for quad_name in ["True Positive", "True Negative", "False Positive", "False Negative"]:
        q_sub = df_samples[df_samples["quadrant"] == quad_name]
        n_samples = len(q_sub)
        pct_of_cohort = (n_samples / len(df_samples)) * 100
        boundary_pct = (q_sub["is_boundary_case"].sum() / n_samples * 100) if n_samples > 0 else 0.0
        
        row = {
            "quadrant": quad_name,
            "sample_count_n": n_samples,
            "cohort_percentage": round(float(pct_of_cohort), 2),
            "boundary_uncertainty_pct": round(float(boundary_pct), 2),
            "mean_pred_probability": round(float(q_sub["mean_pred_prob_class_1"].mean()), 3) if n_samples > 0 else np.nan
        }
        for feat in X.columns:
            clean_feat = feat.replace("_skills", "").replace("_", " ").title()
            row[f"mean_{clean_feat.lower()}"] = round(float(q_sub[feat].mean()), 2) if n_samples > 0 else np.nan
            
        quad_records.append(row)
        
    df_error_summary = pd.DataFrame(quad_records)
    
    # 2. Diagnostic metadata
    total_err = len(df_samples[df_samples["quadrant"].isin(["False Positive", "False Negative"])])
    meta = {
        "model_name": model_name,
        "total_samples": len(df_samples),
        "total_misclassified": total_err,
        "overall_error_rate_pct": round(float(total_err / len(df_samples) * 100), 2),
        "false_positive_count": int((df_samples["quadrant"] == "False Positive").sum()),
        "false_negative_count": int((df_samples["quadrant"] == "False Negative").sum()),
        "boundary_cases_count": int(df_samples["is_boundary_case"].sum()),
        "boundary_cases_pct": round(float(df_samples["is_boundary_case"].sum() / len(df_samples) * 100), 2)
    }
    
    return df_error_summary, meta
