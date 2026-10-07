"""
src/modeling/sds/error_analysis.py
----------------------------------
Error analysis and prediction uncertainty profiling for Senior Data Scientist (SDS) modeling.
Categorizes predictions into confusion matrix quadrants and evaluates boundary uncertainty.
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd

from src.modeling.sds.pipelines import SDS_FEATURE_NAMES


def run_sds_error_analysis(
    oof_predictions_df: pd.DataFrame,
    X: pd.DataFrame,
    groups: pd.Series,
    model_name: str = "Logistic_Regression_L2"
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Analyzes prediction errors, boundary uncertainty, and trait profiles of misclassified cases.
    """
    sub = oof_predictions_df[oof_predictions_df["model_name"] == model_name].copy()

    # Map back trait features using index or subject_id
    # Create an identifier-to-traits map
    id_map = X.copy()
    id_map["id"] = groups
    id_lookup = id_map.groupby("id")[SDS_FEATURE_NAMES].mean().to_dict(orient="index")

    for feat in SDS_FEATURE_NAMES:
        sub[feat] = sub["subject_id"].apply(lambda sid: id_lookup[sid][feat] if sid in id_lookup else np.nan)

    # Classify quadrants
    def get_quadrant(row):
        t, p = row["true_label"], row["pred_class"]
        if t == 1 and p == 1:
            return "True Positive (High Success correctly predicted)"
        elif t == 0 and p == 0:
            return "True Negative (Low Success correctly predicted)"
        elif t == 0 and p == 1:
            return "False Positive (Low Success predicted High)"
        else:
            return "False Negative (High Success predicted Low)"

    sub["error_quadrant"] = sub.apply(get_quadrant, axis=1)
    sub["is_error"] = sub["true_label"] != sub["pred_class"]
    sub["is_uncertain"] = (sub["pred_prob"] >= 0.35) & (sub["pred_prob"] <= 0.65)

    total_n = len(sub)
    total_errors = int(sub["is_error"].sum())
    total_uncertain = int(sub["is_uncertain"].sum())
    errors_in_uncertain = int((sub["is_error"] & sub["is_uncertain"]).sum())

    # Summary table
    quad_counts = sub["error_quadrant"].value_counts()
    records = []
    for quad_name, count in quad_counts.items():
        records.append({
            "quadrant": quad_name,
            "prediction_count": int(count),
            "percentage_of_total": round(count / total_n * 100, 2),
            "is_misclassification": bool("False" in quad_name)
        })

    # Add uncertainty metrics
    records.append({
        "quadrant": "Boundary Uncertainty (0.35 <= P <= 0.65)",
        "prediction_count": total_uncertain,
        "percentage_of_total": round(total_uncertain / total_n * 100, 2),
        "is_misclassification": False
    })
    records.append({
        "quadrant": "Misclassifications inside Uncertainty Zone",
        "prediction_count": errors_in_uncertain,
        "percentage_of_total": round(errors_in_uncertain / total_errors * 100, 2) if total_errors > 0 else 0.0,
        "is_misclassification": True
    })

    summary_df = pd.DataFrame(records)

    # Trait profile by quadrant
    profile_df = sub.groupby("error_quadrant")[SDS_FEATURE_NAMES].mean().round(2).reset_index()

    return summary_df, profile_df
