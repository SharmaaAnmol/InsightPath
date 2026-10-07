"""
interpretability.py
-------------------
Extracts interpretability and explainability artifacts for JDS skill models:
  - Standardized logistic regression coefficients and odds ratios
  - Coefficient stability across repeated cross-validation splits
  - Programmatic Decision Tree rule extraction (IF-THEN human-readable paths)
  - Validation-set permutation feature importance for Random Forest
  - Cross-validation feature ranking stability diagnostics
"""

from typing import Dict, List, Tuple, Any
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, _tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


def extract_logistic_interpretability(
    X: pd.DataFrame,
    y: pd.Series,
    n_splits: int = 5,
    n_repeats: int = 5,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Computes logistic regression coefficients, odds ratios, and stability across 25 CV splits.
    Returns:
      1. df_coef: full model standardized coefficients
      2. df_or: standardized odds ratios
      3. df_stability: split-by-split coefficient stability
    """
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(l1_ratio=0.0, solver="lbfgs", C=1.0, max_iter=1000, random_state=random_state))
    ])
    pipe.fit(X, y)
    
    clf = pipe.named_steps["clf"]
    scaler = pipe.named_steps["scaler"]
    
    coefs = clf.coef_[0]
    intercept = clf.intercept_[0]
    odds_ratios = np.exp(coefs)
    
    # 1. Full model coefficient table
    coef_records = []
    for feat, b, or_val in zip(X.columns, coefs, odds_ratios):
        clean_name = feat.replace("_skills", "").replace("_", " ").title()
        coef_records.append({
            "feature": feat,
            "feature_label": clean_name,
            "standardized_coef_beta": round(float(b), 4),
            "odds_ratio": round(float(or_val), 3),
            "direction": "Positive association" if b > 0 else "Negative association",
            "relative_importance_rank": 0  # To be filled
        })
    df_coef = pd.DataFrame(coef_records).sort_values(by="standardized_coef_beta", ascending=False).reset_index(drop=True)
    df_coef["relative_importance_rank"] = range(1, len(df_coef) + 1)
    
    # 2. Odds Ratios table
    df_or = df_coef[["feature", "feature_label", "odds_ratio", "standardized_coef_beta", "direction", "relative_importance_rank"]].copy()
    
    # 3. Repeated CV coefficient stability
    rskf = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=random_state)
    split_coefs = {feat: [] for feat in X.columns}
    
    for train_idx, _ in rskf.split(X, y):
        X_tr, y_tr = X.iloc[train_idx], y.iloc[train_idx]
        fold_pipe = clone(pipe)
        fold_pipe.fit(X_tr, y_tr)
        f_clf = fold_pipe.named_steps["clf"]
        for feat, b in zip(X.columns, f_clf.coef_[0]):
            split_coefs[feat].append(float(b))
            
    stab_records = []
    for feat in X.columns:
        arr = np.array(split_coefs[feat])
        mean_b = float(arr.mean())
        std_b = float(arr.std())
        # 95% CV confidence interval
        ci_l = mean_b - 1.96 * (std_b / np.sqrt(len(arr)))
        ci_u = mean_b + 1.96 * (std_b / np.sqrt(len(arr)))
        sign_consistent_pct = float((arr > 0).sum() / len(arr) * 100) if mean_b > 0 else float((arr < 0).sum() / len(arr) * 100)
        
        stab_records.append({
            "feature": feat,
            "feature_label": feat.replace("_skills", "").replace("_", " ").title(),
            "cv_splits_n": len(arr),
            "mean_coef_beta": round(mean_b, 4),
            "std_coef_beta": round(std_b, 4),
            "ci_95_lower": round(ci_l, 4),
            "ci_95_upper": round(ci_u, 4),
            "mean_odds_ratio": round(float(np.exp(mean_b)), 3),
            "min_coef_beta": round(float(arr.min()), 4),
            "max_coef_beta": round(float(arr.max()), 4),
            "sign_consistency_pct": round(sign_consistent_pct, 1),
            "stability_status": "STABLE" if sign_consistent_pct >= 95.0 else "MODERATE"
        })
        
    df_stability = pd.DataFrame(stab_records).sort_values(by="mean_coef_beta", ascending=False).reset_index(drop=True)
    return df_coef, df_or, df_stability


def extract_tree_rules(X: pd.DataFrame, y: pd.Series, max_depth: int = 3, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Fits Decision Tree and programmatically extracts human-readable IF-THEN rules and complexity metrics.
    """
    tree_clf = DecisionTreeClassifier(
        max_depth=max_depth,
        min_samples_leaf=5,
        criterion="gini",
        random_state=random_state
    )
    tree_clf.fit(X, y)
    
    # 1. Complexity metadata
    df_complexity = pd.DataFrame([{
        "algorithm": "CART Decision Tree Classifier",
        "criterion": "gini",
        "max_depth_constraint": max_depth,
        "actual_depth": tree_clf.get_depth(),
        "total_nodes": tree_clf.tree_.node_count,
        "leaf_nodes_n": tree_clf.get_n_leaves(),
        "min_samples_leaf": 5,
        "total_training_samples": len(X),
        "interpretability_assessment": "Fully transparent human-readable rule set"
    }])
    
    # 2. Extract rules programmatically
    tree_ = tree_clf.tree_
    feature_name = [
        X.columns[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    
    rule_records = []
    
    def recurse(node, path_rules):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            clean_name = name.replace("_skills", "").replace("_", " ").title()
            threshold = round(float(tree_.threshold[node]), 2)
            
            # Left child: <= threshold
            recurse(tree_.children_left[node], path_rules + [f"{clean_name} <= {threshold}"])
            # Right child: > threshold
            recurse(tree_.children_right[node], path_rules + [f"{clean_name} > {threshold}"])
        else:
            # Leaf node
            samples = int(tree_.n_node_samples[node])
            val = tree_.value[node][0]
            prob_0 = val[0] / samples
            prob_1 = val[1] / samples
            pred_class = int(np.argmax(val))
            
            rule_str = " AND ".join(path_rules) if path_rules else "Root (Unconditional)"
            rule_records.append({
                "rule_id": f"Rule_{len(rule_records)+1}",
                "decision_path": rule_str,
                "predicted_class": pred_class,
                "outcome_label": "High Hike (Y=1)" if pred_class == 1 else "Low Hike (Y=0)",
                "leaf_samples_n": samples,
                "prob_high_hike": round(float(prob_1), 3),
                "prob_low_hike": round(float(prob_0), 3)
            })
            
    recurse(0, [])
    df_rules = pd.DataFrame(rule_records)
    return df_rules, df_complexity


def compute_validation_permutation_importance(
    X: pd.DataFrame,
    y: pd.Series,
    n_splits: int = 5,
    n_repeats: int = 5,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Computes permutation feature importance on held-out validation folds across 25 CV splits.
    Returns:
      1. df_rf_perm: summary permutation importance for Random Forest
      2. df_stability: feature rank stability across all 25 splits
    """
    rskf = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=random_state)
    
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=3,
        min_samples_leaf=4,
        max_features="sqrt",
        random_state=random_state
    )
    
    split_importances = {feat: [] for feat in X.columns}
    rank_occurrences = {feat: [] for feat in X.columns}
    
    for split_idx, (train_idx, val_idx) in enumerate(rskf.split(X, y)):
        X_tr, y_tr = X.iloc[train_idx], y.iloc[train_idx]
        X_v, y_v = X.iloc[val_idx], y.iloc[val_idx]
        
        clf = clone(rf)
        clf.fit(X_tr, y_tr)
        
        # Calculate permutation importance on validation data
        res = permutation_importance(
            clf, X_v, y_v,
            scoring="roc_auc",
            n_repeats=5,
            random_state=random_state
        )
        
        fold_means = {feat: float(res.importances_mean[i]) for i, feat in enumerate(X.columns)}
        for feat, val in fold_means.items():
            split_importances[feat].append(val)
            
        # Determine ranks for this fold (1 = highest importance)
        sorted_feats = sorted(fold_means.keys(), key=lambda f: fold_means[f], reverse=True)
        for rank_pos, f_name in enumerate(sorted_feats, start=1):
            rank_occurrences[f_name].append(rank_pos)
            
    # 1. Summary Permutation Importance
    rf_perm_records = []
    for feat in X.columns:
        arr = np.array(split_importances[feat])
        m_imp = float(arr.mean())
        s_imp = float(arr.std())
        ci_l = m_imp - 1.96 * (s_imp / np.sqrt(len(arr)))
        ci_u = m_imp + 1.96 * (s_imp / np.sqrt(len(arr)))
        
        rf_perm_records.append({
            "feature": feat,
            "feature_label": feat.replace("_skills", "").replace("_", " ").title(),
            "mean_permutation_importance": round(m_imp, 4),
            "std_permutation_importance": round(s_imp, 4),
            "ci_95_lower": round(ci_l, 4),
            "ci_95_upper": round(ci_u, 4),
            "min_importance": round(float(arr.min()), 4),
            "max_importance": round(float(arr.max()), 4)
        })
    df_rf_perm = pd.DataFrame(rf_perm_records).sort_values(by="mean_permutation_importance", ascending=False).reset_index(drop=True)
    df_rf_perm["importance_rank"] = range(1, len(df_rf_perm) + 1)
    
    # 2. Rank Stability Diagnostics
    stability_records = []
    for feat in X.columns:
        ranks = np.array(rank_occurrences[feat])
        mean_rk = float(ranks.mean())
        std_rk = float(ranks.std())
        top1_pct = float((ranks == 1).sum() / len(ranks) * 100)
        top2_pct = float((ranks <= 2).sum() / len(ranks) * 100)
        
        stability_records.append({
            "feature": feat,
            "feature_label": feat.replace("_skills", "").replace("_", " ").title(),
            "cv_splits_evaluated": len(ranks),
            "mean_rank": round(mean_rk, 2),
            "std_rank": round(std_rk, 2),
            "pct_ranked_number_1": round(top1_pct, 1),
            "pct_ranked_top_2": round(top2_pct, 1),
            "modal_rank": int(pd.Series(ranks).mode().iloc[0]),
            "rank_stability": "VERY HIGH" if std_rk <= 0.6 else "HIGH" if std_rk <= 1.0 else "MODERATE"
        })
    df_stability = pd.DataFrame(stability_records).sort_values(by="mean_rank", ascending=True).reset_index(drop=True)
    return df_rf_perm, df_stability
