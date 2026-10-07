"""
assumptions.py
--------------
Evaluates parametric and distribution assumptions for Phase 4 inferential testing.
Computes:
  - Shapiro-Wilk test for normality
  - Skewness and kurtosis coefficients
  - Ceiling and floor effect diagnostics
  - Evaluation of parametric vs non-parametric justification
"""

from typing import Dict, List, Optional
import numpy as np
import pandas as pd
from scipy import stats


def evaluate_distribution_assumptions(
    series: pd.Series,
    variable_name: str,
    dataset_name: str,
    class_label: Optional[str] = "Overall",
    max_scale_value: Optional[float] = None
) -> Dict[str, object]:
    """
    Perform formal assumption checks on a continuous numeric series.
    Returns structured diagnostic dictionary.
    """
    s = series.dropna()
    n = len(s)
    if n < 3:
        raise ValueError(f"Sample size too small for assumption testing: n={n}")

    # Shapiro-Wilk test for normality
    # scipy.stats.shapiro works up to N=5000
    if n <= 5000:
        stat_sw, p_sw = stats.shapiro(s)
    else:
        # Sample for large N
        stat_sw, p_sw = stats.shapiro(s.sample(5000, random_state=42))

    skew = float(stats.skew(s))
    kurt = float(stats.kurtosis(s))
    
    # Ceiling effect: proportion at max scale value
    if max_scale_value is not None:
        ceiling_pct = float((s >= (max_scale_value - 1e-5)).sum() / n * 100)
    else:
        ceiling_pct = float((s == s.max()).sum() / n * 100)

    # Decision rule: normality violated if p < 0.05 or |skew| > 1.0
    normality_violated = bool(p_sw < 0.05 or abs(skew) > 1.0)
    
    if normality_violated:
        recommendation = "Non-parametric (Mann-Whitney U / Kruskal-Wallis / Spearman)"
    else:
        recommendation = "Parametric (Student's t-test / ANOVA / Pearson)"

    return {
        "dataset": dataset_name,
        "variable": variable_name,
        "class_group": str(class_label),
        "n": n,
        "mean": round(float(s.mean()), 3),
        "median": round(float(s.median()), 3),
        "std": round(float(s.std()), 3),
        "skewness": round(skew, 3),
        "kurtosis": round(kurt, 3),
        "shapiro_stat": round(float(stat_sw), 4),
        "shapiro_p": round(float(p_sw), 6),
        "normality_violated": normality_violated,
        "ceiling_pct": round(ceiling_pct, 2),
        "recommended_method": recommendation
    }


def run_full_assumption_diagnostics(
    df_jds: pd.DataFrame,
    df_sds: pd.DataFrame,
    df_ds: pd.DataFrame,
    df_aj: pd.DataFrame
) -> pd.DataFrame:
    """Run comprehensive assumption checks across all core analytical variables."""
    records = []

    # 1. JDS Skills (Overall and by Target Class)
    jds_skills = [
        "big_data_skills", "maths_stats_skills", "coding_skills",
        "ai_and_ml_skills", "dashboard_and_storytelling_skills"
    ]
    for sk in jds_skills:
        # Overall
        records.append(evaluate_distribution_assumptions(
            df_jds[sk], sk, "JDS Skill Traits", class_label="Overall (N=139)", max_scale_value=5.0
        ))
        # High hike
        records.append(evaluate_distribution_assumptions(
            df_jds[df_jds["salary_hike_high_or_low"] == 1][sk], sk, "JDS Skill Traits", class_label="High Hike (n=73)", max_scale_value=5.0
        ))
        # Low hike
        records.append(evaluate_distribution_assumptions(
            df_jds[df_jds["salary_hike_high_or_low"] == 0][sk], sk, "JDS Skill Traits", class_label="Low Hike (n=66)", max_scale_value=5.0
        ))

    # 2. SDS Traits (Overall and by Target Class)
    sds_traits = [
        "neuroticism", "extraversion", "openness_to_experience",
        "agreeableness", "conscientiousness"
    ]
    for tr in sds_traits:
        records.append(evaluate_distribution_assumptions(
            df_sds[tr], tr, "SDS Personality Traits", class_label="Overall (N=161)", max_scale_value=68.0
        ))
        records.append(evaluate_distribution_assumptions(
            df_sds[df_sds["success_classification_high_low"] == 1][tr], tr, "SDS Personality Traits", class_label="High Success (n=85)", max_scale_value=68.0
        ))
        records.append(evaluate_distribution_assumptions(
            df_sds[df_sds["success_classification_high_low"] == 0][tr], tr, "SDS Personality Traits", class_label="Low Success (n=76)", max_scale_value=68.0
        ))

    # 3. DataScience Jobs Continuous Salary & Experience
    for col in ["min_salary_lakh", "avg_salary_lakh", "max_salary_lakh", "min_experience", "num_of_jobs"]:
        records.append(evaluate_distribution_assumptions(
            df_ds[col], col, "DataScience Jobs", class_label="Overall (N=1,602)"
        ))

    # 4. Analytics Jobs Experience Midpoint
    records.append(evaluate_distribution_assumptions(
        df_aj["midpoint_experience"], "midpoint_experience", "Analytics Jobs", class_label="Overall (N=15,841)"
    ))

    return pd.DataFrame(records)
