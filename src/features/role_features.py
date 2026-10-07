"""
role_features.py
----------------
Reusable feature engineering module for mapping unstructured job designations (job_desig)
into 6 standardized role families:
Data Scientist, Data Analyst, Business Analyst, Data Engineer, BI Developer, and Non-Analytics/Other.
"""

import re
import pandas as pd


def map_single_role_family(title: str) -> str:
    """
    Map an unstructured job designation string into a standardized role family.
    Evaluates ordered regex patterns with strict precedence.
    Ambiguous or non-matching titles default to 'Non-Analytics/Other'.
    """
    if not isinstance(title, str) or not title.strip():
        return "Non-Analytics/Other"
        
    t = title.lower().strip()
    
    # 1. Data Scientist
    if re.search(r"\b(data scientist|machine learning|ml engineer|deep learning|ai scientist|ai engineer|nlp engineer)\b", t):
        return "Data Scientist"
    # 2. Data Engineer
    elif re.search(r"\b(data engineer|big data|etl|hadoop|data warehouse|spark developer|database engineer)\b", t):
        return "Data Engineer"
    # 3. BI Developer
    elif re.search(r"\b(bi developer|business intelligence|tableau|power bi|powerbi|dashboard|qlik|reporting analyst|bi analyst)\b", t):
        return "BI Developer"
    # 4. Data Analyst
    elif re.search(r"\b(data analyst|statistical analyst|analytics specialist|analytics consultant|quantitative analyst|marketing analytics|financial analytics|risk analyst)\b", t):
        return "Data Analyst"
    # 5. Business Analyst
    elif re.search(r"\b(business analyst|business analytics|process analyst|functional analyst|systems analyst)\b", t):
        return "Business Analyst"
    # 6. Non-Analytics/Other
    else:
        return "Non-Analytics/Other"


def map_role_families(series: pd.Series) -> pd.Series:
    """Vectorized mapping of job designation series into the 6 role families."""
    return series.apply(map_single_role_family)
