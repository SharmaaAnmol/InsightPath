"""
group_tests.py
--------------
Inferential group comparison tests for Phase 4:
  - Mann-Whitney U test (non-parametric rank-sum test)
  - Student's t-test and Welch's t-test
  - Kruskal-Wallis H test (one-way non-parametric ANOVA)
  - Integration with Cohen's d and rank-biserial effect sizes
"""

from typing import Dict, List, Optional
import numpy as np
import pandas as pd
from scipy import stats

from src.statistics.effect_sizes import compute_cohens_d_with_ci, compute_rank_biserial_with_ci


def run_two_group_comparison(
    group1: pd.Series,
    group2: pd.Series,
    variable_name: str,
    group1_label: str = "High",
    group2_label: str = "Low",
    alternative: str = "two-sided"
) -> Dict[str, object]:
    """
    Run comprehensive two-sample comparison:
    Both parametric (Welch t-test) and non-parametric (Mann-Whitney U) tests,
    plus effect sizes (Cohen's d and rank-biserial correlation) with 95% CIs.
    """
    g1 = group1.dropna()
    g2 = group2.dropna()
    n1, n2 = len(g1), len(g2)
    
    if n1 < 2 or n2 < 2:
        raise ValueError(f"Insufficient sample sizes: n1={n1}, n2={n2}")
        
    m1, m2 = float(g1.mean()), float(g2.mean())
    med1, med2 = float(g1.median()), float(g2.median())
    s1, s2 = float(g1.std()), float(g2.std())
    mean_diff = m1 - m2
    median_diff = med1 - med2
    
    # Non-parametric: Mann-Whitney U
    u_res = stats.mannwhitneyu(g1, g2, alternative=alternative)
    u_stat = float(u_res.statistic)
    p_mwu = float(u_res.pvalue)
    
    # Parametric: Welch's t-test (robust to unequal variances)
    t_res = stats.ttest_ind(g1, g2, equal_var=False, alternative=alternative)
    t_stat = float(t_res.statistic)
    p_t = float(t_res.pvalue)
    
    # Effect sizes with 95% CIs
    d_dict = compute_cohens_d_with_ci(g1, g2)
    rb_dict = compute_rank_biserial_with_ci(u_stat, n1, n2)
    
    return {
        "variable": variable_name,
        "n_group1": n1,
        "n_group2": n2,
        "group1_label": group1_label,
        "group2_label": group2_label,
        "mean_group1": round(m1, 3),
        "mean_group2": round(m2, 3),
        "mean_diff": round(mean_diff, 3),
        "median_group1": round(med1, 3),
        "median_group2": round(med2, 3),
        "median_diff": round(median_diff, 3),
        "std_group1": round(s1, 3),
        "std_group2": round(s2, 3),
        "mann_whitney_u": round(u_stat, 2),
        "p_value_mwu": float(p_mwu),
        "welch_t_stat": round(t_stat, 3),
        "p_value_t": float(p_t),
        "cohens_d": d_dict["d"],
        "cohens_d_ci_lower": d_dict["ci_lower"],
        "cohens_d_ci_upper": d_dict["ci_upper"],
        "rank_biserial_r": rb_dict["r_rb"],
        "rank_biserial_ci_lower": rb_dict["ci_lower"],
        "rank_biserial_ci_upper": rb_dict["ci_upper"]
    }


def run_jds_skill_group_tests(df_jds: pd.DataFrame, alternative: str = "two-sided") -> pd.DataFrame:
    """Run two-group comparisons for the 5 JDS skills across salary_hike_high_or_low."""
    skills = [
        "big_data_skills",
        "maths_stats_skills",
        "coding_skills",
        "ai_and_ml_skills",
        "dashboard_and_storytelling_skills"
    ]
    results = []
    g_high = df_jds[df_jds["salary_hike_high_or_low"] == 1]
    g_low = df_jds[df_jds["salary_hike_high_or_low"] == 0]
    
    for sk in skills:
        res = run_two_group_comparison(
            g_high[sk], g_low[sk],
            variable_name=sk,
            group1_label="High Hike (Y=1)",
            group2_label="Low Hike (Y=0)",
            alternative=alternative
        )
        results.append(res)
        
    return pd.DataFrame(results)


def run_sds_trait_group_tests(df_sds: pd.DataFrame, alternative: str = "two-sided") -> pd.DataFrame:
    """Run two-group comparisons for the 5 SDS Big Five traits across success_classification_high_low."""
    traits = [
        "neuroticism",
        "extraversion",
        "openness_to_experience",
        "agreeableness",
        "conscientiousness"
    ]
    results = []
    g_high = df_sds[df_sds["success_classification_high_low"] == 1]
    g_low = df_sds[df_sds["success_classification_high_low"] == 0]
    
    for tr in traits:
        res = run_two_group_comparison(
            g_high[tr], g_low[tr],
            variable_name=tr,
            group1_label="High Success (Y=1)",
            group2_label="Low Success (Y=0)",
            alternative=alternative
        )
        results.append(res)
        
    return pd.DataFrame(results)


def run_kruskal_wallis_test(
    df: pd.DataFrame,
    group_col: str,
    val_col: str
) -> Dict[str, object]:
    """
    Run omnibus Kruskal-Wallis H test across categorical groups.
    Computes H statistic, p-value, and epsilon-squared effect size.
    """
    df_clean = df[[group_col, val_col]].dropna()
    groups = [group[val_col].values for _, group in df_clean.groupby(group_col)]
    
    h_stat, p_val = stats.kruskal(*groups)
    n = len(df_clean)
    k = len(groups)
    
    # Epsilon-squared: (H - k + 1) / (n - k)
    epsilon_sq = (h_stat - k + 1) / (n - k) if (n > k) else 0.0
    epsilon_sq = max(0.0, float(epsilon_sq))
    
    return {
        "group_col": group_col,
        "val_col": val_col,
        "num_groups": k,
        "total_n": n,
        "h_statistic": round(float(h_stat), 3),
        "p_value": float(p_val),
        "epsilon_squared": round(float(epsilon_sq), 4)
    }
