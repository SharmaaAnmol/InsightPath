"""
src/modeling/sds/cross_validation.py
-----------------------------------
Leakage-safe cross-validation runner for Senior Data Scientist (SDS) modeling.
Implements StratifiedGroupKFold on subject IDs (N=161) to guarantee that
duplicated subject records never span training and validation splits.
"""

from typing import Dict, List, Tuple, Any
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold, RepeatedStratifiedKFold
from sklearn.metrics import (
    roc_auc_score,
    f1_score,
    balanced_accuracy_score,
    accuracy_score,
    precision_score,
    recall_score,
    log_loss,
    brier_score_loss
)
from sklearn.base import clone

from src.modeling.sds.pipelines import get_sds_models, SDS_FEATURE_NAMES


def evaluate_split_metrics(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    y_pred: np.ndarray
) -> Dict[str, float]:
    """
    Computes all 8 required validation metrics for a single evaluation split.
    """
    # Safe clipping for log_loss
    y_prob_clipped = np.clip(y_prob, 1e-15, 1 - 1e-15)

    # ROC AUC handles single-class edge cases gracefully
    try:
        auc = float(roc_auc_score(y_true, y_prob))
    except ValueError:
        auc = 0.5

    macro_f1 = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
    bal_acc = float(balanced_accuracy_score(y_true, y_pred))
    acc = float(accuracy_score(y_true, y_pred))
    prec = float(precision_score(y_true, y_pred, zero_division=0))
    rec = float(recall_score(y_true, y_pred, zero_division=0))

    try:
        loss = float(log_loss(y_true, y_prob_clipped))
    except Exception:
        loss = np.nan

    brier = float(brier_score_loss(y_true, y_prob))

    return {
        "roc_auc": round(auc, 4),
        "macro_f1": round(macro_f1, 4),
        "balanced_accuracy": round(bal_acc, 4),
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "log_loss": round(loss, 4),
        "brier_score": round(brier, 4)
    }


def run_sds_grouped_cross_validation(
    X: pd.DataFrame,
    y: pd.Series,
    groups: pd.Series,
    n_splits: int = 5,
    seeds: List[int] = None
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, List[Dict[str, float]]]]:
    """
    Executes 5-fold x 5-repeat StratifiedGroupKFold evaluation on primary SDS data (N=161).
    Groups strictly by subject ID.
    Returns:
        fold_results_df: split-level metrics (175 rows: 7 models x 25 splits)
        oof_predictions_df: out-of-fold probability predictions
        raw_metrics: raw metric dictionaries by model
    """
    if seeds is None:
        seeds = [42, 43, 44, 45, 46]

    models = get_sds_models(random_state=42)
    fold_records = []
    oof_records = []
    raw_metrics = {m_name: [] for m_name in models.keys()}

    for repeat_idx, seed in enumerate(seeds):
        sgkf = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)

        for fold_idx, (train_idx, val_idx) in enumerate(sgkf.split(X, y, groups=groups)):
            # Integrity assertion: zero subject ID intersection
            train_ids = set(groups.iloc[train_idx])
            val_ids = set(groups.iloc[val_idx])
            overlap = train_ids.intersection(val_ids)
            assert len(overlap) == 0, f"Critical leakage! IDs in both train and val: {overlap}"

            X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
            X_val, y_val = X.iloc[val_idx], y.iloc[val_idx]
            val_ids_series = groups.iloc[val_idx]

            split_id = repeat_idx * n_splits + fold_idx + 1

            for model_name, pipeline in models.items():
                model_clone = clone(pipeline)
                model_clone.fit(X_train, y_train)

                if hasattr(model_clone, "predict_proba"):
                    probs = model_clone.predict_proba(X_val)[:, 1]
                else:
                    probs = model_clone.predict(X_val).astype(float)

                preds = model_clone.predict(X_val)

                # Compute metrics
                metrics = evaluate_split_metrics(y_val.values, probs, preds)
                raw_metrics[model_name].append(metrics)

                fold_records.append({
                    "model_name": model_name,
                    "repeat_idx": repeat_idx + 1,
                    "fold_idx": fold_idx + 1,
                    "split_id": split_id,
                    "seed": seed,
                    "val_sample_size": len(y_val),
                    "val_class1_ratio": round(float(y_val.mean()), 4),
                    **metrics
                })

                for i in range(len(y_val)):
                    oof_records.append({
                        "model_name": model_name,
                        "repeat_idx": repeat_idx + 1,
                        "fold_idx": fold_idx + 1,
                        "split_id": split_id,
                        "subject_id": val_ids_series.iloc[i],
                        "true_label": int(y_val.iloc[i]),
                        "pred_prob": round(float(probs[i]), 4),
                        "pred_class": int(preds[i])
                    })

    fold_results_df = pd.DataFrame(fold_records)
    oof_predictions_df = pd.DataFrame(oof_records)

    return fold_results_df, oof_predictions_df, raw_metrics


def run_sds_sensitivity_cross_validation(
    X_sens: pd.DataFrame,
    y_sens: pd.Series,
    n_splits: int = 5,
    n_repeats: int = 5,
    random_state: int = 42
) -> pd.DataFrame:
    """
    Executes RepeatedStratifiedKFold evaluation on deduplicated SDS cohort (N=152).
    """
    models = get_sds_models(random_state=random_state)
    rskf = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=random_state)

    records = []
    for split_idx, (train_idx, val_idx) in enumerate(rskf.split(X_sens, y_sens)):
        X_train, y_train = X_sens.iloc[train_idx], y_sens.iloc[train_idx]
        X_val, y_val = X_sens.iloc[val_idx], y_sens.iloc[val_idx]

        for model_name, pipeline in models.items():
            model_clone = clone(pipeline)
            model_clone.fit(X_train, y_train)

            if hasattr(model_clone, "predict_proba"):
                probs = model_clone.predict_proba(X_val)[:, 1]
            else:
                probs = model_clone.predict(X_val).astype(float)

            preds = model_clone.predict(X_val)
            metrics = evaluate_split_metrics(y_val.values, probs, preds)

            records.append({
                "model_name": model_name,
                "split_id": split_idx + 1,
                **metrics
            })

    return pd.DataFrame(records)
