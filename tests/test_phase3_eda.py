"""
test_phase3_eda.py
------------------
Comprehensive unit and integration test suite for Phase 3: Purpose-Driven EDA.
Validates:
  1. Input processed dataset existence and row/column integrity.
  2. Target variable validity and binary domain restriction.
  3. All 15 figures exist in both PNG and SVG formats with non-trivial size.
  4. All 13 analytical tables exist in outputs/tables/phase3/ and are populated.
  5. Exhaustive RQ1-RQ9 coverage mapping.
  6. Data leakage safeguards: zero ID feature usage and target independence.
"""

import os
import unittest
import pandas as pd


class TestPhase3EDA(unittest.TestCase):
    """Test suite ensuring Phase 3 outputs adhere to analytical and governance standards."""

    @classmethod
    def setUpClass(cls):
        """Set up file paths and load metadata for Phase 3 tests."""
        cls.ds_path = "data/processed/data_science_jobs_processed.csv"
        cls.aj_path = "data/processed/analytics_jobs_processed.csv"
        cls.jds_path = "data/processed/jds_processed.csv"
        cls.jds_sens_path = "data/processed/jds_sensitivity_3291_removed.csv"
        cls.sds_path = "data/processed/sds_processed.csv"

        cls.tables_dir = "outputs/tables/phase3"
        cls.figs_dir = "outputs/figures/phase3"

        cls.df_ds = pd.read_csv(cls.ds_path)
        cls.df_aj = pd.read_csv(cls.aj_path)
        cls.df_jds = pd.read_csv(cls.jds_path)
        cls.df_jds_sens = pd.read_csv(cls.jds_sens_path)
        cls.df_sds = pd.read_csv(cls.sds_path)

    # -------------------------------------------------------------------------
    # 1. Dataset Integrity & Schema Checks
    # -------------------------------------------------------------------------
    def test_processed_dataset_row_counts(self):
        """Verify exact row counts across all analytical datasets."""
        self.assertEqual(len(self.df_ds), 1602)
        self.assertEqual(len(self.df_aj), 15841)
        self.assertEqual(len(self.df_jds), 139)
        self.assertEqual(len(self.df_jds_sens), 137)
        self.assertEqual(len(self.df_sds), 161)

    def test_key_numeric_columns_exist_and_numeric(self):
        """Verify presence and numeric data types for core analytical features."""
        # DataScience Jobs
        for col in ["min_salary_lakh", "avg_salary_lakh", "max_salary_lakh", "salary_spread_lakh", "min_experience"]:
            self.assertIn(col, self.df_ds.columns)
            self.assertTrue(pd.api.types.is_numeric_dtype(self.df_ds[col]))

        # Analytics Jobs
        for col in ["min_experience", "max_experience", "midpoint_experience", "salary_rank", "salary_midpoint"]:
            self.assertIn(col, self.df_aj.columns)
            self.assertTrue(pd.api.types.is_numeric_dtype(self.df_aj[col]))

        # JDS Skills
        for col in ["big_data_skills", "maths_stats_skills", "coding_skills", "ai_and_ml_skills", "dashboard_and_storytelling_skills"]:
            self.assertIn(col, self.df_jds.columns)
            self.assertTrue(pd.api.types.is_numeric_dtype(self.df_jds[col]))

        # SDS Traits
        for col in ["neuroticism", "extraversion", "openness_to_experience", "agreeableness", "conscientiousness"]:
            self.assertIn(col, self.df_sds.columns)
            self.assertTrue(pd.api.types.is_numeric_dtype(self.df_sds[col]))

    def test_target_variables_binary(self):
        """Verify all target variables are strictly binary in {0, 1}."""
        self.assertEqual(set(self.df_jds["salary_hike_high_or_low"].unique()), {0, 1})
        self.assertEqual(set(self.df_jds_sens["salary_hike_high_or_low"].unique()), {0, 1})
        self.assertEqual(set(self.df_sds["success_classification_high_low"].unique()), {0, 1})
        self.assertEqual(set(self.df_aj["is_high_salary"].unique()), {0, 1})

    # -------------------------------------------------------------------------
    # 2. Table Outputs Integrity
    # -------------------------------------------------------------------------
    def test_all_13_tables_exist_and_non_empty(self):
        """Verify all 13 analytical tables exist, are non-empty, and load properly."""
        expected_tables = [
            "phase3_descriptive_summary.csv",
            "phase3_role_demand.csv",
            "phase3_company_demand.csv",
            "phase3_salary_summary.csv",
            "phase3_experience_summary.csv",
            "phase3_location_summary.csv",
            "phase3_skill_frequency.csv",
            "phase3_skill_salary_comparison.csv",
            "phase3_jds_summary.csv",
            "phase3_sds_summary.csv",
            "phase3_correlation_summary.csv",
            "phase3_diagnostic_summary.csv",
            "phase3_rq_figure_map.csv"
        ]
        for tbl in expected_tables:
            tbl_path = os.path.join(self.tables_dir, tbl)
            self.assertTrue(os.path.exists(tbl_path), f"Missing table: {tbl}")
            self.assertGreater(os.path.getsize(tbl_path), 50, f"Table is empty: {tbl}")
            df = pd.read_csv(tbl_path)
            self.assertGreater(len(df), 0, f"Table contains 0 rows: {tbl}")

    def test_table_populations_reconcile(self):
        """Verify table population counts reconcile with underlying data."""
        # Location table
        df_loc = pd.read_csv(os.path.join(self.tables_dir, "phase3_location_summary.csv"))
        self.assertEqual(df_loc["vacancies_count"].sum(), 15841)
        self.assertEqual(len(df_loc), 7)

        # Role demand table
        df_role = pd.read_csv(os.path.join(self.tables_dir, "phase3_role_demand.csv"))
        self.assertEqual(df_role["postings_count"].sum(), 1602)
        self.assertEqual(len(df_role), 10)

    # -------------------------------------------------------------------------
    # 3. Figure Outputs Integrity
    # -------------------------------------------------------------------------
    def test_all_15_figures_exist_in_png_and_svg(self):
        """Verify all 15 publication figures exist in both high-res PNG and vector SVG formats."""
        for i in range(1, 16):
            prefix = f"fig{i:02d}"
            png_matches = [f for f in os.listdir(self.figs_dir) if f.startswith(prefix) and f.endswith(".png")]
            svg_matches = [f for f in os.listdir(self.figs_dir) if f.startswith(prefix) and f.endswith(".svg")]
            self.assertEqual(len(png_matches), 1, f"Missing PNG for {prefix}")
            self.assertEqual(len(svg_matches), 1, f"Missing SVG for {prefix}")

            png_file = os.path.join(self.figs_dir, png_matches[0])
            svg_file = os.path.join(self.figs_dir, svg_matches[0])
            self.assertGreater(os.path.getsize(png_file), 5000, f"PNG figure too small: {png_matches[0]}")
            self.assertGreater(os.path.getsize(svg_file), 1000, f"SVG figure too small: {svg_matches[0]}")

    # -------------------------------------------------------------------------
    # 4. Research Question Coverage
    # -------------------------------------------------------------------------
    def test_rq_coverage_map_complete(self):
        """Verify all research questions RQ1–RQ9 have documented mappings and limitations."""
        rq_map_path = os.path.join(self.tables_dir, "phase3_rq_figure_map.csv")
        df_rq = pd.read_csv(rq_map_path)
        self.assertEqual(len(df_rq), 9)
        for i in range(1, 10):
            rq_str = f"RQ{i}:"
            self.assertTrue(any(rq_str in row for row in df_rq["research_question"]))

    # -------------------------------------------------------------------------
    # 5. Data Leakage & Methodological Safeguards
    # -------------------------------------------------------------------------
    def test_no_identifier_used_as_explanatory_variable(self):
        """Verify identifier columns are excluded from explanatory feature listings."""
        df_diag = pd.read_csv(os.path.join(self.tables_dir, "phase3_diagnostic_summary.csv"))
        excluded_ids = {"id", "reference_no", "s_no"}
        for _, row in df_diag.iterrows():
            if "Target Leakage" in row["diagnostic_type"] or "Collinearity" in row["diagnostic_type"]:
                continue
            self.assertNotIn(row["feature"], excluded_ids)

    def test_target_leakage_safeguard_enforced(self):
        """Verify salary_rank and salary_midpoint are documented as leaked predictors for is_high_salary."""
        df_diag = pd.read_csv(os.path.join(self.tables_dir, "phase3_diagnostic_summary.csv"))
        leakage_rows = df_diag[df_diag["diagnostic_type"] == "Direct Target Leakage"]
        self.assertEqual(len(leakage_rows), 1)
        self.assertIn("NEVER include salary_rank", leakage_rows.iloc[0]["implication"])


if __name__ == "__main__":
    unittest.main()
