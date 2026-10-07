"""
logistic_models.py
------------------
Multivariable inferential binary logistic regression models and VIF diagnostics:
  - H2: JDS technical skills predicting salary_hike_high_or_low
  - H4: SDS Big Five personality traits predicting success_classification_high_low
  - H6: Analytics Jobs structural factors & skills predicting is_high_salary
  - VIF computation for multicollinearity detection
  - Parameter tables with Wald statistics, Odds Ratios (OR), and 95% CIs
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor


def compute_vif_dataframe(df_features: pd.DataFrame) -> pd.DataFrame:
    """
    Computes Variance Inflation Factor (VIF) for all predictors in df_features.
    Includes constant for correct intercept adjustment.
    """
    X = sm.add_constant(df_features.astype(float))
    vif_records = []
    
    for i, col in enumerate(X.columns):
        if col == "const":
            continue
        vif_val = variance_inflation_factor(X.values, i)
        
        if vif_val < 2.5:
            interp = "Low / Ideal (no collinearity concern)"
        elif vif_val < 5.0:
            interp = "Moderate / Acceptable"
        elif vif_val < 10.0:
            interp = "High / Potential multicollinearity"
        else:
            interp = "Severe multicollinearity"
            
        vif_records.append({
            "feature": col,
            "vif": round(float(vif_val), 3),
            "tolerance": round(float(1.0 / vif_val) if vif_val > 0 else 0.0, 3),
            "interpretation": interp
        })
        
    return pd.DataFrame(vif_records)


def fit_logistic_regression(
    y: pd.Series,
    X_raw: pd.DataFrame,
    standardize_continuous: bool = True,
    model_name: str = "Logistic Regression"
) -> Tuple[pd.DataFrame, Dict[str, object], sm.Logit]:
    """
    Fits an inferential multivariable binary logistic regression model.
    Returns:
      1. Parameter DataFrame with coefficients, SE, Wald z, p-values, OR, 95% CIs
      2. Diagnostics dictionary (Pseudo-R2, Log-Likelihood, LLR p-value, AIC, BIC, etc.)
      3. Fitted statsmodels BinaryResults object
    """
    X_proc = X_raw.copy().astype(float)
    continuous_stats = {}
    
    if standardize_continuous:
        for col in X_proc.columns:
            # Standardize if continuous (more than 2 unique values)
            if X_proc[col].nunique() > 2:
                col_mean = float(X_proc[col].mean())
                col_std = float(X_proc[col].std())
                continuous_stats[col] = {"mean": col_mean, "std": col_std}
                X_proc[col] = (X_proc[col] - col_mean) / (col_std if col_std > 0 else 1.0)
                
    X_const = sm.add_constant(X_proc)
    
    # Fit model using Newton-Raphson
    model = sm.Logit(y.astype(float), X_const)
    res = model.fit(disp=False, maxiter=100)
    
    # Compute Wald z, Odds Ratios, and Wald 95% Confidence Intervals
    params = res.params
    se = res.bse
    z_stat = res.tvalues
    p_vals = res.pvalues
    ci = res.conf_int()
    
    param_records = []
    for col in X_const.columns:
        b = float(params[col])
        s = float(se[col])
        z = float(z_stat[col])
        p = float(p_vals[col])
        ci_l = float(ci.loc[col, 0])
        ci_u = float(ci.loc[col, 1])
        
        # Odds ratio = exp(b)
        or_val = np.exp(b)
        or_ci_l = np.exp(ci_l)
        or_ci_u = np.exp(ci_u)
        
        param_records.append({
            "model": model_name,
            "parameter": col,
            "coef_beta": round(b, 4),
            "std_error": round(s, 4),
            "wald_z": round(z, 3),
            "p_value": float(p),
            "odds_ratio": round(float(or_val), 3),
            "or_ci_lower": round(float(or_ci_l), 3),
            "or_ci_upper": round(float(or_ci_u), 3),
            "standardized": bool(col in continuous_stats),
            "sig_indicator": "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
        })
        
    df_params = pd.DataFrame(param_records)
    
    # Separation and convergence diagnostics
    max_abs_coef = float(np.abs(params).max())
    max_se = float(se.max())
    quasi_separation = bool(max_abs_coef > 15.0 or max_se > 10.0)
    
    diagnostics = {
        "model_name": model_name,
        "sample_size_n": int(res.nobs),
        "target_positive_events": int(y.sum()),
        "target_positive_pct": round(float(y.mean() * 100), 2),
        "converged": bool(res.mle_retvals["converged"]),
        "iterations": int(res.mle_retvals["iterations"]),
        "log_likelihood": round(float(res.llf), 3),
        "log_likelihood_null": round(float(res.llnull), 3),
        "pseudo_r2_mcfadden": round(float(res.prsquared), 4),
        "llr_chi2": round(float(res.llr), 3),
        "llr_pvalue": float(res.llr_pvalue),
        "aic": round(float(res.aic), 2),
        "bic": round(float(res.bic), 2),
        "condition_number": round(float(np.linalg.cond(X_const)), 2),
        "quasi_separation_detected": quasi_separation
    }
    
    return df_params, diagnostics, res


def run_h2_jds_logistic(df_jds: pd.DataFrame, model_label: str = "H2_JDS_Primary_N139") -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, object]]:
    """Runs H2 JDS multivariable logistic model and VIF diagnostics."""
    skills = [
        "big_data_skills",
        "maths_stats_skills",
        "coding_skills",
        "ai_and_ml_skills",
        "dashboard_and_storytelling_skills"
    ]
    X = df_jds[skills]
    y = df_jds["salary_hike_high_or_low"]
    
    df_vif = compute_vif_dataframe(X)
    df_params, diag, _ = fit_logistic_regression(
        y, X, standardize_continuous=True, model_name=model_label
    )
    return df_params, df_vif, diag


def run_h4_sds_logistic(df_sds: pd.DataFrame, model_label: str = "H4_SDS_Primary_N161") -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, object]]:
    """Runs H4 SDS multivariable logistic model and VIF diagnostics."""
    traits = [
        "neuroticism",
        "extraversion",
        "openness_to_experience",
        "agreeableness",
        "conscientiousness"
    ]
    X = df_sds[traits]
    y = df_sds["success_classification_high_low"]
    
    df_vif = compute_vif_dataframe(X)
    df_params, diag, _ = fit_logistic_regression(
        y, X, standardize_continuous=True, model_name=model_label
    )
    return df_params, df_vif, diag


def run_h6_analytics_logistic(df_aj: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, object]]:
    """
    Runs H6 multivariable logistic regression on Analytics Jobs (N=15,841) predicting is_high_salary.
    Candidate predictors:
      - midpoint_experience (standardized continuous)
      - location_cluster dummies (reference: Bengaluru)
      - job_role_family dummies (reference: Data Science)
      - top skill indicators: skill_python, skill_r, skill_sql, skill_machine_learning,
        skill_sas, skill_spark, skill_excel, skill_analytics
    STRICT ZERO TARGET LEAKAGE: salary_rank and salary_midpoint are omitted.
    """
    y = df_aj["is_high_salary"]
    
    # 1. Experience
    exp_series = pd.Series(
        df_aj["midpoint_experience"], name="midpoint_experience"
    )
    
    # 2. Location dummies (drop Bengaluru as baseline)
    loc_dummies = pd.get_dummies(df_aj["location_cluster"], prefix="loc", dtype=float)
    if "loc_Bengaluru" in loc_dummies.columns:
        loc_dummies = loc_dummies.drop(columns=["loc_Bengaluru"])
    else:
        loc_dummies = loc_dummies.iloc[:, 1:]
        
    # 3. Role family dummies (drop Data Science as baseline)
    role_dummies = pd.get_dummies(df_aj["job_role_family"], prefix="role", dtype=float)
    if "role_Data Science" in role_dummies.columns:
        role_dummies = role_dummies.drop(columns=["role_Data Science"])
    else:
        role_dummies = role_dummies.iloc[:, 1:]
        
    # 4. Top skills
    top_skills = [
        "skill_python", "skill_r", "skill_sql", "skill_machine_learning",
        "skill_sas", "skill_spark", "skill_excel", "skill_analytics"
    ]
    skill_df = df_aj[top_skills].astype(float)
    
    X = pd.concat([exp_series, loc_dummies, role_dummies, skill_df], axis=1)
    
    df_vif = compute_vif_dataframe(X)
    df_params, diag, _ = fit_logistic_regression(
        y, X, standardize_continuous=True, model_name="H6_Multivariable_Premium_Salary_N15841"
    )
    return df_params, df_vif, diag
