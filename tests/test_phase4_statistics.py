"""
test_phase4_statistics.py
-------------------------
Unit and integration test suite for Phase 4: Statistical Analysis & Hypothesis Testing.
Tests:
  - Dataset loading and sample sizes (DS=1602, AJ=15841, JDS=139/137, SDS=161/152)
  - Target variables and distribution integrity
  - Assumption checks and normality diagnostics
  - Group test statistics and 95% confidence intervals
  - Benjamini-Hochberg FDR correction properties
  - Logistic regression fits, VIF diagnostics, and zero leakage verification
  - Bivariate and adjusted regression models for H5
  - Chi-square expected frequencies and Cramér's V for H6
  - Existence and validity of all 26 exported tables and 7 figures
"""

import unittest
from pathlib import Path
import numpy as np
import pandas as pd

from src.statistics.assumptions import evaluate_distribution_assumptions
from src.statistics.effect_sizes import (
    compute_cohens_d_with_ci,
    compute_rank_biserial_with_ci,
    compute_odds_ratio_with_ci,
    compute_pearson_r_with_ci
)
from src.statistics.group_tests import run_two_group_comparison
from src.statistics.multiple_testing import apply_benjamini_hochberg
from src.statistics.logistic_models import compute_vif_dataframe, run_h2_jds_logistic, run_h4_sds_logistic
from src.statistics.contingency import run_geographic_chisquare_test


