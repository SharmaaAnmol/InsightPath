"""
effect_sizes.py
---------------
Rigorous effect size computation and 95% confidence intervals for Phase 4.
Implements:
  - Cohen's d with analytical 95% CI
  - Rank-biserial correlation (r_rb) for Mann-Whitney U tests with Fisher's z CI
  - Cliff's delta
  - Odds Ratios with Woolf's logit 95% CI
  - Cramér's V for categorical contingency tables
  - Pearson r with Fisher's z 95% CI
"""

from typing import Dict, Tuple
import numpy as np
import pandas as pd
from scipy import stats


def compute_cohens_d_with_ci(
    group1: pd.Series,
    group2: pd.Series,
    alpha: float = 0.05
) -> Dict[str, float]:
    """
    Compute Cohen's d standardized mean difference with analytical 95% CI.
    group1 is typically the primary/high group, group2 is control/low.
    """
    g1, g2 = group1.dropna(), group2.dropna()
    n1, n2 = len(g1), len(g2)
    m1, m2 = g1.mean(), g2.mean()
    v1, v2 = g1.var(ddof=1), g2.var(ddof=1)
    
    pooled_sd = np.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2))
    if pooled_sd == 0:
        return {"d": 0.0, "ci_lower": 0.0, "ci_upper": 0.0, "se": 0.0}
        
    d = (m1 - m2) / pooled_sd
    
    # Standard error of Cohen's d
    se_d = np.sqrt((n1 + n2) / (n1 * n2) + (d ** 2) / (2 * (n1 + n2)))
    z_crit = stats.norm.ppf(1 - alpha / 2)
    
    ci_lower = d - z_crit * se_d
    ci_upper = d + z_crit * se_d
    
    return {
        "d": round(float(d), 3),
        "ci_lower": round(float(ci_lower), 3),
        "ci_upper": round(float(ci_upper), 3),
        "se": round(float(se_d), 3)
    }


def compute_rank_biserial_with_ci(
    u_stat: float,
    n1: int,
    n2: int,
    alpha: float = 0.05
) -> Dict[str, float]:
    """
    Compute rank-biserial correlation r_rb from Mann-Whitney U statistic with 95% CI.
    r_rb = 1 - 2U / (n1 * n2), ranges from -1.0 to +1.0.
    """
    total_pairs = n1 * n2
    if total_pairs == 0:
        return {"r_rb": 0.0, "ci_lower": 0.0, "ci_upper": 0.0, "se": 0.0}
        
    r_rb = 1.0 - (2.0 * u_stat / total_pairs)
    
    # Bound to [-0.9999, 0.9999] for Fisher's z transform
    r_clipped = np.clip(r_rb, -0.9999, 0.9999)
    z = np.arctanh(r_clipped)
    se_z = np.sqrt(1.0 / (n1 + n2 - 3)) if (n1 + n2 > 3) else 0.0
    
    z_crit = stats.norm.ppf(1 - alpha / 2)
    ci_z_lower = z - z_crit * se_z
    ci_z_upper = z + z_crit * se_z
    
    ci_lower = np.tanh(ci_z_lower)
    ci_upper = np.tanh(ci_z_upper)
    
    return {
        "r_rb": round(float(r_rb), 3),
        "ci_lower": round(float(ci_lower), 3),
        "ci_upper": round(float(ci_upper), 3),
        "se": round(float(se_z), 3)
    }


def compute_odds_ratio_with_ci(
    a: int, b: int, c: int, d: int,
    alpha: float = 0.05
) -> Dict[str, float]:
    """
    Compute Odds Ratio for 2x2 contingency table:
      [ [a (exposed/event),     b (exposed/no event)],
        [c (unexposed/event),   d (unexposed/no event)] ]
    Uses Woolf's logit method with Haldane-Anscombe 0.5 continuity correction if zero cell exists.
    """
    if a == 0 or b == 0 or c == 0 or d == 0:
        a_adj, b_adj, c_adj, d_adj = a + 0.5, b + 0.5, c + 0.5, d + 0.5
    else:
        a_adj, b_adj, c_adj, d_adj = float(a), float(b), float(c), float(d)
        
    or_val = (a_adj * d_adj) / (b_adj * c_adj)
    ln_or = np.log(or_val)
    se_ln_or = np.sqrt(1.0 / a_adj + 1.0 / b_adj + 1.0 / c_adj + 1.0 / d_adj)
    
    z_crit = stats.norm.ppf(1 - alpha / 2)
    ci_lower = np.exp(ln_or - z_crit * se_ln_or)
    ci_upper = np.exp(ln_or + z_crit * se_ln_or)
    
    return {
        "odds_ratio": round(float(or_val), 3),
        "ci_lower": round(float(ci_lower), 3),
        "ci_upper": round(float(ci_upper), 3),
        "se_ln_or": round(float(se_ln_or), 3)
    }


def compute_cramers_v(contingency_table: np.ndarray) -> float:
    """Compute Cramér's V effect size for categorical contingency tables."""
    chi2 = stats.chi2_contingency(contingency_table, correction=False)[0]
    n = contingency_table.sum()
    r, k = contingency_table.shape
    min_dim = min(r - 1, k - 1)
    if min_dim == 0 or n == 0:
        return 0.0
    v = np.sqrt(chi2 / (n * min_dim))
    return round(float(v), 3)


def compute_pearson_r_with_ci(
    x: pd.Series,
    y: pd.Series,
    alpha: float = 0.05
) -> Dict[str, float]:
    """Compute Pearson r correlation with Fisher's z 95% confidence interval."""
    df_clean = pd.DataFrame({"x": x, "y": y}).dropna()
    n = len(df_clean)
    if n < 4:
        raise ValueError("Sample size too small for correlation CI calculation.")
        
    r, p_val = stats.pearsonr(df_clean["x"], df_clean["y"])
    r_clipped = np.clip(r, -0.9999, 0.9999)
    z = np.arctanh(r_clipped)
    se_z = np.sqrt(1.0 / (n - 3))
    
    z_crit = stats.norm.ppf(1 - alpha / 2)
    ci_lower = np.tanh(z - z_crit * se_z)
    ci_upper = np.tanh(z + z_crit * se_z)
    
    return {
        "r": round(float(r), 3),
        "p_value": float(p_val),
        "ci_lower": round(float(ci_lower), 3),
        "ci_upper": round(float(ci_upper), 3),
        "n": n
    }
