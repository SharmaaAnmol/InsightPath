"""
cross_validation.py
-------------------
Implements Repeated Stratified K-Fold cross-validation (5 folds x 5 repeats = 25 splits):
  - Strictly leakage-free evaluation: all pipelines fitted exclusively on training folds
  - Generation of split-level performance metrics across all candidate models
  - Accumulation of out-of-fold predictions
  - Calculation of mean, std, min, max, and CV uncertainty intervals
"""

import time
from typing import Dict, List, Tuple, Any
import numpy as np
import pandas as pd
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import (
    roc_auc_score,
    f1_score,
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    log_loss,
    brier_score_loss
)
from sklearn.base import clone


def build_cv_configuration_table(n_splits: int = 5, n_repeats: int = 5, random_state: int = 42) -> pd.DataFrame:
    """Builds Table 2: phase5_cv_configuration.csv."""
    records = [{
        "cv_strategy": "Repeated Stratified K-Fold Cross-Validation",
        "num_folds_k": n_splits,
        "num_repeats_r": n_repeats,
        "total_validation_splits": n_splits * n_repeats,
        "random_state": random_state,
        "stratification_target": "salary_hike_high_or_low",
        "approx_train_fold_n": 111,
        "approx_val_fold_n": 28,
        "leakage_guardrail": "Preprocessing (StandardScaler) strictly encapsulated inside Pipeline",
        "uncertainty_reporting": "Mean, Std, Min, Max, and 95% CV Confidence Interval across 25 splits"
    }]
    return pd.DataFrame(records)


