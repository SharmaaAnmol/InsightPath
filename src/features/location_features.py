"""
location_features.py
--------------------
Reusable feature engineering module for geographic location normalization.
Standardizes location strings and maps them deterministically into 7 primary macro clusters:
Bengaluru, Mumbai, NCR, Pune, Hyderabad, Chennai, and Other/Tier-2.
"""

from typing import Tuple
import pandas as pd


def clean_location_string(series: pd.Series) -> pd.Series:
    """Safely strip leading/trailing whitespace from location strings."""
    return series.astype(str).str.strip()


def map_single_location(loc_str: str) -> str:
    """
    Deterministic rule-based mapping of location strings into 7 macro clusters.
    Evaluates primary metro location (first token in multi-city strings),
    with full-string fallback.
    """
    if not isinstance(loc_str, str) or not loc_str.strip():
        return "Other/Tier-2"
        
    # Isolate primary location token before comma or slash
    primary = loc_str.split(",")[0].split("/")[0].strip().lower()
    
    # 1. Bengaluru / Bangalore
    if any(k in primary for k in ["bengaluru", "bangalore"]):
        return "Bengaluru"
    # 2. Mumbai / Navi Mumbai
    elif any(k in primary for k in ["mumbai", "navi mumbai", "thane"]):
        return "Mumbai"
    # 3. National Capital Region (NCR)
    elif any(k in primary for k in ["delhi", "gurgaon", "gurugram", "noida", "ncr", "faridabad", "ghaziabad"]):
        return "NCR"
    # 4. Pune
    elif "pune" in primary:
        return "Pune"
    # 5. Hyderabad / Secunderabad
    elif any(k in primary for k in ["hyderabad", "secunderabad"]):
        return "Hyderabad"
    # 6. Chennai
    elif "chennai" in primary:
        return "Chennai"
    else:
        # Full string fallback for multi-city mentions where primary was generic (e.g. 'India')
        full = loc_str.lower()
        if any(k in full for k in ["bengaluru", "bangalore"]):
            return "Bengaluru"
        elif any(k in full for k in ["mumbai", "navi mumbai"]):
            return "Mumbai"
        elif any(k in full for k in ["delhi", "gurgaon", "gurugram", "noida", "ncr"]):
            return "NCR"
        elif "pune" in full:
            return "Pune"
        elif "hyderabad" in full:
            return "Hyderabad"
        elif "chennai" in full:
            return "Chennai"
        else:
            return "Other/Tier-2"


def map_location_clusters(series: pd.Series) -> pd.Series:
    """Vectorized mapping of location series to the 7 macro clusters."""
    return series.apply(map_single_location)
