"""
load_raw.py
-----------
Loads raw datasets for Phase 2 while performing SHA-256 cryptographic verification.
Ensures that all source files remain 100% byte-for-byte identical before and after transformations.
"""

import os
import hashlib
import pandas as pd
from typing import Dict, Tuple

from src.data.loaders import load_csv_dataset, load_excel_dataset


RAW_FILES = [
    "DataScience Jobs.csv",
    "Analytics Jobs.csv",
    "JDS Skill Traits.xlsx",
    "SDS Personality Traits.xlsx"
]


def compute_file_hash(filepath: str) -> str:
    """Compute SHA-256 digest of a file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found for hash calculation: {filepath}")
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()


def verify_raw_integrity(raw_dir: str = "data/raw", project_root: str = ".") -> pd.DataFrame:
    """
    Verify that raw files exist and match between root and data/raw/.
    Returns verification summary DataFrame.
    """
    records = []
    for fname in RAW_FILES:
        root_path = os.path.join(project_root, fname)
        raw_path = os.path.join(raw_dir, fname)
        
        root_exists = os.path.exists(root_path)
        raw_exists = os.path.exists(raw_path)
        
        root_hash = compute_file_hash(root_path) if root_exists else None
        raw_hash = compute_file_hash(raw_path) if raw_exists else None
        
        is_identical = bool(root_hash and raw_hash and (root_hash == raw_hash))
        
        records.append({
            "filename": fname,
            "root_path": root_path,
            "raw_path": raw_path,
            "size_bytes": os.path.getsize(raw_path) if raw_exists else 0,
            "root_sha256": root_hash,
            "raw_sha256": raw_hash,
            "is_identical": is_identical,
            "status": "PASS" if is_identical else "FAIL"
        })
        
    df = pd.DataFrame(records)
    if not df["is_identical"].all():
        raise RuntimeError("FATAL: Raw file hash verification failed! Data integrity compromised.")
    return df


def load_raw_phase2(raw_dir: str = "data/raw") -> Dict[str, pd.DataFrame]:
    """Load raw datasets into memory as DataFrames without mutation."""
    # 1. Data Science Jobs
    df_ds = load_csv_dataset(os.path.join(raw_dir, "DataScience Jobs.csv"))
    
    # 2. Analytics Jobs
    df_aj = load_csv_dataset(os.path.join(raw_dir, "Analytics Jobs.csv"))
    
    # 3. JDS Skill Traits
    _, df_jds = load_excel_dataset(os.path.join(raw_dir, "JDS Skill Traits.xlsx"))
    
    # 4. SDS Personality Traits
    _, df_sds = load_excel_dataset(os.path.join(raw_dir, "SDS Personality Traits.xlsx"))
    
    return {
        "DataScience Jobs": df_ds,
        "Analytics Jobs": df_aj,
        "JDS Skill Traits": df_jds,
        "SDS Personality Traits": df_sds
    }
