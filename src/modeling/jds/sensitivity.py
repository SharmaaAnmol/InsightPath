"""
sensitivity.py
--------------
Sensitivity modeling and parsimony evaluation for JDS skills:
  - Repeated CV evaluation on sensitivity cohort (N=137, ID 3291 excluded)
  - Pre-registered robustness audit: delta AUC <= 0.02 threshold check
  - Coefficient and odds ratio drift analysis
  - Permutation feature importance stability between cohorts
  - Full (5 features) vs Phase-4-informed Reduced (2 features) parsimony comparison
"""

from typing import Dict, List, Tuple, Any
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.inspection import permutation_importance

from src.modeling.jds.data import JDS_FEATURES, JDS_REDUCED_FEATURES
from src.modeling.jds.pipelines import build_candidate_pipelines, build_reduced_pipelines
from src.modeling.jds.cross_validation import evaluate_pipelines_cv


def run_sensitivity_modeling(
    pipelines: Dict[str, Any],
    X_sens: pd.DataFrame,
    y_sens: pd.Series,
    df_summary_prim: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Evaluates candidate pipelines on sensitivity cohort N=137 and compares against primary cohort N=139.
    Returns:
      1. df_sens_perf: sensitivity model performance and delta AUC comparison table
      2. df_sens_folds: fold-by-fold results for sensitivity
      3. df_sens_oof: out-of-fold predictions for sensitivity
    """
    df_sens_folds, df_sens_oof, df_sens_sum = evaluate_pipelines_cv(pipelines, X_sens, y_sens)
    
    # Merge primary and sensitivity summaries
    merged = pd.merge(
        df_summary_prim[["model_name", "roc_auc_mean", "macro_f1_mean", "accuracy_mean"]],
        df_sens_sum[["model_name", "roc_auc_mean", "macro_f1_mean", "accuracy_mean"]],
        on="model_name",
        suffixes=("_primary", "_sensitivity")
    )
    
    records = []
    for _, row in merged.iterrows():
        auc_p = row["roc_auc_mean_primary"]
        auc_s = row["roc_auc_mean_sensitivity"]
        delta_auc = abs(auc_p - auc_s)
        f1_p = row["macro_f1_mean_primary"]
        f1_s = row["macro_f1_mean_sensitivity"]
        delta_f1 = abs(f1_p - f1_s)
        
        # Pre-registered robustness classification rule:
        # If delta_auc <= 0.02 -> ROBUST TO OBSERVATIONAL NOISE
        if delta_auc <= 0.02:
            verdict = "ROBUST TO OBSERVATIONAL NOISE"
        elif delta_auc <= 0.05:
            verdict = "DIRECTIONALLY ROBUST"
        else:
            verdict = "SENSITIVE"
            
        records.append({
            "model_name": row["model_name"],
            "primary_n": 139,
            "sensitivity_n": 137,
            "primary_roc_auc": round(float(auc_p), 4),
            "sensitivity_roc_auc": round(float(auc_s), 4),
            "delta_roc_auc": round(float(delta_auc), 4),
            "primary_macro_f1": round(float(f1_p), 4),
            "sensitivity_macro_f1": round(float(f1_s), 4),
            "delta_macro_f1": round(float(delta_f1), 4),
            "primary_accuracy": round(float(row["accuracy_mean_primary"]), 4),
            "sensitivity_accuracy": round(float(row["accuracy_mean_sensitivity"]), 4),
            "robustness_verdict": verdict
        })
        
    df_sens_perf = pd.DataFrame(records).sort_values(by="primary_roc_auc", ascending=False).reset_index(drop=True)
    return df_sens_perf, df_sens_folds, df_sens_oof


def compare_sensitivity_coefficients(
    X_prim: pd.DataFrame,
    y_prim: pd.Series,
    X_sens: pd.DataFrame,
    y_sens: pd.Series,
    random_state: int = 42
) -> pd.DataFrame:
    """
    Compares standardized logistic regression coefficients between Primary N=139 and Sensitivity N=137.
    Builds Table 18: phase5_sensitivity_coefficients.csv.
    """
    pipe_prim = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(l1_ratio=0.0, solver="lbfgs", C=1.0, max_iter=1000, random_state=random_state))
    ])
    pipe_sens = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(l1_ratio=0.0, solver="lbfgs", C=1.0, max_iter=1000, random_state=random_state))
    ])
    
    pipe_prim.fit(X_prim, y_prim)
    pipe_sens.fit(X_sens, y_sens)
    
    c_prim = pipe_prim.named_steps["clf"].coef_[0]
    c_sens = pipe_sens.named_steps["clf"].coef_[0]
    
    records = []
    for feat, b_p, b_s in zip(X_prim.columns, c_prim, c_sens):
        or_p = float(np.exp(b_p))
        or_s = float(np.exp(b_s))
        delta_b = abs(b_p - b_s)
        delta_or = abs(or_p - or_s)
        
        records.append({
            "feature": feat,
            "feature_label": feat.replace("_skills", "").replace("_", " ").title(),
            "primary_coef_beta": round(float(b_p), 4),
            "sens_coef_beta": round(float(b_s), 4),
            "delta_coef": round(float(delta_b), 4),
            "primary_odds_ratio": round(or_p, 3),
            "sens_odds_ratio": round(or_s, 3),
            "delta_odds_ratio": round(float(delta_or), 3),
            "rank_primary": 0,  # to be assigned
            "rank_sens": 0,
            "rank_preserved": True
        })
        
    df_c = pd.DataFrame(records).sort_values(by="primary_coef_beta", ascending=False).reset_index(drop=True)
    df_c["rank_primary"] = range(1, len(df_c) + 1)
    
    # Assign sensitivity ranks
    df_c_s = df_c.sort_values(by="sens_coef_beta", ascending=False).reset_index(drop=True)
    sens_ranks = {row["feature"]: rk for rk, row in enumerate(df_c_s.to_dict(orient="records"), start=1)}
    df_c["rank_sens"] = df_c["feature"].map(sens_ranks)
    df_c["rank_preserved"] = df_c["rank_primary"] == df_c["rank_sens"]
    df_c["stability_status"] = df_c["rank_preserved"].apply(lambda p: "ROBUST (Identical Rank)" if p else "MODERATE DRIFT")
    
    return df_c


def compare_sensitivity_feature_importance(
    df_rf_perm_prim: pd.DataFrame,
    X_sens: pd.DataFrame,
    y_sens: pd.Series,
    random_state: int = 42
) -> pd.DataFrame:
    """
    Compares Random Forest permutation feature importance between Primary N=139 and Sensitivity N=137.
    Builds Table 19: phase5_sensitivity_feature_importance.csv.
    """
    from sklearn.ensemble import RandomForestClassifier
    rf = RandomForestClassifier(n_estimators=100, max_depth=3, min_samples_leaf=4, max_features="sqrt", random_state=random_state)
    rf.fit(X_sens, y_sens)
    
    res = permutation_importance(rf, X_sens, y_sens, scoring="roc_auc", n_repeats=10, random_state=random_state)
    
    sens_means = {feat: float(res.importances_mean[i]) for i, feat in enumerate(X_sens.columns)}
    
    records = []
    for _, row in df_rf_perm_prim.iterrows():
        feat = row["feature"]
        m_p = row["mean_permutation_importance"]
        m_s = sens_means[feat]
        delta_m = abs(m_p - m_s)
        
        records.append({
            "feature": feat,
            "feature_label": row["feature_label"],
            "primary_perm_importance": m_p,
            "sens_perm_importance": round(m_s, 4),
            "delta_importance": round(delta_m, 4),
            "primary_rank": row["importance_rank"],
            "sens_rank": 0,  # to be assigned
            "rank_preserved": True
        })
        
    df_imp = pd.DataFrame(records)
    # Assign sensitivity rank
    df_imp_s = df_imp.sort_values(by="sens_perm_importance", ascending=False).reset_index(drop=True)
    sens_ranks = {row["feature"]: rk for rk, row in enumerate(df_imp_s.to_dict(orient="records"), start=1)}
    df_imp["sens_rank"] = df_imp["feature"].map(sens_ranks)
    df_imp["rank_preserved"] = df_imp["primary_rank"] == df_imp["sens_rank"]
    df_imp["stability_status"] = df_imp["rank_preserved"].apply(lambda p: "ROBUST (Identical Rank)" if p else "MODERATE DRIFT")
    
    return df_imp.sort_values(by="primary_rank", ascending=True).reset_index(drop=True)


def evaluate_full_vs_reduced_features(
    X: pd.DataFrame,
    y: pd.Series,
    random_state: int = 42
) -> pd.DataFrame:
    """
    Compares 5-Feature Full Model against Phase-4-informed 2-Feature Reduced Model
    (Maths/Stats + Storytelling).
    Builds Table 16: phase5_full_vs_reduced_features.csv.
    """
    full_pipes = {
        "Logistic_L2": build_candidate_pipelines(random_state)["Logistic_Regression_L2"],
        "Decision_Tree": build_candidate_pipelines(random_state)["Decision_Tree"],
        "Random_Forest": build_candidate_pipelines(random_state)["Random_Forest"]
    }
    red_pipes = build_reduced_pipelines(random_state)
    
    _, _, sum_full = evaluate_pipelines_cv(full_pipes, X, y, random_state=random_state)
    _, _, sum_red = evaluate_pipelines_cv(red_pipes, X[JDS_REDUCED_FEATURES], y, random_state=random_state)
    
    pairs = [
        ("Logistic Regression L2", "Logistic_L2", "Logistic_L2_Reduced_2Feat"),
        ("Decision Tree Classifier", "Decision_Tree", "Decision_Tree_Reduced_2Feat"),
        ("Random Forest Classifier", "Random_Forest", "Random_Forest_Reduced_2Feat")
    ]
    
    records = []
    for label, full_key, red_key in pairs:
        f_row = sum_full[sum_full["model_name"] == full_key].iloc[0]
        r_row = sum_red[sum_red["model_name"] == red_key].iloc[0]
        
        auc_f = f_row["roc_auc_mean"]
        auc_r = r_row["roc_auc_mean"]
        delta_auc = auc_f - auc_r
        pct_retained = (auc_r / auc_f * 100) if auc_f > 0 else 0.0
        
        records.append({
            "algorithm_family": label,
            "full_features_n": 5,
            "reduced_features_n": 2,
            "reduced_feature_set": "maths_stats_skills + dashboard_and_storytelling_skills",
            "full_roc_auc": auc_f,
            "reduced_roc_auc": auc_r,
            "delta_roc_auc": round(float(delta_auc), 4),
            "pct_auc_retained": round(float(pct_retained), 2),
            "full_macro_f1": f_row["macro_f1_mean"],
            "reduced_macro_f1": r_row["macro_f1_mean"],
            "full_accuracy": f_row["accuracy_mean"],
            "reduced_accuracy": r_row["accuracy_mean"],
            "parsimony_assessment": f"Retains {pct_retained:.1f}% of full discrimination with 60% fewer features."
        })
        
    return pd.DataFrame(records)
