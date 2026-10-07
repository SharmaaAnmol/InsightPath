"""
correlations.py
---------------
Evaluates bivariate correlation and regression models for H5:
  - Pearson correlation with Fisher's z 95% CI
  - Spearman rank correlation
  - Bivariate OLS regressions (raw and log-transformed salary) with HC3 robust SEs
  - Adjusted OLS models controlling for job title and posting volume
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm

from src.statistics.effect_sizes import compute_pearson_r_with_ci


def compute_spearman_rho_with_ci(
    x: pd.Series,
    y: pd.Series,
    alpha: float = 0.05
) -> Dict[str, float]:
    """Compute Spearman rank correlation with asymptotic 95% confidence interval."""
    df_clean = pd.DataFrame({"x": x, "y": y}).dropna()
    n = len(df_clean)
    if n < 4:
        raise ValueError("Sample size too small for Spearman CI calculation.")
        
    rho, p_val = stats.spearmanr(df_clean["x"], df_clean["y"])
    rho_clipped = np.clip(rho, -0.9999, 0.9999)
    z = np.arctanh(rho_clipped)
    # Fieller et al. standard error for Spearman rho Fisher transform
    se_z = np.sqrt(1.06 / (n - 3))
    
    z_crit = stats.norm.ppf(1 - alpha / 2)
    ci_lower = np.tanh(z - z_crit * se_z)
    ci_upper = np.tanh(z + z_crit * se_z)
    
    return {
        "rho": round(float(rho), 3),
        "p_value": float(p_val),
        "ci_lower": round(float(ci_lower), 3),
        "ci_upper": round(float(ci_upper), 3),
        "n": n
    }


def run_h5_bivariate_regressions(df_ds: pd.DataFrame) -> pd.DataFrame:
    """
    Run OLS bivariate regressions for H5 (DataScience Jobs, N=1,602):
      1. avg_salary_lakh ~ min_experience (raw)
      2. log(avg_salary_lakh) ~ min_experience (log-transformed)
      3. min_salary_lakh ~ min_experience
      4. max_salary_lakh ~ min_experience
    Fits with HC3 robust standard errors.
    """
    df = df_ds.copy()
    df["log_avg_salary"] = np.log(df["avg_salary_lakh"])
    df["log_min_salary"] = np.log(df["min_salary_lakh"])
    df["log_max_salary"] = np.log(df["max_salary_lakh"])
    
    models_spec = [
        ("avg_salary_lakh", "avg_salary_lakh ~ min_experience (Linear)"),
        ("log_avg_salary", "log(avg_salary_lakh) ~ min_experience (Semi-Log)"),
        ("min_salary_lakh", "min_salary_lakh ~ min_experience (Linear)"),
        ("max_salary_lakh", "max_salary_lakh ~ min_experience (Linear)")
    ]
    
    results = []
    x = sm.add_constant(df["min_experience"])
    
    for outcome_col, model_label in models_spec:
        y = df[outcome_col]
        # Fit OLS with HC3 heteroskedasticity-robust covariance
        ols_model = sm.OLS(y, x).fit(cov_type="HC3")
        
        beta_0 = ols_model.params["const"]
        beta_1 = ols_model.params["min_experience"]
        se_beta_1 = ols_model.bse["min_experience"]
        ci_lower, ci_upper = ols_model.conf_int().loc["min_experience"]
        p_val = ols_model.pvalues["min_experience"]
        r_sq = ols_model.rsquared
        adj_r_sq = ols_model.rsquared_adj
        f_stat = ols_model.fvalue
        f_pval = ols_model.f_pvalue
        n = int(ols_model.nobs)
        
        results.append({
            "model_specification": model_label,
            "dependent_variable": outcome_col,
            "independent_variable": "min_experience",
            "n": n,
            "intercept": round(float(beta_0), 4),
            "slope_beta": round(float(beta_1), 4),
            "slope_se_hc3": round(float(se_beta_1), 4),
            "ci_lower": round(float(ci_lower), 4),
            "ci_upper": round(float(ci_upper), 4),
            "t_stat": round(float(ols_model.tvalues["min_experience"]), 3),
            "p_value": float(p_val),
            "r_squared": round(float(r_sq), 4),
            "adj_r_squared": round(float(adj_r_sq), 4),
            "f_stat": round(float(f_stat), 2) if f_stat is not None else np.nan,
            "f_pvalue": float(f_pval) if f_pval is not None else np.nan
        })
        
    return pd.DataFrame(results)


def run_h5_adjusted_regressions(df_ds: pd.DataFrame) -> pd.DataFrame:
    """
    Run adjusted regression models for H5:
      Model 1: avg_salary_lakh ~ min_experience + C(job_title)
      Model 2: log(avg_salary_lakh) ~ min_experience + C(job_title)
      Model 3: log(avg_salary_lakh) ~ min_experience + C(job_title) + log10_num_of_jobs
    Using HC3 robust standard errors.
    """
    df = df_ds.copy()
    df["log_avg_salary"] = np.log(df["avg_salary_lakh"])
    
    # Create job title dummies (reference: Data Scientist)
    dummies_job = pd.get_dummies(df["job_title"], prefix="title", drop_first=True, dtype=float)
    
    specs = [
        (
            "avg_salary_lakh ~ min_experience + job_title (Linear Adjusted)",
            df["avg_salary_lakh"],
            pd.concat([df[["min_experience"]], dummies_job], axis=1)
        ),
        (
            "log(avg_salary_lakh) ~ min_experience + job_title (Semi-Log Adjusted)",
            df["log_avg_salary"],
            pd.concat([df[["min_experience"]], dummies_job], axis=1)
        ),
        (
            "log(avg_salary_lakh) ~ min_experience + job_title + log10_num_of_jobs (Full Adjusted)",
            df["log_avg_salary"],
            pd.concat([df[["min_experience", "log10_num_of_jobs"]], dummies_job], axis=1)
        )
    ]
    
    results = []
    for spec_name, y, X_raw in specs:
        X = sm.add_constant(X_raw)
        model = sm.OLS(y, X).fit(cov_type="HC3")
        
        beta_exp = model.params["min_experience"]
        se_exp = model.bse["min_experience"]
        ci_low, ci_high = model.conf_int().loc["min_experience"]
        p_exp = model.pvalues["min_experience"]
        
        results.append({
            "model_specification": spec_name,
            "dependent_variable": y.name,
            "n": int(model.nobs),
            "experience_slope_beta": round(float(beta_exp), 4),
            "experience_se_hc3": round(float(se_exp), 4),
            "ci_lower": round(float(ci_low), 4),
            "ci_upper": round(float(ci_high), 4),
            "t_stat": round(float(model.tvalues["min_experience"]), 3),
            "p_value": float(p_exp),
            "r_squared": round(float(model.rsquared), 4),
            "adj_r_squared": round(float(model.rsquared_adj), 4),
            "f_stat": round(float(model.fvalue), 2) if model.fvalue is not None else np.nan,
            "num_predictors": int(len(X.columns) - 1)
        })
        
    return pd.DataFrame(results)


def run_h5_correlation_tests(df_ds: pd.DataFrame, df_aj: pd.DataFrame) -> pd.DataFrame:
    """Run all primary H5 correlation tests across both market datasets."""
    records = []
    
    # 1. DataScience Jobs: min_experience vs avg_salary_lakh
    p_res = compute_pearson_r_with_ci(df_ds["min_experience"], df_ds["avg_salary_lakh"])
    s_res = compute_spearman_rho_with_ci(df_ds["min_experience"], df_ds["avg_salary_lakh"])
    records.append({
        "dataset": "DataScience Jobs",
        "var_x": "min_experience",
        "var_y": "avg_salary_lakh",
        "n": p_res["n"],
        "metric": "Pearson r",
        "estimate": p_res["r"],
        "ci_lower": p_res["ci_lower"],
        "ci_upper": p_res["ci_upper"],
        "p_value": p_res["p_value"],
        "interpretation": "Moderate-to-strong positive linear correlation"
    })
    records.append({
        "dataset": "DataScience Jobs",
        "var_x": "min_experience",
        "var_y": "avg_salary_lakh",
        "n": s_res["n"],
        "metric": "Spearman rho",
        "estimate": s_res["rho"],
        "ci_lower": s_res["ci_lower"],
        "ci_upper": s_res["ci_upper"],
        "p_value": s_res["p_value"],
        "interpretation": "Moderate monotonic positive rank correlation"
    })
    
    # 2. DataScience Jobs: min_experience vs log(avg_salary_lakh)
    log_salary = np.log(df_ds["avg_salary_lakh"])
    p_log = compute_pearson_r_with_ci(df_ds["min_experience"], log_salary)
    records.append({
        "dataset": "DataScience Jobs",
        "var_x": "min_experience",
        "var_y": "log(avg_salary_lakh)",
        "n": p_log["n"],
        "metric": "Pearson r (Semi-log)",
        "estimate": p_log["r"],
        "ci_lower": p_log["ci_lower"],
        "ci_upper": p_log["ci_upper"],
        "p_value": p_log["p_value"],
        "interpretation": "Semi-log linear relationship"
    })
    
    # 3. Analytics Jobs: midpoint_experience vs salary_midpoint
    # (Checking monotonic alignment in individual vacancy dataset)
    p_aj = compute_pearson_r_with_ci(df_aj["midpoint_experience"], df_aj["salary_midpoint"])
    s_aj = compute_spearman_rho_with_ci(df_aj["midpoint_experience"], df_aj["salary_midpoint"])
    records.append({
        "dataset": "Analytics Jobs",
        "var_x": "midpoint_experience",
        "var_y": "salary_midpoint",
        "n": p_aj["n"],
        "metric": "Pearson r",
        "estimate": p_aj["r"],
        "ci_lower": p_aj["ci_lower"],
        "ci_upper": p_aj["ci_upper"],
        "p_value": p_aj["p_value"],
        "interpretation": "Moderate positive linear association"
    })
    records.append({
        "dataset": "Analytics Jobs",
        "var_x": "midpoint_experience",
        "var_y": "salary_midpoint",
        "n": s_aj["n"],
        "metric": "Spearman rho",
        "estimate": s_aj["rho"],
        "ci_lower": s_aj["ci_lower"],
        "ci_upper": s_aj["ci_upper"],
        "p_value": s_aj["p_value"],
        "interpretation": "Moderate positive rank correlation"
    })
    
    return pd.DataFrame(records)
