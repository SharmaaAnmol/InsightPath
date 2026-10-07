"""
test_data_audit.py
------------------
Automated test suite verifying raw file integrity, loading capabilities,
profiling functions, and non-mutation guarantees.
Compatible with standard library unittest and pytest.
"""

import os
import unittest
import hashlib
import pandas as pd

from src.data.loaders import load_csv_dataset, load_excel_dataset, load_all_raw_datasets
from src.data.profiling import (
    profile_dataframe,
    profile_missing_values,
    profile_duplicates,
    profile_identifier,
    profile_numeric_columns,
    detect_potential_outliers,
    profile_categorical_columns,
    profile_target_distribution,
)


class TestDataAudit(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.raw_dir = "data/raw"
        cls.files = [
            "DataScience Jobs.csv",
            "Analytics Jobs.csv",
            "JDS Skill Traits.xlsx",
            "SDS Personality Traits.xlsx"
        ]
        
    def test_01_all_raw_files_exist_and_match_root(self):
        """Verify that all 4 raw datasets exist in data/raw/ and match root byte-for-byte."""
        for f in self.files:
            root_p = f
            raw_p = os.path.join(self.raw_dir, f)
            self.assertTrue(os.path.exists(root_p), f"Root file missing: {root_p}")
            self.assertTrue(os.path.exists(raw_p), f"Raw file missing: {raw_p}")
            
            with open(root_p, "rb") as fp1, open(raw_p, "rb") as fp2:
                h1 = hashlib.sha256(fp1.read()).hexdigest()
                h2 = hashlib.sha256(fp2.read()).hexdigest()
            self.assertEqual(h1, h2, f"Hash mismatch between root and data/raw for {f}")

    def test_02_datasets_load_successfully(self):
        """Verify that all four datasets load into pandas DataFrames without crashing."""
        datasets = load_all_raw_datasets(self.raw_dir)
        self.assertEqual(len(datasets), 4)
        
        # Check shapes
        self.assertEqual(datasets["DataScience Jobs"].shape, (1602, 8))
        self.assertEqual(datasets["Analytics Jobs"].shape, (15841, 8))
        self.assertEqual(datasets["JDS Skill Traits"].shape, (171, 7))
        self.assertEqual(datasets["SDS Personality Traits"].shape, (161, 7))

    def test_03_expected_columns_exist(self):
        """Verify that core expected columns exist across all datasets."""
        datasets = load_all_raw_datasets(self.raw_dir)
        
        # DataScience Jobs
        ds_cols = datasets["DataScience Jobs"].columns
        for c in ["reference_no", "company_name", "job_title", "min_experience", "avg_salary", "num_of_jobs"]:
            self.assertIn(c, ds_cols)
            
        # Analytics Jobs
        aj_cols = datasets["Analytics Jobs"].columns
        for c in ["s_no", "experience", "job_desig", "location", "salary", "key_skills"]:
            self.assertIn(c, aj_cols)
            
        # JDS
        jds_cols = datasets["JDS Skill Traits"].columns
        for c in ["id", "big_data_skills", "maths-stats_skills", "salary_hike_high_or_low"]:
            self.assertIn(c, jds_cols)
            
        # SDS
        sds_cols = datasets["SDS Personality Traits"].columns
        self.assertIn("id", [c.strip() for c in sds_cols])
        self.assertTrue(any("neuroticism" in c.lower() for c in sds_cols))

    def test_04_raw_datasets_remain_unmodified(self):
        """Verify that loading datasets does NOT alter the raw files on disk."""
        for f in self.files:
            raw_p = os.path.join(self.raw_dir, f)
            with open(raw_p, "rb") as fp:
                initial_hash = hashlib.sha256(fp.read()).hexdigest()
                
            # Perform read
            if f.endswith(".csv"):
                _ = load_csv_dataset(raw_p)
            else:
                _ = load_excel_dataset(raw_p)
                
            with open(raw_p, "rb") as fp:
                post_hash = hashlib.sha256(fp.read()).hexdigest()
            self.assertEqual(initial_hash, post_hash, f"Raw file modified on disk: {raw_p}")

    def test_05_missing_value_profiler_structure(self):
        """Verify that profile_missing_values returns expected columns and captures JDS null rows."""
        df_jds = load_all_raw_datasets(self.raw_dir)["JDS Skill Traits"]
        mv_df = profile_missing_values(df_jds, "JDS Skill Traits")
        
        expected_cols = [
            "dataset", "column", "actual_nan_count", "string_missing_count",
            "total_missing_count", "missing_percentage", "non_missing_count",
            "unique_non_missing_count", "missing_severity"
        ]
        for c in expected_cols:
            self.assertIn(c, mv_df.columns)
            
        # Exactly 32 null rows in JDS
        id_row = mv_df[mv_df["column"] == "id"].iloc[0]
        self.assertEqual(id_row["actual_nan_count"], 32)

    def test_06_duplicate_profiler_structure(self):
        """Verify duplicate profiler accurately identifies duplicate IDs in SDS and DataScience Jobs."""
        datasets = load_all_raw_datasets(self.raw_dir)
        
        # DataScience Jobs has 142 duplicate reference numbers
        dup_ds = profile_duplicates(datasets["DataScience Jobs"], "DataScience Jobs", "reference_no")
        self.assertEqual(dup_ds["duplicate_ids"], 142)
        self.assertEqual(dup_ds["exact_duplicate_rows"], 0)
        
        # Analytics Jobs has 0 duplicate s_no
        dup_aj = profile_duplicates(datasets["Analytics Jobs"], "Analytics Jobs", "s_no")
        self.assertEqual(dup_aj["duplicate_ids"], 0)
        self.assertEqual(dup_aj["exact_duplicate_rows"], 0)

    def test_07_target_balance_profiler(self):
        """Verify target distribution profiler correctly computes class counts and percentages."""
        datasets = load_all_raw_datasets(self.raw_dir)
        jds_tgt = profile_target_distribution(datasets["JDS Skill Traits"], "salary_hike_high_or_low", "JDS")
        
        self.assertEqual(jds_tgt["total_valid_records"], 139)
        self.assertEqual(jds_tgt["class_0_count"], 66)
        self.assertEqual(jds_tgt["class_1_count"], 73)
        self.assertAlmostEqual(jds_tgt["imbalance_ratio"], 1.106, places=2)


if __name__ == "__main__":
    unittest.main()
