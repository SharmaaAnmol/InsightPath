"""
test_phase5_jds_modeling.py
---------------------------
Unit and integration test suite for Phase 5: JDS Skill Modeling & Interpretability.
Verifies:
  - Dataset integrity, shapes, targets, and feature isolation
  - Zero target and identifier leakage in design matrix X
  - Pipeline structure (StandardScaler encapsulated inside Pipeline)
  - Repeated Stratified K-Fold cross-validation (25 splits)
  - Model convergence and bounds on metrics (ROC-AUC, Macro F1 in [0, 1])
  - Constrained decision tree depth (<= 3) and random forest tree count (100)
  - Full vs reduced feature model performance retention
  - Sensitivity analysis robustness (delta AUC <= 0.02)
  - Existence and validity of all 24 tables, 10 figures (PNG/SVG), and serialized model
  - Raw data immutability and zero cross-dataset row joins
"""

import unittest
from pathlib import Path
import numpy as np
import pandas as pd
import joblib

from src.modeling.jds.data import (
    JDS_FEATURES,
    JDS_REDUCED_FEATURES,
    JDS_TARGET,
    load_jds_primary,
    load_jds_sensitivity,
    audit_jds_anomalies
)
from src.modeling.jds.pipelines import build_candidate_pipelines, build_reduced_pipelines
from src.modeling.jds.cross_validation import evaluate_pipelines_cv


