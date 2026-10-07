"""
experience_features.py
----------------------
Reusable feature engineering module for parsing experience strings.
Extracts lower bound, upper bound, and midpoint experience from string intervals (e.g. '6-10 yrs').
Validates that min_experience <= max_experience.
"""

import re
from typing import Tuple
import pandas as pd


def parse_experience_interval(series: pd.Series) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Parse experience strings following 'X-Y yrs' into:
    - min_experience: integer lower bound
    - max_experience: integer upper bound
    - midpoint_experience: float midpoint = (min + max) / 2.0
    
    Raises ValueError if any row fails pattern matching or has min > max.
    """
    pattern = re.compile(r"(\d+)\s*-\s*(\d+)")
    min_vals = []
    max_vals = []
    mid_vals = []
    
    for idx, val in series.items():
        val_str = str(val).strip()
        match = pattern.search(val_str)
        if not match:
            raise ValueError(f"Experience parsing exception at row index {idx}: '{val_str}'")
            
        min_e = int(match.group(1))
        max_e = int(match.group(2))
        
        if min_e > max_e:
            raise ValueError(f"Invalid experience ordering at row index {idx}: min={min_e} > max={max_e} in '{val_str}'")
            
        min_vals.append(min_e)
        max_vals.append(max_e)
        mid_vals.append((min_e + max_e) / 2.0)
        
    idx_s = series.index
    return (
        pd.Series(min_vals, index=idx_s, dtype="int64"),
        pd.Series(max_vals, index=idx_s, dtype="int64"),
        pd.Series(mid_vals, index=idx_s, dtype="float64")
    )
