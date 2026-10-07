"""
run_phase5.py
-------------
Master orchestrator for Phase 5: Junior Data Scientist Skill Modeling & Interpretability.
Executes the full predictive pipeline end-to-end:
  1. Loads and validates primary (N=139) and sensitivity (N=137) datasets
  2. Audits contradictory duplicate ID 3291
  3. Constructs leakage-free pipelines across 6 candidate models + naive baseline
  4. Executes 5x5 Repeated Stratified K-Fold CV (25 validation splits)
  5. Evaluates out-of-fold performance metrics (ROC-AUC, Macro F1, Brier, etc.)
  6. Extracts interpretability artifacts (odds ratios, tree rules, permutation importance)
  7. Conducts error analysis and feature importance stability diagnostics
  8. Evaluates parsimony: Full 5-feature vs Reduced 2-feature models
  9. Evaluates sensitivity robustness on N=137 (robustness verdict)
  10. Exports all 24 CSV tables to outputs/tables/phase5/
  11. Generates Figures 23–32 (PNG & SVG) to outputs/figures/phase5/
  12. Serializes champion model and metadata to outputs/models/phase5/
  13. Enforces rigorous validation assertions
"""

import sys
import time
from pathlib import Path
import pandas as pd
import numpy as np

from src.modeling.jds.data import (
    JDS_FEATURES,
    JDS_REDUCED_FEATURES,
    load_jds_primary,
    load_jds_sensitivity,
    audit_jds_anomalies,
    build_dataset_summary_table
)
from src.modeling.jds.pipelines import (
    build_candidate_pipelines,
    build_model_configuration_table
)
from src.modeling.jds.cross_validation import (
    build_cv_configuration_table,
    evaluate_pipelines_cv
)
from src.modeling.jds.evaluation import (
    build_baseline_metrics_table,
    build_model_comparison_table,
    build_final_model_selection_table
)
from src.modeling.jds.interpretability import (
    extract_logistic_interpretability,
    extract_tree_rules,
    compute_validation_permutation_importance
)
from src.modeling.jds.error_analysis import run_error_analysis
from src.modeling.jds.sensitivity import (
    run_sensitivity_modeling,
    compare_sensitivity_coefficients,
    compare_sensitivity_feature_importance,
    evaluate_full_vs_reduced_features
)
from src.modeling.jds.reporting import (
    export_table,
    build_phase4_traceability_table,
    build_reproducibility_audit_table,
    build_validation_summary_table,
    generate_fig23_roc_curves,
    generate_fig24_performance_comparison,
    generate_fig25_logistic_odds_ratios,
    generate_fig26_tree_decision_rules,
    generate_fig27_permutation_importance,
    generate_fig28_importance_stability,
    generate_fig29_baseline_vs_models,
    generate_fig30_sensitivity_comparison,
    generate_fig31_confusion_matrix,
    generate_fig32_full_vs_reduced,
    serialize_champion_model
)


