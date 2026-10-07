"""
salary_features.py
------------------
Reusable feature engineering module for salary transformations.
Parses string currency notations with 'L' suffix to continuous float64 (Lakhs INR).
Computes absolute and relative salary spread metrics.
Maps discrete salary brackets to ordinal ranks and interval midpoints.
"""

from typing import Tuple
import numpy as np
import pandas as pd


def parse_lakhs_currency_string(series: pd.Series) -> pd.Series:
    """
    Parse strings with 'L' or 'l' suffix (e.g. '7.8L', '16.0L') to float64 Lakhs.
    Rejects malformed values by raising ValueError.
    """
    clean_series = series.astype(str).str.strip().str.replace(r"[Ll]$", "", regex=True)
    numeric_series = pd.to_numeric(clean_series, errors="raise").astype(float)
    return numeric_series


def compute_salary_spread(
    min_sal: pd.Series,
    avg_sal: pd.Series,
    max_sal: pd.Series
) -> Tuple[pd.Series, pd.Series]:
    """
    Compute absolute salary spread (max - min) and relative spread ratio (spread / avg).
    Handles zero division safely by returning 0.0 when avg_salary is zero.
    """
    spread = max_sal - min_sal
    # Safe division: where avg_sal > 0, spread / avg_sal; else 0.0
    spread_ratio = np.where(avg_sal > 0, spread / avg_sal, 0.0)
    return spread.round(3), pd.Series(spread_ratio, index=avg_sal.index).round(4)


# Ordered salary brackets dictionary for Analytics Jobs
SALARY_BRACKET_CONFIG = {
    "0to3": {"rank": 1, "midpoint": 1.5, "is_high": 0},
    "3to6": {"rank": 2, "midpoint": 4.5, "is_high": 0},
    "6to10": {"rank": 3, "midpoint": 8.0, "is_high": 0},
    "10to15": {"rank": 4, "midpoint": 12.5, "is_high": 0},
    "15to25": {"rank": 5, "midpoint": 20.0, "is_high": 1},
    "25to50": {"rank": 6, "midpoint": 37.5, "is_high": 1}
}


def transform_salary_brackets(series: pd.Series) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Transform discrete categorical salary brackets into:
    - salary_rank: integer factor (1 to 6)
    - salary_midpoint: continuous approximation in Lakhs INR
    - is_high_salary: binary flag (1 for 15to25 and 25to50, else 0)
    """
    ranks = []
    midpoints = []
    is_highs = []
    
    for val in series:
        val_str = str(val).strip()
        if val_str in SALARY_BRACKET_CONFIG:
            cfg = SALARY_BRACKET_CONFIG[val_str]
            ranks.append(cfg["rank"])
            midpoints.append(cfg["midpoint"])
            is_highs.append(cfg["is_high"])
        else:
            raise ValueError(f"Unknown discrete salary bracket encountered: '{val_str}'")
            
    idx = series.index
    return pd.Series(ranks, index=idx, dtype="int64"), pd.Series(midpoints, index=idx, dtype="float64"), pd.Series(is_highs, index=idx, dtype="int64")
