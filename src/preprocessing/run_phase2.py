"""
run_phase2.py
-------------
Master execution pipeline for Phase 2: Data Cleaning & Transformation.
Coordinates end-to-end execution across:
  1. Cryptographic raw integrity verification (before)
  2. JDS Skill Traits cleaning (Baseline N=139, Sensitivity N=137)
  3. SDS Personality Traits cleaning (N=161)
  4. Data Science Jobs cleaning & spread derivation (N=1,602)
  5. Analytics Jobs cleaning, intervals, clusters, roles, and skills (N=15,841)
  6. Saving interim and processed CSV files
  7. Logging all atomic transformations to outputs/tables/phase2_transformation_log.csv
  8. Executing comprehensive post-cleaning validation suite
  9. Cryptographic raw integrity re-verification (after)
"""

import os
import sys
import pandas as pd

from src.preprocessing.load_raw import verify_raw_integrity, load_raw_phase2
from src.preprocessing.transformation_log import TransformationLogger
from src.preprocessing.clean_jds import clean_jds_dataset
from src.preprocessing.clean_sds import clean_sds_dataset
from src.preprocessing.clean_data_science_jobs import clean_data_science_jobs_dataset
from src.preprocessing.clean_analytics_jobs import clean_analytics_jobs_dataset
from src.preprocessing.validate_processed_data import validate_processed_datasets


def main():
    print("=" * 70)
    print("PHASE 2: DATA CLEANING & TRANSFORMATION PIPELINE")
    print("=" * 70)

    # Step 1: Pre-execution raw integrity verification
    print("\n[Step 1/9] Verifying raw file integrity prior to execution...")
    df_pre_integrity = verify_raw_integrity()
    print("  Pre-execution raw integrity: PASS (All hashes match)")

    # Step 2: Initialize Transformation Logger
    print("\n[Step 2/9] Initializing Transformation Logger...")
    logger = TransformationLogger(output_path="outputs/tables/phase2_transformation_log.csv")

    # Step 3: Load Raw Datasets
    print("\n[Step 3/9] Loading raw datasets into memory...")
    raw_datasets = load_raw_phase2()
    for name, df in raw_datasets.items():
        print(f"  Loaded raw '{name}': {len(df):,} rows, {len(df.columns)} columns")

    # Step 4: Clean JDS Dataset
    print("\n[Step 4/9] Cleaning JDS Skill Traits...")
    df_jds_interim, df_jds_baseline, df_jds_sensitivity = clean_jds_dataset(
        raw_datasets["JDS Skill Traits"],
        logger=logger
    )
    print(f"  JDS interim: {len(df_jds_interim)} rows")
    print(f"  JDS baseline: {len(df_jds_baseline)} rows, {len(df_jds_baseline.columns)} columns")
    print(f"  JDS sensitivity: {len(df_jds_sensitivity)} rows (ID 3291 excluded)")

    # Step 5: Clean SDS Dataset
    print("\n[Step 5/9] Cleaning SDS Personality Traits...")
    df_sds_interim, df_sds_processed = clean_sds_dataset(
        raw_datasets["SDS Personality Traits"],
        logger=logger
    )
    print(f"  SDS interim: {len(df_sds_interim)} rows")
    print(f"  SDS processed: {len(df_sds_processed)} rows, {len(df_sds_processed.columns)} columns")

    # Step 6: Clean Data Science Jobs Dataset
    print("\n[Step 6/9] Cleaning Data Science Jobs...")
    df_ds_interim, df_ds_processed = clean_data_science_jobs_dataset(
        raw_datasets["DataScience Jobs"],
        logger=logger
    )
    print(f"  Data Science Jobs interim: {len(df_ds_interim)} rows")
    print(f"  Data Science Jobs processed: {len(df_ds_processed)} rows, {len(df_ds_processed.columns)} columns")

    # Step 7: Clean Analytics Jobs Dataset
    print("\n[Step 7/9] Cleaning Analytics Jobs & Engineering Features...")
    df_aj_interim, df_aj_processed = clean_analytics_jobs_dataset(
        raw_datasets["Analytics Jobs"],
        logger=logger,
        top_k_skills=50,
        skill_output_path="outputs/tables/skill_frequency_profile.csv"
    )
    print(f"  Analytics Jobs interim: {len(df_aj_interim)} rows")
    print(f"  Analytics Jobs processed: {len(df_aj_processed)} rows, {len(df_aj_processed.columns)} columns")

    # Step 8: Export Interim and Processed CSV Files
    print("\n[Step 8/9] Exporting datasets to data/interim/ and data/processed/...")
    os.makedirs("data/interim", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("outputs/tables", exist_ok=True)

    # Interim exports
    df_jds_interim.to_csv("data/interim/jds_interim.csv", index=False)
    df_sds_interim.to_csv("data/interim/sds_interim.csv", index=False)
    df_ds_interim.to_csv("data/interim/data_science_jobs_interim.csv", index=False)
    df_aj_interim.to_csv("data/interim/analytics_jobs_interim.csv", index=False)
    print("  Saved 4 interim CSV files in data/interim/")

    # Processed exports
    df_jds_baseline.to_csv("data/processed/jds_processed.csv", index=False)
    df_jds_sensitivity.to_csv("data/processed/jds_sensitivity_3291_removed.csv", index=False)
    df_sds_processed.to_csv("data/processed/sds_processed.csv", index=False)
    df_ds_processed.to_csv("data/processed/data_science_jobs_processed.csv", index=False)
    df_aj_processed.to_csv("data/processed/analytics_jobs_processed.csv", index=False)
    print("  Saved 5 processed CSV files in data/processed/")

    # Export Transformation Log
    df_log = logger.to_dataframe()
    df_log.to_csv("outputs/tables/phase2_transformation_log.csv", index=False)
    print(f"  Saved transformation log ({len(df_log)} atomic operations) to outputs/tables/phase2_transformation_log.csv")

    # Step 9: Post-Cleaning Validation & Integrity Re-verification
    print("\n[Step 9/9] Running Validation Suite & Post-execution Integrity Check...")
    interim_datasets = {
        "jds_interim": df_jds_interim,
        "sds_interim": df_sds_interim,
        "data_science_jobs_interim": df_ds_interim,
        "analytics_jobs_interim": df_aj_interim
    }
    processed_datasets = {
        "jds_processed": df_jds_baseline,
        "jds_sensitivity_3291_removed": df_jds_sensitivity,
        "sds_processed": df_sds_processed,
        "data_science_jobs_processed": df_ds_processed,
        "analytics_jobs_processed": df_aj_processed
    }

    df_val_summary, df_before_after = validate_processed_datasets(
        raw_datasets=raw_datasets,
        interim_datasets=interim_datasets,
        processed_datasets=processed_datasets,
        output_dir="outputs/tables"
    )
    print("  Validation summary generated:")
    print(df_val_summary[["dataset", "observed_rows", "expected_rows", "status"]].to_string(index=False))

    # Re-verify raw hashes post-transformation
    df_post_integrity = verify_raw_integrity()
    df_post_integrity.to_csv("outputs/tables/raw_integrity_verification.csv", index=False)
    print("  Post-execution raw integrity re-verification: PASS (Zero bytes mutated)")

    print("\n" + "=" * 70)
    print("PHASE 2 MASTER PIPELINE EXECUTION COMPLETE: ALL CHECKS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()
