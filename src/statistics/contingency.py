"""
contingency.py
--------------
Categorical association testing for H6:
  - Chi-square test of independence for Geography vs Premium Salary
  - Standardized Pearson residuals and Adjusted Standardized Residuals
  - Cramér's V effect size
  - Kruskal-Wallis H test and post-hoc pairwise tests for Regional Salary Rank
  - 2x2 contingency tables and Odds Ratios for skill-premium associations
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

from src.statistics.effect_sizes import compute_odds_ratio_with_ci, compute_cramers_v


def run_geographic_chisquare_test(df_aj: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, object]]:
    """
    Evaluates geographic independence: location_cluster x is_high_salary.
    Computes:
      - Observed frequencies
      - Expected frequencies
      - Standardized residuals (Pearson residuals)
      - Adjusted standardized residuals (Haberman residuals)
      - Chi-square test statistic, df, p-value, Cramér's V
    """
    ct = pd.crosstab(df_aj["location_cluster"], df_aj["is_high_salary"])
    chi2, p_val, dof, expected = stats.chi2_contingency(ct, correction=False)
    
    n_total = float(ct.values.sum())
    v_cramer = compute_cramers_v(ct.values)
    
    row_sums = ct.sum(axis=1).values
    col_sums = ct.sum(axis=0).values
    
    records = []
    for i, cluster in enumerate(ct.index):
        obs_low = ct.loc[cluster, 0]
        obs_high = ct.loc[cluster, 1]
        exp_low = expected[i, 0]
        exp_high = expected[i, 1]
        
        # Pearson standardized residual: (O - E) / sqrt(E)
        std_res_low = (obs_low - exp_low) / np.sqrt(exp_low)
        std_res_high = (obs_high - exp_high) / np.sqrt(exp_high)
        
        # Adjusted standardized residual (Haberman):
        # r_adj = (O - E) / sqrt(E * (1 - r_i/N) * (1 - c_j/N))
        denom_high = np.sqrt(exp_high * (1.0 - row_sums[i] / n_total) * (1.0 - col_sums[1] / n_total))
        adj_res_high = (obs_high - exp_high) / denom_high if denom_high > 0 else 0.0
        
        high_pct = (obs_high / (obs_low + obs_high)) * 100
        
        records.append({
            "location_cluster": cluster,
            "total_postings": int(obs_low + obs_high),
            "observed_high_salary": int(obs_high),
            "expected_high_salary": round(float(exp_high), 2),
            "observed_standard_salary": int(obs_low),
            "expected_standard_salary": round(float(exp_low), 2),
            "high_salary_pct": round(float(high_pct), 2),
            "std_residual_high": round(float(std_res_high), 3),
            "adj_standardized_residual_high": round(float(adj_res_high), 3),
            "local_direction": "Over-represented" if adj_res_high > 2.0 else "Under-represented" if adj_res_high < -2.0 else "Neutral"
        })
        
    df_results = pd.DataFrame(records)
    
    summary_meta = {
        "test_name": "Pearson Chi-Square Test of Independence",
        "contingency_table": "location_cluster x is_high_salary (7 x 2)",
        "n_total": int(n_total),
        "chi2_statistic": round(float(chi2), 3),
        "degrees_of_freedom": int(dof),
        "p_value": float(p_val),
        "cramers_v": float(v_cramer),
        "min_expected_frequency": round(float(expected.min()), 2),
        "assumptions_met": bool(expected.min() >= 5.0)
    }
    
    return df_results, summary_meta


def run_regional_salary_rank_posthoc(df_aj: pd.DataFrame) -> pd.DataFrame:
    """
    Conducts post-hoc pairwise Mann-Whitney U tests comparing salary_rank across
    all pairs of the 7 location clusters, with Benjamini-Hochberg FDR correction.
    """
    clusters = sorted(df_aj["location_cluster"].dropna().unique())
    pairs = []
    
    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            c1, c2 = clusters[i], clusters[j]
            s1 = df_aj[df_aj["location_cluster"] == c1]["salary_rank"].dropna()
            s2 = df_aj[df_aj["location_cluster"] == c2]["salary_rank"].dropna()
            
            u_res = stats.mannwhitneyu(s1, s2, alternative="two-sided")
            u_stat = float(u_res.statistic)
            p_val = float(u_res.pvalue)
            
            # Rank-biserial correlation
            r_rb = 1.0 - (2.0 * u_stat / (len(s1) * len(s2)))
            
            pairs.append({
                "cluster_1": c1,
                "cluster_2": c2,
                "n_1": len(s1),
                "n_2": len(s2),
                "mean_rank_1": round(float(s1.mean()), 2),
                "mean_rank_2": round(float(s2.mean()), 2),
                "mann_whitney_u": round(u_stat, 1),
                "rank_biserial_r": round(float(r_rb), 3),
                "raw_p_value": float(p_val)
            })
            
    df_posthoc = pd.DataFrame(pairs)
    
    # Apply Benjamini-Hochberg FDR correction across pairwise tests
    reject, pvals_corrected, _, _ = multipletests(df_posthoc["raw_p_value"], alpha=0.05, method="fdr_bh")
    df_posthoc["fdr_adjusted_p"] = [round(float(p), 6) for p in pvals_corrected]
    df_posthoc["significant_after_fdr"] = reject
    
    return df_posthoc


def run_skill_premium_associations(
    df_aj: pd.DataFrame,
    skill_columns: Optional[List[str]] = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Evaluates 2x2 contingency tables and Odds Ratios for individual skills vs is_high_salary.
    Applies Benjamini-Hochberg FDR correction.
    Returns:
      1. Complete skill association table
      2. Formal H6 FDR results table
    """
    if skill_columns is None:
        # Default to all binary skill columns with at least 50 occurrences
        skill_cols = [c for c in df_aj.columns if c.startswith("skill_")]
        skill_columns = [c for c in skill_cols if df_aj[c].sum() >= 50]
        
    records = []
    for sk in skill_columns:
        # 2x2 table:
        # a: skill=1, high=1
        # b: skill=1, high=0
        # c: skill=0, high=1
        # d: skill=0, high=0
        tab = pd.crosstab(df_aj[sk], df_aj["is_high_salary"])
        a = int(tab.loc[1, 1]) if (1 in tab.index and 1 in tab.columns) else 0
        b = int(tab.loc[1, 0]) if (1 in tab.index and 0 in tab.columns) else 0
        c = int(tab.loc[0, 1]) if (0 in tab.index and 1 in tab.columns) else 0
        d = int(tab.loc[0, 0]) if (0 in tab.index and 0 in tab.columns) else 0
        
        chi2, p_val, _, _ = stats.chi2_contingency([[a, b], [c, d]], correction=True)
        or_dict = compute_odds_ratio_with_ci(a, b, c, d)
        
        n_with_skill = a + b
        pct_high_with_skill = (a / n_with_skill * 100) if n_with_skill > 0 else 0.0
        pct_high_without_skill = (c / (c + d) * 100) if (c + d) > 0 else 0.0
        
        clean_skill_name = sk.replace("skill_", "").replace("_", " ").title()
        
        records.append({
            "skill_code": sk,
            "skill_name": clean_skill_name,
            "n_with_skill": n_with_skill,
            "pct_high_with_skill": round(float(pct_high_with_skill), 2),
            "pct_high_without_skill": round(float(pct_high_without_skill), 2),
            "cell_a_skill_high": a,
            "cell_b_skill_low": b,
            "cell_c_noskill_high": c,
            "cell_d_noskill_low": d,
            "odds_ratio": or_dict["odds_ratio"],
            "ci_lower": or_dict["ci_lower"],
            "ci_upper": or_dict["ci_upper"],
            "chi2_statistic": round(float(chi2), 3),
            "raw_p_value": float(p_val)
        })
        
    df_skills = pd.DataFrame(records)
    
    # Sort by raw p-value
    df_skills = df_skills.sort_values(by="raw_p_value", ascending=True).reset_index(drop=True)
    
    # Apply Benjamini-Hochberg FDR correction
    reject, pvals_corrected, _, _ = multipletests(df_skills["raw_p_value"], alpha=0.05, method="fdr_bh")
    df_skills["fdr_adjusted_p"] = [round(float(p), 6) for p in pvals_corrected]
    df_skills["significant_after_fdr"] = reject
    
    # Create formal FDR results table for H6
    fdr_table = df_skills[[
        "skill_code", "skill_name", "odds_ratio", "ci_lower", "ci_upper",
        "raw_p_value", "fdr_adjusted_p", "significant_after_fdr"
    ]].copy()
    fdr_table["hypothesis"] = "H6"
    fdr_table["test_family"] = "Analytics Jobs Skill-Premium Contingency Family"
    
    return df_skills, fdr_table