def run_phase5_pipeline():
    print("============================================================")
    print("STARTING PHASE 5: JDS SKILL MODELING & INTERPRETABILITY")
    print("============================================================")
    
    base_dir = Path("/Users/anmolsharma/Desktop/DataScienceTool")
    tables_dir = base_dir / "outputs" / "tables" / "phase5"
    figures_dir = base_dir / "outputs" / "figures" / "phase5"
    models_dir = base_dir / "outputs" / "models" / "phase5"
    
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)
    
    # -------------------------------------------------------------
    # STEP 1: Data Ingestion & Anomaly Audit
    # -------------------------------------------------------------
    print("\n[Step 1] Loading JDS analytical cohorts...")
    X_prim, y_prim, df_prim = load_jds_primary(base_dir)
    X_sens, y_sens, df_sens = load_jds_sensitivity(base_dir)
    
    print(f"  - Primary Cohort: N={len(X_prim)} (Features: {list(X_prim.columns)})")
    print(f"  - Sensitivity Cohort: N={len(X_sens)} (ID 3291 removed)")
    
    anomaly_audit = audit_jds_anomalies(df_prim, df_sens)
    print(f"  - Anomaly Audit: ID 3291 rows={anomaly_audit['id_3291_rows']}, conflicting targets={anomaly_audit['id_3291_conflicting_targets']}")
    
    df_dataset_summary = build_dataset_summary_table(df_prim, df_sens)
    export_table(df_dataset_summary, "phase5_dataset_summary.csv", tables_dir)
    print("  -> Exported Table 1: phase5_dataset_summary.csv")
    
    # -------------------------------------------------------------
    # STEP 2: Cross-Validation & Model Configurations
    # -------------------------------------------------------------
    print("\n[Step 2] Configuring Repeated Stratified K-Fold CV & Candidate Pipelines...")
    df_cv_config = build_cv_configuration_table(n_splits=5, n_repeats=5, random_state=42)
    export_table(df_cv_config, "phase5_cv_configuration.csv", tables_dir)
    print("  -> Exported Table 2: phase5_cv_configuration.csv")
    
    df_model_config = build_model_configuration_table()
    export_table(df_model_config, "phase5_model_configuration.csv", tables_dir)
    print("  -> Exported Table 3: phase5_model_configuration.csv")
    
    # -------------------------------------------------------------
    # STEP 3: Out-of-Sample Cross-Validation Execution
    # -------------------------------------------------------------
    print("\n[Step 3] Executing 5x5 Repeated Stratified CV across candidate models (25 splits)...")
    pipelines = build_candidate_pipelines(random_state=42)
    df_folds, df_oof, df_summary = evaluate_pipelines_cv(
        pipelines, X_prim, y_prim, n_splits=5, n_repeats=5, random_state=42
    )
    
    df_baseline = build_baseline_metrics_table(df_summary)
    export_table(df_baseline, "phase5_baseline_metrics.csv", tables_dir)
    print("  -> Exported Table 4: phase5_baseline_metrics.csv")
    
    export_table(df_summary, "phase5_model_performance.csv", tables_dir)
    print("  -> Exported Table 5: phase5_model_performance.csv")
    
    export_table(df_folds, "phase5_cv_fold_results.csv", tables_dir)
    print(f"  -> Exported Table 6: phase5_cv_fold_results.csv ({len(df_folds)} split evaluations)")
    
    export_table(df_oof, "phase5_oof_predictions.csv", tables_dir)
    print(f"  -> Exported Table 7: phase5_oof_predictions.csv ({len(df_oof)} predictions)")
    
    # -------------------------------------------------------------
    # STEP 4: Interpretability & Explainability
    # -------------------------------------------------------------
    print("\n[Step 4] Extracting interpretability artifacts (Odds Ratios, Tree Rules, Permutation Importance)...")
    df_coef, df_or, df_logit_stab = extract_logistic_interpretability(
        X_prim, y_prim, n_splits=5, n_repeats=5, random_state=42
    )
    export_table(df_coef, "phase5_logistic_coefficients.csv", tables_dir)
    export_table(df_or, "phase5_logistic_odds_ratios.csv", tables_dir)
    export_table(df_logit_stab, "phase5_logistic_stability.csv", tables_dir)
    print("  -> Exported Tables 8, 9, 10: phase5_logistic_coefficients/odds_ratios/stability.csv")
    
    df_tree_rules, df_tree_comp = extract_tree_rules(X_prim, y_prim, max_depth=3, random_state=42)
    export_table(df_tree_rules, "phase5_tree_rules.csv", tables_dir)
    export_table(df_tree_comp, "phase5_tree_complexity.csv", tables_dir)
    print("  -> Exported Tables 11, 12: phase5_tree_rules/complexity.csv")
    
    df_rf_perm, df_imp_stab = compute_validation_permutation_importance(
        X_prim, y_prim, n_splits=5, n_repeats=5, random_state=42
    )
    export_table(df_rf_perm, "phase5_rf_permutation_importance.csv", tables_dir)
    export_table(df_imp_stab, "phase5_feature_importance_stability.csv", tables_dir)
    print("  -> Exported Tables 13, 14: phase5_rf_permutation_importance/stability.csv")
    
    # -------------------------------------------------------------
    # STEP 5: Error Analysis & Parsimony
    # -------------------------------------------------------------
    print("\n[Step 5] Conducting out-of-fold error analysis & parsimony evaluation...")
    df_error_summary, error_meta = run_error_analysis(df_oof, X_prim, y_prim, model_name="Logistic_Regression_L2")
    export_table(df_error_summary, "phase5_error_analysis.csv", tables_dir)
    print(f"  -> Exported Table 15: phase5_error_analysis.csv (Overall error rate = {error_meta['overall_error_rate_pct']}%)")
    
    df_parsimony = evaluate_full_vs_reduced_features(X_prim, y_prim, random_state=42)
    export_table(df_parsimony, "phase5_full_vs_reduced_features.csv", tables_dir)
    print(f"  -> Exported Table 16: phase5_full_vs_reduced_features.csv (Retains {df_parsimony['pct_auc_retained'].iloc[0]}% AUC)")
    
    # -------------------------------------------------------------
    # STEP 6: Sensitivity Analysis on N=137
    # -------------------------------------------------------------
    print("\n[Step 6] Running sensitivity analysis on N=137 (ID 3291 excluded)...")
    sens_pipes = build_candidate_pipelines(random_state=42)
    df_sens_perf, _, _ = run_sensitivity_modeling(sens_pipes, X_sens, y_sens, df_summary)
    export_table(df_sens_perf, "phase5_sensitivity_model_performance.csv", tables_dir)
    print(f"  -> Exported Table 17: phase5_sensitivity_model_performance.csv (Verdict: {df_sens_perf['robustness_verdict'].iloc[0]})")
    
    df_sens_coef = compare_sensitivity_coefficients(X_prim, y_prim, X_sens, y_sens, random_state=42)
    export_table(df_sens_coef, "phase5_sensitivity_coefficients.csv", tables_dir)
    print("  -> Exported Table 18: phase5_sensitivity_coefficients.csv")
    
    df_sens_imp = compare_sensitivity_feature_importance(df_rf_perm, X_sens, y_sens, random_state=42)
    export_table(df_sens_imp, "phase5_sensitivity_feature_importance.csv", tables_dir)
    print("  -> Exported Table 19: phase5_sensitivity_feature_importance.csv")
    
    # -------------------------------------------------------------
    # STEP 7: Comparison, Traceability, Selection & Audits
    # -------------------------------------------------------------
    print("\n[Step 7] Generating model comparison, traceability, and final selection...")
    df_comparison = build_model_comparison_table(df_summary)
    export_table(df_comparison, "phase5_model_comparison.csv", tables_dir)
    print("  -> Exported Table 20: phase5_model_comparison.csv")
    
    df_traceability = build_phase4_traceability_table(df_coef, df_rf_perm)
    export_table(df_traceability, "phase5_phase4_traceability.csv", tables_dir)
    print("  -> Exported Table 21: phase5_phase4_traceability.csv")
    
    df_selection = build_final_model_selection_table(df_summary)
    export_table(df_selection, "phase5_final_model_selection.csv", tables_dir)
    print("  -> Exported Table 22: phase5_final_model_selection.csv")
    
    df_repro = build_reproducibility_audit_table()
    export_table(df_repro, "phase5_reproducibility_audit.csv", tables_dir)
    print("  -> Exported Table 23: phase5_reproducibility_audit.csv")
    
    df_val_summary = build_validation_summary_table()
    export_table(df_val_summary, "phase5_validation_summary.csv", tables_dir)
    print("  -> Exported Table 24: phase5_validation_summary.csv")
    
    # -------------------------------------------------------------
    # STEP 8: Publication Figure Generation (Figures 23–32)
    # -------------------------------------------------------------
    print("\n[Step 8] Rendering publication-quality figures (Figures 23–32 in PNG & SVG)...")
    generate_fig23_roc_curves(df_oof, figures_dir)
    print("  -> Generated Fig 23: fig23_model_roc_curves")
    generate_fig24_performance_comparison(df_summary, figures_dir)
    print("  -> Generated Fig 24: fig24_model_performance_comparison")
    generate_fig25_logistic_odds_ratios(df_or, df_logit_stab, figures_dir)
    print("  -> Generated Fig 25: fig25_logistic_odds_ratios")
    generate_fig26_tree_decision_rules(X_prim, y_prim, figures_dir)
    print("  -> Generated Fig 26: fig26_tree_decision_rules")
    generate_fig27_permutation_importance(df_rf_perm, figures_dir)
    print("  -> Generated Fig 27: fig27_permutation_feature_importance")
    generate_fig28_importance_stability(df_imp_stab, figures_dir)
    print("  -> Generated Fig 28: fig28_feature_importance_stability")
    generate_fig29_baseline_vs_models(df_comparison, figures_dir)
    print("  -> Generated Fig 29: fig29_baseline_vs_models")
    generate_fig30_sensitivity_comparison(df_sens_perf, figures_dir)
    print("  -> Generated Fig 30: fig30_sensitivity_model_comparison")
    generate_fig31_confusion_matrix(df_oof, figures_dir)
    print("  -> Generated Fig 31: fig31_confusion_matrix_best_model")
    generate_fig32_full_vs_reduced(df_parsimony, figures_dir)
    print("  -> Generated Fig 32: fig32_full_vs_reduced_features")
    
    # -------------------------------------------------------------
    # STEP 9: Model Serialization
    # -------------------------------------------------------------
    print("\n[Step 9] Serializing selected champion model pipeline...")
    champion_pipeline = build_candidate_pipelines(random_state=42)["Logistic_Regression_L2"]
    model_metadata = {
        "model_name": "Logistic_Regression_L2",
        "cohort": "JDS Primary Analytical Dataset (N=139)",
        "features": JDS_FEATURES,
        "target": "salary_hike_high_or_low",
        "random_state": 42,
        "validation_strategy": "RepeatedStratifiedKFold (5 Folds x 5 Repeats = 25 Splits)",
        "cv_mean_roc_auc": df_summary[df_summary["model_name"] == "Logistic_Regression_L2"]["roc_auc_mean"].iloc[0],
        "cv_mean_macro_f1": df_summary[df_summary["model_name"] == "Logistic_Regression_L2"]["macro_f1_mean"].iloc[0],
        "cv_mean_accuracy": df_summary[df_summary["model_name"] == "Logistic_Regression_L2"]["accuracy_mean"].iloc[0],
        "coefficients": dict(zip(JDS_FEATURES, df_coef["standardized_coef_beta"].tolist())),
        "odds_ratios": dict(zip(JDS_FEATURES, df_or["odds_ratio"].tolist()))
    }
    model_path = serialize_champion_model(champion_pipeline, X_prim, y_prim, models_dir, model_metadata)
    print(f"  -> Serialized champion pipeline to {model_path}")
    
    # -------------------------------------------------------------
    # STEP 10: Validation Assertions
    # -------------------------------------------------------------
    print("\n[Step 10] Running Phase 5 validation assertions...")
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
    for tbl in expected_tables:
        p = tables_dir / tbl
        assert p.exists() and p.stat().st_size > 0, f"Missing or empty table: {tbl}"
    print(f"  [PASS] All {len(expected_tables)} tables exist and verified non-empty.")
    
    expected_figs = [
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
    for fig_stem in expected_figs:
        png_p = figures_dir / f"{fig_stem}.png"
        svg_p = figures_dir / f"{fig_stem}.svg"
        assert png_p.exists() and png_p.stat().st_size > 0, f"Missing PNG: {png_p}"
        assert svg_p.exists() and svg_p.stat().st_size > 0, f"Missing SVG: {svg_p}"
    print(f"  [PASS] All {len(expected_figs)} figures exist in both PNG and SVG.")
    
    assert (models_dir / "jds_champion_logistic_l2.joblib").exists(), "Missing serialized model"
    assert (models_dir / "jds_champion_metadata.json").exists(), "Missing model metadata"
    print("  [PASS] Champion model artifacts verified on disk.")
    
    print("\n============================================================")
    print("PHASE 5 EXECUTION COMPLETE AND FULLY VALIDATED")
    print("============================================================")
    return True


if __name__ == "__main__":
    run_phase5_pipeline()