def evaluate_pipelines_cv(
    pipelines: Dict[str, Any],
    X: pd.DataFrame,
    y: pd.Series,
    n_splits: int = 5,
    n_repeats: int = 5,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Executes Repeated Stratified K-Fold CV across all provided pipelines.
    Returns:
      1. cv_fold_results_df: split-by-split metrics (25 rows per model)
      2. oof_predictions_df: out-of-fold predictions
      3. cv_summary_df: aggregated mean/std/ci metrics table
    """
    rskf = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=random_state)
    
    fold_records = []
    oof_records = []
    
    for model_name, pipe in pipelines.items():
        t0_model = time.time()
        split_idx = 0
        
        for repeat_idx in range(n_repeats):
            for fold_idx in range(n_splits):
                # Fetch indices for this specific split
                # Using rskf.split generator
                pass
                
    # Re-iterate cleanly through splits generator
    splits_list = list(rskf.split(X, y))
    assert len(splits_list) == n_splits * n_repeats, f"Expected {n_splits*n_repeats} splits"
    
    for model_name, pipe in pipelines.items():
        t0_fit = time.time()
        
        for split_id, (train_idx, val_idx) in enumerate(splits_list):
            rep_id = split_id // n_splits
            fold_id = split_id % n_splits
            
            X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
            X_val, y_val = X.iloc[val_idx], y.iloc[val_idx]
            
            # Clone pipeline to ensure clean slate per fold
            clf = clone(pipe)
            t_start = time.time()
            clf.fit(X_train, y_train)
            fit_time = time.time() - t_start
            
            # Predictions
            y_pred = clf.predict(X_val)
            
            # Probabilities (or dummy for baseline)
            if hasattr(clf, "predict_proba"):
                y_prob = clf.predict_proba(X_val)[:, 1]
            else:
                y_prob = np.full(len(y_val), float(y_train.mean()))
                
            # Compute evaluation metrics
            # For baseline majority, ROC-AUC is exactly 0.5
            if model_name == "Baseline_Majority":
                auc = 0.500
                ll = log_loss(y_val, np.column_stack([1 - y_prob, y_prob]), labels=[0, 1])
            else:
                auc = roc_auc_score(y_val, y_prob)
                # Clip probabilities for stable log loss
                y_prob_clipped = np.clip(y_prob, 1e-15, 1 - 1e-15)
                ll = log_loss(y_val, np.column_stack([1 - y_prob_clipped, y_prob_clipped]), labels=[0, 1])
                
            f1_macro = f1_score(y_val, y_pred, average="macro", zero_division=0)
            bal_acc = balanced_accuracy_score(y_val, y_pred)
            acc = accuracy_score(y_val, y_pred)
            prec = precision_score(y_val, y_pred, zero_division=0)
            rec = recall_score(y_val, y_pred, zero_division=0)
            brier = brier_score_loss(y_val, y_prob)
            
            fold_records.append({
                "model_name": model_name,
                "split_id": split_id,
                "repeat_id": rep_id,
                "fold_id": fold_id,
                "train_n": len(train_idx),
                "val_n": len(val_idx),
                "roc_auc": round(float(auc), 4),
                "macro_f1": round(float(f1_macro), 4),
                "balanced_accuracy": round(float(bal_acc), 4),
                "accuracy": round(float(acc), 4),
                "precision": round(float(prec), 4),
                "recall": round(float(rec), 4),
                "log_loss": round(float(ll), 4),
                "brier_score": round(float(brier), 4),
                "fit_time_sec": round(float(fit_time), 4)
            })
            
            # Record out-of-fold predictions
            for idx_in_val, orig_row_idx in enumerate(val_idx):
                oof_records.append({
                    "model_name": model_name,
                    "split_id": split_id,
                    "repeat_id": rep_id,
                    "fold_id": fold_id,
                    "sample_index": int(orig_row_idx),
                    "true_class": int(y_val.iloc[idx_in_val]),
                    "predicted_class": int(y_pred[idx_in_val]),
                    "predicted_prob_class_1": round(float(y_prob[idx_in_val]), 4),
                    "is_correct": bool(y_val.iloc[idx_in_val] == y_pred[idx_in_val])
                })
                
    df_folds = pd.DataFrame(fold_records)
    df_oof = pd.DataFrame(oof_records)
    
    # Summary aggregation
    summary_records = []
    for model_name, grp in df_folds.groupby("model_name", sort=False):
        n_splits_eval = len(grp)
        auc_m = grp["roc_auc"].mean()
        auc_s = grp["roc_auc"].std()
        f1_m = grp["macro_f1"].mean()
        f1_s = grp["macro_f1"].std()
        
        # 95% CV confidence interval for the mean: mean +/- 1.96 * (std / sqrt(25))
        ci_auc_low = auc_m - 1.96 * (auc_s / np.sqrt(n_splits_eval))
        ci_auc_high = auc_m + 1.96 * (auc_s / np.sqrt(n_splits_eval))
        
        summary_records.append({
            "model_name": model_name,
            "validation_splits_n": n_splits_eval,
            "roc_auc_mean": round(float(auc_m), 4),
            "roc_auc_std": round(float(auc_s), 4),
            "roc_auc_ci_lower": round(float(ci_auc_low), 4),
            "roc_auc_ci_upper": round(float(ci_auc_high), 4),
            "roc_auc_min": round(float(grp["roc_auc"].min()), 4),
            "roc_auc_max": round(float(grp["roc_auc"].max()), 4),
            "macro_f1_mean": round(float(f1_m), 4),
            "macro_f1_std": round(float(f1_s), 4),
            "balanced_accuracy_mean": round(float(grp["balanced_accuracy"].mean()), 4),
            "balanced_accuracy_std": round(float(grp["balanced_accuracy"].std()), 4),
            "accuracy_mean": round(float(grp["accuracy"].mean()), 4),
            "accuracy_std": round(float(grp["accuracy"].std()), 4),
            "precision_mean": round(float(grp["precision"].mean()), 4),
            "recall_mean": round(float(grp["recall"].mean()), 4),
            "log_loss_mean": round(float(grp["log_loss"].mean()), 4),
            "brier_score_mean": round(float(grp["brier_score"].mean()), 4)
        })
        
    df_summary = pd.DataFrame(summary_records)
    # Sort by ROC-AUC mean descending
    df_summary = df_summary.sort_values(by="roc_auc_mean", ascending=False).reset_index(drop=True)
    
    return df_folds, df_oof, df_summary