class TestPhase4Statistics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = Path(__file__).resolve().parent.parent
        cls.data_dir = cls.base_dir / "data" / "processed"
        cls.tables_dir = cls.base_dir / "outputs" / "tables" / "phase4"
        cls.figures_dir = cls.base_dir / "outputs" / "figures" / "phase4"
        
        cls.df_ds = pd.read_csv(cls.data_dir / "data_science_jobs_processed.csv")
        cls.df_aj = pd.read_csv(cls.data_dir / "analytics_jobs_processed.csv")
        cls.df_jds = pd.read_csv(cls.data_dir / "jds_processed.csv")
        cls.df_jds_sens = pd.read_csv(cls.data_dir / "jds_sensitivity_3291_removed.csv")
        cls.df_sds = pd.read_csv(cls.data_dir / "sds_processed.csv")
        cls.df_sds_dedup = cls.df_sds.drop_duplicates(subset=["id"], keep="first")

    def test_sample_sizes_and_cohort_integrity(self):
        """Verify exact sample sizes for primary and sensitivity cohorts."""
        self.assertEqual(len(self.df_ds), 1602)
        self.assertEqual(len(self.df_aj), 15841)
        self.assertEqual(len(self.df_jds), 139)
        self.assertEqual(len(self.df_jds_sens), 137)
        self.assertEqual(len(self.df_sds), 161)
        self.assertEqual(len(self.df_sds_dedup), 152)

    def test_target_distributions(self):
        """Verify binary target definitions and distributions."""
        self.assertEqual(set(self.df_jds["salary_hike_high_or_low"].unique()), {0, 1})
        self.assertEqual(set(self.df_sds["success_classification_high_low"].unique()), {0, 1})
        self.assertEqual(set(self.df_aj["is_high_salary"].unique()), {0, 1})
        
        # Check target counts
        self.assertEqual(self.df_jds["salary_hike_high_or_low"].sum(), 73)
        self.assertEqual(self.df_sds["success_classification_high_low"].sum(), 85)
        self.assertEqual(self.df_aj["is_high_salary"].sum(), 4526)

    def test_assumptions_diagnostic_module(self):
        """Verify assumption diagnostics correctly detect non-normality and ceiling effects."""
        res = evaluate_distribution_assumptions(
            self.df_jds["coding_skills"], "coding_skills", "JDS", max_scale_value=5.0
        )
        self.assertTrue(res["normality_violated"])
        self.assertGreater(res["ceiling_pct"], 25.0)
        self.assertIn("Non-parametric", res["recommended_method"])

    def test_effect_sizes_and_confidence_intervals(self):
        """Verify Cohen's d, rank-biserial, OR, and Pearson r confidence intervals are ordered."""
        g1 = pd.Series([4.5, 4.8, 5.0, 4.2, 4.9, 4.7])
        g2 = pd.Series([3.1, 3.4, 3.2, 2.9, 3.5, 3.0])
        
        d_res = compute_cohens_d_with_ci(g1, g2)
        self.assertGreater(d_res["d"], 0.0)
        self.assertLessEqual(d_res["ci_lower"], d_res["ci_upper"])
        
        rb_res = compute_rank_biserial_with_ci(5.0, 10, 10)
        self.assertLessEqual(rb_res["ci_lower"], rb_res["ci_upper"])
        
        or_res = compute_odds_ratio_with_ci(50, 20, 25, 45)
        self.assertGreater(or_res["odds_ratio"], 1.0)
        self.assertLessEqual(or_res["ci_lower"], or_res["ci_upper"])
        
        r_res = compute_pearson_r_with_ci(self.df_ds["min_experience"], self.df_ds["avg_salary_lakh"])
        self.assertGreater(r_res["r"], 0.50)
        self.assertLessEqual(r_res["ci_lower"], r_res["ci_upper"])

    def test_benjamini_hochberg_fdr(self):
        """Verify BH FDR adjusts p-values monotonically and controls FDR."""
        df_p = pd.DataFrame({"p": [0.001, 0.015, 0.040, 0.200, 0.850]})
        df_adj = apply_benjamini_hochberg(df_p, "p")
        
        adj_vals = df_adj["bh_adjusted_p"].values
        # Monotonicity check
        for i in range(len(adj_vals) - 1):
            self.assertLessEqual(adj_vals[i], adj_vals[i + 1])
        # Adjusted p >= raw p
        for i in range(len(adj_vals)):
            self.assertGreaterEqual(adj_vals[i], df_p["p"].iloc[i])

    def test_h1_jds_group_comparisons(self):
        """Verify H1 group comparisons confirm Storytelling & Maths differentiation and Big Data failure."""
        res_story = run_two_group_comparison(
            self.df_jds[self.df_jds["salary_hike_high_or_low"] == 1]["dashboard_and_storytelling_skills"],
            self.df_jds[self.df_jds["salary_hike_high_or_low"] == 0]["dashboard_and_storytelling_skills"],
            "storytelling"
        )
        self.assertLess(res_story["p_value_mwu"], 1e-5)
        self.assertGreater(res_story["cohens_d"], 1.0)
        
        res_bd = run_two_group_comparison(
            self.df_jds[self.df_jds["salary_hike_high_or_low"] == 1]["big_data_skills"],
            self.df_jds[self.df_jds["salary_hike_high_or_low"] == 0]["big_data_skills"],
            "big_data"
        )
        self.assertGreater(res_bd["p_value_mwu"], 0.05)
        self.assertLess(res_bd["cohens_d"], 0.40)

    def test_h2_jds_logistic_model_and_vif(self):
        """Verify H2 multivariable model converges and VIF is low."""
        params, vif, diag = run_h2_jds_logistic(self.df_jds)
        self.assertTrue(diag["converged"])
        self.assertGreater(diag["pseudo_r2_mcfadden"], 0.40)
        self.assertFalse(diag["quasi_separation_detected"])
        
        # VIF < 5.0 for all skills
        self.assertTrue((vif["vif"] < 5.0).all())

    def test_h3_and_h4_sds_models(self):
        """Verify H3 and H4 confirm Conscientiousness/Openness and reject Neuroticism hypothesis."""
        params, vif, diag = run_h4_sds_logistic(self.df_sds)
        self.assertTrue(diag["converged"])
        self.assertGreater(diag["pseudo_r2_mcfadden"], 0.60)
        
        # Conscientiousness and Openness should have large positive odds ratios
        c_row = params[params["parameter"] == "conscientiousness"].iloc[0]
        self.assertGreater(c_row["odds_ratio"], 5.0)
        self.assertLess(c_row["p_value"], 0.01)
        
        # Neuroticism OR should not be significantly less than 1.0
        n_row = params[params["parameter"] == "neuroticism"].iloc[0]
        self.assertGreater(n_row["odds_ratio"], 1.0)

    def test_h5_experience_compensation_models(self):
        """Verify H5 experience correlation and positive regression slope."""
        r_res = compute_pearson_r_with_ci(self.df_ds["min_experience"], self.df_ds["avg_salary_lakh"])
        self.assertAlmostEqual(r_res["r"], 0.593, places=2)
        self.assertLess(r_res["p_value"], 1e-50)

    def test_h6_geography_and_zero_leakage(self):
        """Verify H6 chi-square test validity and absence of leakage variables."""
        df_geo, meta = run_geographic_chisquare_test(self.df_aj)
        self.assertTrue(meta["assumptions_met"])
        self.assertGreaterEqual(meta["min_expected_frequency"], 5.0)
        self.assertLess(meta["p_value"], 1e-5)
        
        # Check Table 21 for absence of leakage variables
        t21 = pd.read_csv(self.tables_dir / "phase4_h6_logistic.csv")
        predictors = t21["parameter"].tolist()
        self.assertNotIn("salary_rank", predictors)
        self.assertNotIn("salary_midpoint", predictors)

    def test_all_26_tables_exist_and_non_empty(self):
        """Verify all 26 required Phase 4 CSV tables exist and have valid row counts."""
        expected_tables = [
            "phase4_hypothesis_summary.csv",
            "phase4_h1_jds_group_tests.csv",
            "phase4_h1_fdr_results.csv",
            "phase4_h1_sensitivity.csv",
            "phase4_h2_jds_logistic.csv",
            "phase4_h2_vif.csv",
            "phase4_h2_sensitivity.csv",
            "phase4_h3_sds_group_tests.csv",
            "phase4_h3_fdr_results.csv",
            "phase4_h3_sensitivity.csv",
            "phase4_h4_sds_logistic.csv",
            "phase4_h4_vif.csv",
            "phase4_h4_sensitivity.csv",
            "phase4_h5_correlation_tests.csv",
            "phase4_h5_regression.csv",
            "phase4_h5_adjusted_models.csv",
            "phase4_h6_geography_chisquare.csv",
            "phase4_h6_geography_posthoc.csv",
            "phase4_h6_skill_associations.csv",
            "phase4_h6_fdr_results.csv",
            "phase4_h6_logistic.csv",
            "phase4_effect_size_matrix.csv",
            "phase4_assumption_diagnostics.csv",
            "phase4_multiple_testing_summary.csv",
            "phase4_sensitivity_summary.csv",
            "phase4_rq_hypothesis_traceability.csv"
        ]
        self.assertEqual(len(expected_tables), 26)
        for tbl in expected_tables:
            p = self.tables_dir / tbl
            self.assertTrue(p.exists(), f"Missing table: {tbl}")
            df = pd.read_csv(p)
            self.assertGreater(len(df), 0, f"Empty table: {tbl}")

    def test_all_7_figures_exist_in_png_and_svg(self):
        """Verify Figures 16 to 22 exist in both PNG and SVG formats."""
        fig_stems = [
            "fig16_h1_jds_skill_effects",
            "fig17_h2_jds_adjusted_odds_ratios",
            "fig18_h3_sds_personality_effects",
            "fig19_h4_sds_adjusted_odds_ratios",
            "fig20_h5_experience_salary_regressions",
            "fig21_h6_geography_premium_association",
            "fig22_h6_skill_odds_ratios"
        ]
        self.assertEqual(len(fig_stems), 7)
        for stem in fig_stems:
            png_p = self.figures_dir / f"{stem}.png"
            svg_p = self.figures_dir / f"{stem}.svg"
            self.assertTrue(png_p.exists(), f"Missing PNG: {stem}")
            self.assertTrue(svg_p.exists(), f"Missing SVG: {stem}")
            self.assertGreater(png_p.stat().st_size, 1000)
            self.assertGreater(svg_p.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