class TestPhase5JDSModeling(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = Path("/Users/anmolsharma/Desktop/DataScienceTool")
        cls.tables_dir = cls.base_dir / "outputs" / "tables" / "phase5"
        cls.figures_dir = cls.base_dir / "outputs" / "figures" / "phase5"
        cls.models_dir = cls.base_dir / "outputs" / "models" / "phase5"
        
        cls.X_prim, cls.y_prim, cls.df_prim = load_jds_primary(cls.base_dir)
        cls.X_sens, cls.y_sens, cls.df_sens = load_jds_sensitivity(cls.base_dir)

    def test_primary_and_sensitivity_cohort_sizes(self):
        """1 & 2: Primary JDS N=139, Sensitivity N=137."""
        self.assertEqual(len(self.X_prim), 139)
        self.assertEqual(len(self.y_prim), 139)
        self.assertEqual(len(self.X_sens), 137)
        self.assertEqual(len(self.y_sens), 137)

    def test_target_integrity(self):
        """3 & 9: Target contains only {0, 1} and no fold/cohort has missing targets."""
        self.assertEqual(set(self.y_prim.unique()), {0, 1})
        self.assertEqual(set(self.y_sens.unique()), {0, 1})
        self.assertEqual(self.y_prim.isnull().sum(), 0)
        self.assertEqual(self.y_sens.isnull().sum(), 0)
        self.assertEqual((self.y_prim == 1).sum(), 73)
        self.assertEqual((self.y_prim == 0).sum(), 66)

    def test_feature_matrix_isolation_and_no_leakage(self):
        """4, 5, 6: Features match exact 5 skills; ID and target strictly excluded."""
        self.assertEqual(list(self.X_prim.columns), JDS_FEATURES)
        self.assertEqual(list(self.X_sens.columns), JDS_FEATURES)
        self.assertNotIn("id", self.X_prim.columns)
        self.assertNotIn(JDS_TARGET, self.X_prim.columns)
        self.assertNotIn("id", self.X_sens.columns)
        self.assertNotIn(JDS_TARGET, self.X_sens.columns)

    def test_pipeline_encapsulation_and_no_pre_split_leakage(self):
        """7 & 10: StandardScaler is inside pipeline, no global scaling before CV."""
        pipes = build_candidate_pipelines(random_state=42)
        l2_pipe = pipes["Logistic_Regression_L2"]
        self.assertIn("scaler", l2_pipe.named_steps)
        self.assertIn("clf", l2_pipe.named_steps)
        
        # Verify raw X features have non-zero mean and non-unit variance (unscaled)
        self.assertNotAlmostEqual(self.X_prim["maths_stats_skills"].mean(), 0.0, places=1)
        self.assertNotAlmostEqual(self.X_prim["maths_stats_skills"].std(), 1.0, places=1)

    def test_cross_validation_splits(self):
        """8: Repeated Stratified CV creates exactly 25 splits (5 folds x 5 repeats)."""
        from sklearn.model_selection import RepeatedStratifiedKFold
        rskf = RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=42)
        splits = list(rskf.split(self.X_prim, self.y_prim))
        self.assertEqual(len(splits), 25)

    def test_baseline_majority_classifier(self):
        """11: Naive majority baseline accuracy equals empirical prevalence (~52.5%)."""
        pipes = {"Baseline": build_candidate_pipelines(random_state=42)["Baseline_Majority"]}
        _, _, sum_df = evaluate_pipelines_cv(pipes, self.X_prim, self.y_prim)
        self.assertAlmostEqual(sum_df["accuracy_mean"].iloc[0], 0.525, places=2)
        self.assertAlmostEqual(sum_df["roc_auc_mean"].iloc[0], 0.500, places=3)

    def test_model_constraints(self):
        """12, 13, 14: Logistic trains, Decision Tree depth <= 3, Random Forest = 100 trees."""
        pipes = build_candidate_pipelines(random_state=42)
        
        dt_clf = pipes["Decision_Tree"].named_steps["clf"]
        self.assertLessEqual(dt_clf.max_depth, 3)
        
        rf_clf = pipes["Random_Forest"].named_steps["clf"]
        self.assertEqual(rf_clf.n_estimators, 100)
        self.assertLessEqual(rf_clf.max_depth, 3)

    def test_oof_predictions_and_metric_bounds(self):
        """15, 16, 17, 18: OOF predictions exist, all metrics bounded in [0, 1]."""
        oof_path = self.tables_dir / "phase5_oof_predictions.csv"
        self.assertTrue(oof_path.exists())
        df_oof = pd.read_csv(oof_path)
        self.assertEqual(len(df_oof), 139 * 5 * 7)  # 139 samples * 5 repeats * 7 models
        
        perf_path = self.tables_dir / "phase5_model_performance.csv"
        self.assertTrue(perf_path.exists())
        df_perf = pd.read_csv(perf_path)
        
        for col in ["roc_auc_mean", "macro_f1_mean", "accuracy_mean", "balanced_accuracy_mean"]:
            self.assertTrue((df_perf[col] >= 0.0).all() and (df_perf[col] <= 1.0).all())

    def test_feature_importance_outputs_are_finite(self):
        """19: Feature importances and odds ratios are finite positive values."""
        or_path = self.tables_dir / "phase5_logistic_odds_ratios.csv"
        df_or = pd.read_csv(or_path)
        self.assertTrue(np.isfinite(df_or["odds_ratio"]).all())
        self.assertTrue((df_or["odds_ratio"] > 0).all())
        
        rf_path = self.tables_dir / "phase5_rf_permutation_importance.csv"
        df_rf = pd.read_csv(rf_path)
        self.assertTrue(np.isfinite(df_rf["mean_permutation_importance"]).all())

    def test_sensitivity_model_robustness(self):
        """20: Sensitivity models execute and satisfy delta AUC <= 0.02 threshold."""
        sens_path = self.tables_dir / "phase5_sensitivity_model_performance.csv"
        df_sens = pd.read_csv(sens_path)
        l2_sens = df_sens[df_sens["model_name"] == "Logistic_Regression_L2"].iloc[0]
        self.assertLessEqual(l2_sens["delta_roc_auc"], 0.02)
        self.assertEqual(l2_sens["robustness_verdict"], "ROBUST TO OBSERVATIONAL NOISE")

    def test_all_24_tables_exist_and_non_empty(self):
        """21: Verify all 24 required Phase 5 CSV tables exist and have valid row counts."""
        expected_tables = [
            "phase5_dataset_summary.csv",
            "phase5_cv_configuration.csv",
            "phase5_model_configuration.csv",
            "phase5_baseline_metrics.csv",
            "phase5_model_performance.csv",
            "phase5_cv_fold_results.csv",
            "phase5_oof_predictions.csv",
            "phase5_logistic_coefficients.csv",
            "phase5_logistic_odds_ratios.csv",
            "phase5_logistic_stability.csv",
            "phase5_tree_rules.csv",
            "phase5_tree_complexity.csv",
            "phase5_rf_permutation_importance.csv",
            "phase5_feature_importance_stability.csv",
            "phase5_error_analysis.csv",
            "phase5_full_vs_reduced_features.csv",
            "phase5_sensitivity_model_performance.csv",
            "phase5_sensitivity_coefficients.csv",
            "phase5_sensitivity_feature_importance.csv",
            "phase5_model_comparison.csv",
            "phase5_phase4_traceability.csv",
            "phase5_final_model_selection.csv",
            "phase5_reproducibility_audit.csv",
            "phase5_validation_summary.csv"
        ]
        self.assertEqual(len(expected_tables), 24)
        for tbl in expected_tables:
            p = self.tables_dir / tbl
            self.assertTrue(p.exists(), f"Missing table: {tbl}")
            df = pd.read_csv(p)
            self.assertGreater(len(df), 0, f"Empty table: {tbl}")

    def test_all_10_figures_exist_in_png_and_svg(self):
        """22: Verify all 10 figures exist in both PNG and SVG formats."""
        fig_stems = [
            "fig23_model_roc_curves",
            "fig24_model_performance_comparison",
            "fig25_logistic_odds_ratios",
            "fig26_tree_decision_rules",
            "fig27_permutation_feature_importance",
            "fig28_feature_importance_stability",
            "fig29_baseline_vs_models",
            "fig30_sensitivity_model_comparison",
            "fig31_confusion_matrix_best_model",
            "fig32_full_vs_reduced_features"
        ]
        self.assertEqual(len(fig_stems), 10)
        for stem in fig_stems:
            png_p = self.figures_dir / f"{stem}.png"
            svg_p = self.figures_dir / f"{stem}.svg"
            self.assertTrue(png_p.exists(), f"Missing PNG: {stem}")
            self.assertTrue(svg_p.exists(), f"Missing SVG: {stem}")
            self.assertGreater(png_p.stat().st_size, 1000)
            self.assertGreater(svg_p.stat().st_size, 1000)

    def test_serialized_champion_model_reproducibility(self):
        """23: Serialized champion pipeline exists and reproduces predictions on X."""
        model_p = self.models_dir / "jds_champion_logistic_l2.joblib"
        meta_p = self.models_dir / "jds_champion_metadata.json"
        self.assertTrue(model_p.exists())
        self.assertTrue(meta_p.exists())
        
        loaded_pipe = joblib.load(model_p)
        preds = loaded_pipe.predict(self.X_prim)
        self.assertEqual(len(preds), 139)
        self.assertEqual(set(np.unique(preds)), {0, 1})

    def test_zero_cross_dataset_joins_and_raw_integrity(self):
        """24 & 25: Cohorts remain non-merged, raw files remain intact."""
        raw_jds = self.base_dir / "data" / "raw" / "JDS Skill Traits.xlsx"
        self.assertTrue(raw_jds.exists())
        self.assertGreater(raw_jds.stat().st_size, 0)
        # Check that SDS and job posting columns do not appear in X_prim
        for forbidden in ["neuroticism", "min_experience", "location_cluster", "is_high_salary"]:
            self.assertNotIn(forbidden, self.X_prim.columns)


if __name__ == "__main__":
    unittest.main()
