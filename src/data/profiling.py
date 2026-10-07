"""
profiling.py
------------
Reusable data profiling and diagnostic functions.
Computes comprehensive data type, missingness, duplicate, identifier,
numerical, categorical, outlier, and target distribution metrics.
"""

from typing import Dict, List, Optional, Any
import numpy as np
import pandas as pd


def profile_dataframe(df: pd.DataFrame, dataset_name: str) -> Dict[str, Any]:
    """Calculate high-level structural dimensions and memory metrics for a DataFrame."""
    mem_bytes = df.memory_usage(deep=True).sum()
    mem_mb = mem_bytes / (1024 * 1024)
    return {
        "dataset_name": dataset_name,
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "memory_usage_bytes": mem_bytes,
        "memory_usage_mb": round(mem_mb, 3),
        "columns": list(df.columns)
    }


def profile_missing_values(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    """
    Profile missing values and string representations of missingness across all columns.
    Does NOT replace or alter the underlying DataFrame.
    """
    missing_tokens = ["", " ", "na", "n/a", "null", "none", "-", "--", "unknown", "not available", "nan"]
    records = []
    total_len = len(df)
    
    for col in df.columns:
        s = df[col]
        actual_nan_count = s.isna().sum()
        
        # Check for string representation of missingness
        string_missing_count = 0
        if s.dtype == "object":
            str_vals = s.dropna().astype(str).str.strip().str.lower()
            string_missing_count = str_vals.isin(missing_tokens).sum()
            
        combined_missing = actual_nan_count + string_missing_count
        non_missing = total_len - combined_missing
        unique_non_missing = s.dropna().nunique()
        
        missing_pct = round((combined_missing / total_len) * 100, 3) if total_len > 0 else 0.0
        
        # Missing severity category
        if missing_pct == 0.0:
            severity = "0% (Complete)"
        elif missing_pct < 1.0:
            severity = "<1% (Negligible)"
        elif missing_pct <= 5.0:
            severity = "1-5% (Low)"
        elif missing_pct <= 20.0:
            severity = "5-20% (Moderate)"
        elif missing_pct <= 50.0:
            severity = "20-50% (High)"
        else:
            severity = ">50% (Severe)"
            
        records.append({
            "dataset": dataset_name,
            "column": col,
            "actual_nan_count": actual_nan_count,
            "string_missing_count": string_missing_count,
            "total_missing_count": combined_missing,
            "missing_percentage": missing_pct,
            "non_missing_count": non_missing,
            "unique_non_missing_count": unique_non_missing,
            "missing_severity": severity
        })
        
    res_df = pd.DataFrame(records)
    return res_df.sort_values("missing_percentage", ascending=False).reset_index(drop=True)


def profile_duplicates(df: pd.DataFrame, dataset_name: str, id_col: Optional[str] = None) -> Dict[str, Any]:
    """Calculate exact row duplicates, ID duplicates, and uniqueness ratios."""
    total_rows = len(df)
    exact_dups = df.duplicated().sum()
    exact_dup_pct = round((exact_dups / total_rows) * 100, 3) if total_rows > 0 else 0.0
    
    profile = {
        "dataset": dataset_name,
        "total_rows": total_rows,
        "exact_duplicate_rows": int(exact_dups),
        "exact_duplicate_pct": exact_dup_pct,
        "id_column": id_col,
        "unique_ids": None,
        "duplicate_ids": None,
        "id_uniqueness_ratio": None
    }
    
    if id_col and id_col in df.columns:
        s_id = df[id_col].dropna()
        n_unique_ids = s_id.nunique()
        n_dup_ids = len(s_id) - n_unique_ids
        uniqueness_ratio = round(n_unique_ids / len(s_id), 4) if len(s_id) > 0 else 0.0
        
        profile["unique_ids"] = int(n_unique_ids)
        profile["duplicate_ids"] = int(n_dup_ids)
        profile["id_uniqueness_ratio"] = float(uniqueness_ratio)
        
    return profile


def profile_identifier(df: pd.DataFrame, id_col: str, dataset_name: str) -> Dict[str, Any]:
    """Detailed audit of an identifier column."""
    if id_col not in df.columns:
        raise ValueError(f"Column '{id_col}' not found in {dataset_name}")
        
    s = df[id_col]
    total_len = len(s)
    missing_count = int(s.isna().sum())
    valid_s = s.dropna()
    
    # Check numeric conversion safely
    num_s = pd.to_numeric(valid_s, errors="coerce")
    is_numeric = num_s.notna().all()
    
    min_val = num_s.min() if is_numeric and len(num_s) > 0 else (valid_s.min() if len(valid_s) > 0 else None)
    max_val = num_s.max() if is_numeric and len(num_s) > 0 else (valid_s.max() if len(valid_s) > 0 else None)
    unique_count = int(valid_s.nunique())
    dup_count = int(valid_s.duplicated().sum())
    uniqueness_ratio = round(unique_count / len(valid_s), 4) if len(valid_s) > 0 else 0.0
    
    return {
        "dataset": dataset_name,
        "identifier_column": id_col,
        "data_type": str(s.dtype),
        "is_numeric": is_numeric,
        "total_records": total_len,
        "missing_count": missing_count,
        "unique_count": unique_count,
        "duplicate_count": dup_count,
        "uniqueness_ratio": uniqueness_ratio,
        "min_value": min_val,
        "max_value": max_val
    }


def profile_numeric_columns(df: pd.DataFrame, dataset_name: str, cols: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Compute comprehensive statistical summary metrics for numeric variables.
    Handles columns stored as numbers or numeric-convertible strings.
    """
    records = []
    target_cols = cols if cols is not None else [
        c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) or 
        pd.to_numeric(df[c].dropna(), errors="coerce").notna().all()
    ]
    
    for c in target_cols:
        s_raw = df[c]
        s_num = pd.to_numeric(s_raw, errors="coerce").dropna()
        if len(s_num) == 0:
            continue
            
        cnt = int(len(s_num))
        missing_cnt = int(s_raw.isna().sum() + (len(s_raw.dropna()) - len(s_num)))
        mean_val = float(s_num.mean())
        std_val = float(s_num.std()) if cnt > 1 else 0.0
        min_val = float(s_num.min())
        max_val = float(s_num.max())
        q1_val = float(s_num.quantile(0.25))
        med_val = float(s_num.median())
        q3_val = float(s_num.quantile(0.75))
        iqr_val = float(q3_val - q1_val)
        skew_val = float(s_num.skew()) if cnt > 2 else 0.0
        unique_cnt = int(s_num.nunique())
        
        records.append({
            "dataset": dataset_name,
            "column": c,
            "count": cnt,
            "missing_count": missing_cnt,
            "mean": round(mean_val, 3),
            "std": round(std_val, 3),
            "min": round(min_val, 3),
            "q1": round(q1_val, 3),
            "median": round(med_val, 3),
            "q3": round(q3_val, 3),
            "max": round(max_val, 3),
            "iqr": round(iqr_val, 3),
            "skewness": round(skew_val, 3),
            "unique_count": unique_cnt
        })
        
    return pd.DataFrame(records)


def detect_potential_outliers(df: pd.DataFrame, numeric_cols: List[str], dataset_name: str) -> pd.DataFrame:
    """
    Audit potential outliers using the Tukey IQR standard rule:
    Lower Bound = Q1 - 1.5 * IQR
    Upper Bound = Q3 + 1.5 * IQR
    Does NOT remove or alter outliers.
    """
    records = []
    for c in numeric_cols:
        s_num = pd.to_numeric(df[c], errors="coerce").dropna()
        if len(s_num) < 4:
            continue
            
        q1 = s_num.quantile(0.25)
        q3 = s_num.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        low_outliers = s_num[s_num < lower_bound]
        high_outliers = s_num[s_num > upper_bound]
        total_outliers = len(low_outliers) + len(high_outliers)
        outlier_pct = round((total_outliers / len(s_num)) * 100, 3)
        
        sample_low = sorted(low_outliers.unique().tolist())[:3]
        sample_high = sorted(high_outliers.unique().tolist(), reverse=True)[:3]
        
        records.append({
            "dataset": dataset_name,
            "column": c,
            "count": len(s_num),
            "q1": round(q1, 3),
            "q3": round(q3, 3),
            "iqr": round(iqr, 3),
            "lower_bound": round(lower_bound, 3),
            "upper_bound": round(upper_bound, 3),
            "low_outlier_count": len(low_outliers),
            "high_outlier_count": len(high_outliers),
            "total_outlier_count": total_outliers,
            "outlier_percentage": outlier_pct,
            "sample_extreme_values": str(sample_low + sample_high)
        })
        
    return pd.DataFrame(records)


def profile_categorical_columns(df: pd.DataFrame, dataset_name: str, max_cardinality: int = 1000) -> pd.DataFrame:
    """Audit categorical columns for uniqueness, top frequencies, and capitalization/whitespace issues."""
    records = []
    for c in df.columns:
        s = df[c].dropna().astype(str)
        if len(s) == 0:
            continue
            
        unique_cnt = s.nunique()
        # Evaluate whitespace and casing variability
        has_leading_trailing_ws = (s != s.str.strip()).any()
        cased_distinct = s.str.lower().nunique()
        casing_inconsistency = (unique_cnt != cased_distinct)
        
        top_val = s.value_counts().index[0] if unique_cnt > 0 else None
        top_freq = int(s.value_counts().iloc[0]) if unique_cnt > 0 else 0
        top_pct = round((top_freq / len(s)) * 100, 2) if len(s) > 0 else 0.0
        
        records.append({
            "dataset": dataset_name,
            "column": c,
            "total_valid_values": len(s),
            "unique_categories": unique_cnt,
            "whitespace_anomaly": has_leading_trailing_ws,
            "casing_inconsistency": casing_inconsistency,
            "most_frequent_value": str(top_val)[:50],
            "top_value_frequency": top_freq,
            "top_value_percentage": top_pct
        })
        
    return pd.DataFrame(records)


def profile_target_distribution(df: pd.DataFrame, target_col: str, dataset_name: str) -> Dict[str, Any]:
    """Audit target distribution, binary balance, and class imbalance ratio."""
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in {dataset_name}")
        
    s = pd.to_numeric(df[target_col], errors="coerce").dropna()
    val_counts = s.value_counts().to_dict()
    total_valid = len(s)
    
    classes = sorted(list(val_counts.keys()))
    class_0_cnt = int(val_counts.get(0.0, val_counts.get(0, 0)))
    class_1_cnt = int(val_counts.get(1.0, val_counts.get(1, 0)))
    
    pct_0 = round((class_0_cnt / total_valid) * 100, 2) if total_valid > 0 else 0.0
    pct_1 = round((class_1_cnt / total_valid) * 100, 2) if total_valid > 0 else 0.0
    
    majority_class = 1 if class_1_cnt >= class_0_cnt else 0
    minority_class = 0 if majority_class == 1 else 1
    imbalance_ratio = round(max(class_0_cnt, class_1_cnt) / max(1, min(class_0_cnt, class_1_cnt)), 3)
    
    return {
        "dataset": dataset_name,
        "target_column": target_col,
        "total_valid_records": total_valid,
        "class_0_count": class_0_cnt,
        "class_0_pct": pct_0,
        "class_1_count": class_1_cnt,
        "class_1_pct": pct_1,
        "majority_class": majority_class,
        "minority_class": minority_class,
        "imbalance_ratio": imbalance_ratio
    }
