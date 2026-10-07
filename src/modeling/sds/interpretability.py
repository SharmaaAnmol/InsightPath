"""
src/modeling/sds/interpretability.py
-----------------------------------
Model interpretability and explainability routines for Senior Data Scientist (SDS) modeling.
Computes standardized odds ratios, coefficient stability, programmatic decision rules,
and out-of-sample permutation feature importance.
"""

from typing import Dict, List, Tuple, Any
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.tree import _tree
from sklearn.base import clone

from src.modeling.sds.pipelines import get_sds_models, SDS_FEATURE_NAMES


def extract_logistic_interpretability(
    X: pd.DataFrame,
    y: pd.Series,
    groups: pd.Series,
    model_key: str = "Logistic_Regression_L2",
    seeds: List[int] = None
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Fits logistic pipeline on full primary cohort and across 25 splits to extract:
    1. Full-sample standardized coefficients and odds ratios
    2. Odds ratios with 95% confidence intervals
    3. Split-by-split coefficient stability metrics
    """
    if seeds is None:
        seeds = [42, 43, 44, 45, 46]

    models = get_sds_models(random_state=42)
    pipeline = models[model_key]

    # Full fit
    pipeline.fit(X, y)
    clf = pipeline.named_steps["clf"]
    coefs_full = clf.coef_[0]
    intercept_full = clf.intercept_[0]

    # Evaluate across 25 splits for empirical standard errors
    from sklearn.model_selection import StratifiedGroupKFold
    split_coefs = {feat: [] for feat in SDS_FEATURE_NAMES}
    split_intercepts = []

    for seed in seeds:
        sgkf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=seed)
        for train_idx, _ in sgkf.split(X, y, groups=groups):
            pipe_clone = clone(pipeline)
            pipe_clone.fit(X.iloc[train_idx], y.iloc[train_idx])
            c = pipe_clone.named_steps["clf"].coef_[0]
            for i, feat in enumerate(SDS_FEATURE_NAMES):
                split_coefs[feat].append(c[i])
            split_intercepts.append(pipe_clone.named_steps["clf"].intercept_[0])

    coef_records = []
    or_records = []
    stability_records = []

    # Intercept
    int_mean = float(np.mean(split_intercepts))
    int_se = float(np.std(split_intercepts, ddof=1))

    coef_records.append({
        "parameter": "Intercept",
        "full_sample_coef": round(float(intercept_full), 4),
        "cv_mean_coef": round(int_mean, 4),
        "cv_std_coef": round(int_se, 4),
        "z_stat": round(int_mean / int_se, 3) if int_se > 0 else np.nan,
        "is_intercept": True
    })

    for i, feat in enumerate(SDS_FEATURE_NAMES):
        b = float(coefs_full[i])
        b_splits = np.array(split_coefs[feat])
        b_mean = float(np.mean(b_splits))
        b_se = float(np.std(b_splits, ddof=1))

        # Standardized Odds Ratio: e^beta
        or_val = float(np.exp(b))
        ci_low = float(np.exp(b - 1.96 * b_se))
        ci_high = float(np.exp(b + 1.96 * b_se))

        coef_records.append({
            "parameter": feat,
            "full_sample_coef": round(b, 4),
            "cv_mean_coef": round(b_mean, 4),
            "cv_std_coef": round(b_se, 4),
            "z_stat": round(b_mean / b_se, 3) if b_se > 0 else np.nan,
            "is_intercept": False
        })

        or_records.append({
            "trait_dimension": feat,
            "standardized_coef_beta": round(b, 4),
            "coef_std_error": round(b_se, 4),
            "adjusted_odds_ratio": round(or_val, 4),
            "or_ci_lower_95": round(ci_low, 4),
            "or_ci_upper_95": round(ci_high, 4),
            "relative_importance_rank": 0  # populated after sorting
        })

        stability_records.append({
            "trait_dimension": feat,
            "mean_coefficient": round(b_mean, 4),
            "std_coefficient": round(b_se, 4),
            "min_coefficient": round(float(np.min(b_splits)), 4),
            "max_coefficient": round(float(np.max(b_splits)), 4),
            "sign_consistency_pct": round(float(np.mean(b_splits > 0) if b_mean > 0 else np.mean(b_splits < 0)) * 100, 1),
            "cv_stability_verdict": "HIGHLY STABLE" if b_se < 0.5 and (np.mean(b_splits > 0) == 1.0 or np.mean(b_splits < 0) == 1.0) else "MODERATELY STABLE"
        })

    coef_df = pd.DataFrame(coef_records)
    or_df = pd.DataFrame(or_records).sort_values("adjusted_odds_ratio", ascending=False).reset_index(drop=True)
    or_df["relative_importance_rank"] = range(1, len(or_df) + 1)
    stability_df = pd.DataFrame(stability_records).sort_values("mean_coefficient", ascending=False).reset_index(drop=True)

    return coef_df, or_df, stability_df


def extract_decision_tree_rules(
    X: pd.DataFrame,
    y: pd.Series,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Fits constrained CART decision tree on full cohort and programmatically extracts readable rules.
    """
    models = get_sds_models(random_state=random_state)
    dt = models["Decision_Tree"]
    dt.fit(X, y)
    clf = dt.named_steps["clf"]

    tree_ = clf.tree_
    feature_names = SDS_FEATURE_NAMES

    rules = []

    def recurse(node, depth, path_conditions):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_names[tree_.feature[node]]
            threshold = tree_.threshold[node]
            # Left child: <= threshold
            recurse(tree_.children_left[node], depth + 1, path_conditions + [f"{name} <= {threshold:.2f}"])
            # Right child: > threshold
            recurse(tree_.children_right[node], depth + 1, path_conditions + [f"{name} > {threshold:.2f}"])
        else:
            # Leaf node
            val = tree_.value[node][0]
            n_samples = int(tree_.n_node_samples[node])
            prob_high = float(val[1] / np.sum(val))
            pred_class = 1 if prob_high >= 0.5 else 0

            rule_text = " AND ".join(path_conditions) if path_conditions else "ROOT (ALL SAMPLES)"
            rules.append({
                "leaf_id": len(rules) + 1,
                "rule_path": rule_text,
                "n_samples": n_samples,
                "samples_low_success": int(val[0]),
                "samples_high_success": int(val[1]),
                "prob_high_success": round(prob_high, 4),
                "predicted_class": pred_class,
                "predicted_label": "High Success" if pred_class == 1 else "Low Success"
            })

    recurse(0, 1, [])
    rules_df = pd.DataFrame(rules)

    complexity_df = pd.DataFrame([{
        "max_depth_configured": 3,
        "actual_depth": clf.get_depth(),
        "total_nodes": clf.tree_.node_count,
        "leaf_nodes": clf.get_n_leaves(),
        "root_split_feature": feature_names[clf.tree_.feature[0]],
        "root_split_threshold": round(float(clf.tree_.threshold[0]), 2),
        "criterion": "gini",
        "min_samples_leaf": 5
    }])

    return rules_df, complexity_df


def compute_permutation_importance_on_held_out(
    X: pd.DataFrame,
    y: pd.Series,
    groups: pd.Series,
    model_key: str = "Random_Forest",
    seeds: List[int] = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Computes permutation feature importance strictly on held-out validation folds across 25 splits.
    """
    if seeds is None:
        seeds = [42, 43, 44, 45, 46]

    from sklearn.model_selection import StratifiedGroupKFold
    models = get_sds_models(random_state=42)
    pipeline = models[model_key]

    importance_runs = {feat: [] for feat in SDS_FEATURE_NAMES}
    rank_runs = {feat: [] for feat in SDS_FEATURE_NAMES}

    for seed in seeds:
        sgkf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=seed)
        for train_idx, val_idx in sgkf.split(X, y, groups=groups):
            pipe_clone = clone(pipeline)
            pipe_clone.fit(X.iloc[train_idx], y.iloc[train_idx])

            # Permutation importance on unseen validation fold
            res = permutation_importance(
                pipe_clone,
                X.iloc[val_idx],
                y.iloc[val_idx],
                scoring="roc_auc",
                n_repeats=5,
                random_state=seed
            )

            fold_means = res.importances_mean
            for i, feat in enumerate(SDS_FEATURE_NAMES):
                importance_runs[feat].append(fold_means[i])

            # Ranks for this split (1 = highest)
            ranks = len(SDS_FEATURE_NAMES) - np.argsort(np.argsort(fold_means))
            for i, feat in enumerate(SDS_FEATURE_NAMES):
                rank_runs[feat].append(ranks[i])

    summary_records = []
    stability_records = []

    for feat in SDS_FEATURE_NAMES:
        vals = np.array(importance_runs[feat])
        ranks = np.array(rank_runs[feat])

        m_imp = float(np.mean(vals))
        s_imp = float(np.std(vals, ddof=1))

        summary_records.append({
            "trait_dimension": feat,
            "mean_permutation_importance": round(m_imp, 4),
            "std_permutation_importance": round(s_imp, 4),
            "min_importance": round(float(np.min(vals)), 4),
            "max_importance": round(float(np.max(vals)), 4),
            "rank": 0
        })

        stability_records.append({
            "trait_dimension": feat,
            "rank_1_pct": round(float(np.mean(ranks == 1)) * 100, 1),
            "rank_2_pct": round(float(np.mean(ranks == 2)) * 100, 1),
            "rank_3_pct": round(float(np.mean(ranks == 3)) * 100, 1),
            "rank_4_pct": round(float(np.mean(ranks == 4)) * 100, 1),
            "rank_5_pct": round(float(np.mean(ranks == 5)) * 100, 1),
            "top_2_frequency_pct": round(float(np.mean(ranks <= 2)) * 100, 1),
            "average_rank": round(float(np.mean(ranks)), 2)
        })

    summary_df = pd.DataFrame(summary_records).sort_values("mean_permutation_importance", ascending=False).reset_index(drop=True)
    summary_df["rank"] = range(1, len(summary_df) + 1)

    stability_df = pd.DataFrame(stability_records).sort_values("top_2_frequency_pct", ascending=False).reset_index(drop=True)

    return summary_df, stability_df
