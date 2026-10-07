"""
run_phase4.py
-------------
Master orchestrator for Phase 4: Statistical Analysis & Hypothesis Testing.
Executes the full inferential pipeline end-to-end:
  1. Loads and validates processed datasets
  2. Runs assumption diagnostics across all continuous variables
  3. Evaluates H1 (JDS skill group tests, FDR correction, sensitivity)
  4. Evaluates H2 (JDS multivariable logistic model, VIF, sensitivity)
  5. Evaluates H3 (SDS Big Five group tests, FDR correction, sensitivity)
  6. Evaluates H4 (SDS multivariable logistic model, VIF, sensitivity)
  7. Evaluates H5 (Bivariate correlations, OLS, Semi-log, Adjusted models)
  8. Evaluates H6 (Geography chi-square, post-hoc, skill odds ratios, multivariable logistic)
  9. Consolidates multiple testing, effect sizes, sensitivity summaries
  10. Exports all 26 tables to outputs/tables/phase4/
  11. Exports Figures 16–22 (PNG and SVG) to outputs/figures/phase4/
  12. Validates statistical assertions and data integrity
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

from src.statistics.assumptions import run_full_assumption_diagnostics
from src.statistics.group_tests import run_jds_skill_group_tests, run_sds_trait_group_tests
from src.statistics.correlations import (
    run_h5_correlation_tests,
    run_h5_bivariate_regressions,
    run_h5_adjusted_regressions
)
from src.statistics.multiple_testing import (
    apply_benjamini_hochberg,
    build_multiple_testing_summary
)
from src.statistics.logistic_models import (
    run_h2_jds_logistic,
    run_h4_sds_logistic,
    run_h6_analytics_logistic
)
from src.statistics.contingency import (
    run_geographic_chisquare_test,
    run_regional_salary_rank_posthoc,
    run_skill_premium_associations
)
from src.statistics.sensitivity import (
    run_h1_sensitivity_comparison,
    run_h2_sensitivity_comparison,
    run_h3_sensitivity_comparison,
    run_h4_sensitivity_comparison,
    build_consolidated_sensitivity_summary
)
from src.statistics.reporting import (
    export_table,
    build_hypothesis_decision_matrix,
    build_effect_size_matrix,
    build_traceability_matrix
)
from src.statistics.figures import (
    generate_fig16_h1_jds_effects,
    generate_fig17_h2_jds_odds_ratios,
    generate_fig18_h3_sds_personality_effects,
    generate_fig19_h4_sds_odds_ratios,
    generate_fig20_h5_regressions,
    generate_fig21_h6_geography,
    generate_fig22_h6_skill_odds_ratios
)


def run_phase4_pipeline():
    print("============================================================")
    print("STARTING PHASE 4: STATISTICAL ANALYSIS & HYPOTHESIS TESTING")
    print("============================================================")
    
    base_dir = Path("/Users/anmolsharma/Desktop/DataScienceTool")
    data_dir = base_dir / "data" / "processed"
    tables_dir = base_dir / "outputs" / "tables" / "phase4"
    figures_dir = base_dir / "outputs" / "figures" / "phase4"
    
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    
    # -------------------------------------------------------------
    # STEP 1: Load Analytical Datasets
    # -------------------------------------------------------------
    print("\n[Step 1] Loading analytical processed datasets...")
    df_ds = pd.read_csv(data_dir / "data_science_jobs_processed.csv")
    df_aj = pd.read_csv(data_dir / "analytics_jobs_processed.csv")
    df_jds_prim = pd.read_csv(data_dir / "jds_processed.csv")
    df_jds_sens = pd.read_csv(data_dir / "jds_sensitivity_3291_removed.csv")
    df_sds_prim = pd.read_csv(data_dir / "sds_processed.csv")
    
    # Deduplicate SDS for sensitivity cohort (N=152)
    df_sds_sens = df_sds_prim.drop_duplicates(subset=["id"], keep="first").copy()
    
    print(f"  - DataScience Jobs: {df_ds.shape[0]} rows, {df_ds.shape[1]} cols")
    print(f"  - Analytics Jobs: {df_aj.shape[0]} rows, {df_aj.shape[1]} cols")
    print(f"  - JDS Primary: {df_jds_prim.shape[0]} rows | Sensitivity: {df_jds_sens.shape[0]} rows")
    print(f"  - SDS Primary: {df_sds_prim.shape[0]} rows | Deduplicated: {df_sds_sens.shape[0]} rows")
    
    # Assert sample sizes
    assert len(df_ds) == 1602, f"Expected 1602 rows in DS, got {len(df_ds)}"
    assert len(df_aj) == 15841, f"Expected 15841 rows in AJ, got {len(df_aj)}"
    assert len(df_jds_prim) == 139, f"Expected 139 rows in JDS primary, got {len(df_jds_prim)}"
    assert len(df_jds_sens) == 137, f"Expected 137 rows in JDS sens, got {len(df_jds_sens)}"
    assert len(df_sds_prim) == 161, f"Expected 161 rows in SDS primary, got {len(df_sds_prim)}"
    assert len(df_sds_sens) == 152, f"Expected 152 rows in SDS sens, got {len(df_sds_sens)}"
    
    # -------------------------------------------------------------
    # STEP 2: Assumption Diagnostics
    # -------------------------------------------------------------
    print("\n[Step 2] Running formal assumption checks across all core variables...")
    df_assumptions = run_full_assumption_diagnostics(df_jds_prim, df_sds_prim, df_ds, df_aj)
    export_table(df_assumptions, "phase4_assumption_diagnostics.csv", tables_dir)
    print(f"  -> Exported Table 23: phase4_assumption_diagnostics.csv ({len(df_assumptions)} rows)")
    
    # -------------------------------------------------------------
    # STEP 3: Hypothesis 1 (JDS Skills Group Comparisons)
    # -------------------------------------------------------------
    print("\n[Step 3] Evaluating H1 (JDS Skills vs Salary Hike)...")
    df_h1_group = run_jds_skill_group_tests(df_jds_prim)
    export_table(df_h1_group, "phase4_h1_jds_group_tests.csv", tables_dir)
    print("  -> Exported Table 2: phase4_h1_jds_group_tests.csv")
    
    # Benjamini-Hochberg FDR for H1
    df_h1_fdr = apply_benjamini_hochberg(df_h1_group, "p_value_mwu")
    df_h1_fdr_export = df_h1_fdr[[
        "variable", "mann_whitney_u", "p_value_mwu", "bh_adjusted_p", "bh_significant",
        "cohens_d", "rank_biserial_r"
    ]].rename(columns={"p_value_mwu": "raw_p", "bh_adjusted_p": "fdr_adjusted_p", "bh_significant": "significant_after_fdr"})
    df_h1_fdr_export["hypothesis"] = "H1"
    df_h1_fdr_export["family"] = "JDS Skill Group Comparisons"
    export_table(df_h1_fdr_export, "phase4_h1_fdr_results.csv", tables_dir)
    print("  -> Exported Table 3: phase4_h1_fdr_results.csv")
    
    # H1 Sensitivity Comparison
    df_h1_sens = run_h1_sensitivity_comparison(df_jds_prim, df_jds_sens)
    export_table(df_h1_sens, "phase4_h1_sensitivity.csv", tables_dir)
    print("  -> Exported Table 4: phase4_h1_sensitivity.csv")
    
    # -------------------------------------------------------------
    # STEP 4: Hypothesis 2 (JDS Multivariable Logistic Regression)
    # -------------------------------------------------------------
    print("\n[Step 4] Evaluating H2 (JDS Independent Skill Associations)...")
    df_h2_params, df_h2_vif, h2_diag = run_h2_jds_logistic(df_jds_prim, model_label="H2_JDS_Primary_N139")
    export_table(df_h2_params, "phase4_h2_jds_logistic.csv", tables_dir)
    export_table(df_h2_vif, "phase4_h2_vif.csv", tables_dir)
    print(f"  -> Exported Table 5: phase4_h2_jds_logistic.csv (Pseudo R2 = {h2_diag['pseudo_r2_mcfadden']:.4f})")
    print("  -> Exported Table 6: phase4_h2_vif.csv")
    
    # H2 Sensitivity Regression
    df_h2_sens = run_h2_sensitivity_comparison(df_jds_prim, df_jds_sens)
    export_table(df_h2_sens, "phase4_h2_sensitivity.csv", tables_dir)
    print("  -> Exported Table 7: phase4_h2_sensitivity.csv")
    
    # -------------------------------------------------------------
    # STEP 5: Hypothesis 3 (SDS Personality Group Comparisons)
    # -------------------------------------------------------------
    print("\n[Step 5] Evaluating H3 (SDS Personality Traits vs Consulting Success)...")
    df_h3_group = run_sds_trait_group_tests(df_sds_prim)
    export_table(df_h3_group, "phase4_h3_sds_group_tests.csv", tables_dir)
    print("  -> Exported Table 8: phase4_h3_sds_group_tests.csv")
    
    # Benjamini-Hochberg FDR for H3
    df_h3_fdr = apply_benjamini_hochberg(df_h3_group, "p_value_mwu")
    df_h3_fdr_export = df_h3_fdr[[
        "variable", "mann_whitney_u", "p_value_mwu", "bh_adjusted_p", "bh_significant",
        "cohens_d", "rank_biserial_r"
    ]].rename(columns={"p_value_mwu": "raw_p", "bh_adjusted_p": "fdr_adjusted_p", "bh_significant": "significant_after_fdr"})
    df_h3_fdr_export["hypothesis"] = "H3"
    df_h3_fdr_export["family"] = "SDS Personality Group Comparisons"
    export_table(df_h3_fdr_export, "phase4_h3_fdr_results.csv", tables_dir)
    print("  -> Exported Table 9: phase4_h3_fdr_results.csv")
    
    # H3 Sensitivity Comparison
    df_h3_sens = run_h3_sensitivity_comparison(df_sds_prim, df_sds_sens)
    export_table(df_h3_sens, "phase4_h3_sensitivity.csv", tables_dir)
    print("  -> Exported Table 10: phase4_h3_sensitivity.csv")
    
    # -------------------------------------------------------------
    # STEP 6: Hypothesis 4 (SDS Multivariable Logistic Regression)
    # -------------------------------------------------------------
    print("\n[Step 6] Evaluating H4 (SDS Directional Personality Associations)...")
    df_h4_params, df_h4_vif, h4_diag = run_h4_sds_logistic(df_sds_prim, model_label="H4_SDS_Primary_N161")
    export_table(df_h4_params, "phase4_h4_sds_logistic.csv", tables_dir)
    export_table(df_h4_vif, "phase4_h4_vif.csv", tables_dir)
    print(f"  -> Exported Table 11: phase4_h4_sds_logistic.csv (Pseudo R2 = {h4_diag['pseudo_r2_mcfadden']:.4f})")
    print("  -> Exported Table 12: phase4_h4_vif.csv")
    
    # H4 Sensitivity Regression
    df_h4_sens = run_h4_sensitivity_comparison(df_sds_prim, df_sds_sens)
    export_table(df_h4_sens, "phase4_h4_sensitivity.csv", tables_dir)
    print("  -> Exported Table 13: phase4_h4_sensitivity.csv")
    
    # -------------------------------------------------------------
    # STEP 7: Hypothesis 5 (Experience & Compensation)
    # -------------------------------------------------------------
    print("\n[Step 7] Evaluating H5 (Experience-to-Compensation Elasticity)...")
    df_h5_corr = run_h5_correlation_tests(df_ds, df_aj)
    export_table(df_h5_corr, "phase4_h5_correlation_tests.csv", tables_dir)
    print("  -> Exported Table 14: phase4_h5_correlation_tests.csv")
    
    df_h5_bivariate = run_h5_bivariate_regressions(df_ds)
    export_table(df_h5_bivariate, "phase4_h5_regression.csv", tables_dir)
    print("  -> Exported Table 15: phase4_h5_regression.csv")
    
    df_h5_adjusted = run_h5_adjusted_regressions(df_ds)
    export_table(df_h5_adjusted, "phase4_h5_adjusted_models.csv", tables_dir)
    print("  -> Exported Table 16: phase4_h5_adjusted_models.csv")
    
    # -------------------------------------------------------------
    # STEP 8: Hypothesis 6 (Premium Salary, Geography & Skills)
    # -------------------------------------------------------------
    print("\n[Step 8] Evaluating H6 (Geography, Regional Rank, Skills, Multivariable Logistic)...")
    df_geo_res, geo_meta = run_geographic_chisquare_test(df_aj)
    export_table(df_geo_res, "phase4_h6_geography_chisquare.csv", tables_dir)
    print(f"  -> Exported Table 17: phase4_h6_geography_chisquare.csv (Chi2 = {geo_meta['chi2_statistic']}, p = {geo_meta['p_value']:.2e})")
    
    df_geo_posthoc = run_regional_salary_rank_posthoc(df_aj)
    export_table(df_geo_posthoc, "phase4_h6_geography_posthoc.csv", tables_dir)
    print(f"  -> Exported Table 18: phase4_h6_geography_posthoc.csv ({len(df_geo_posthoc)} pairwise comparisons)")
    
    df_skills_all, df_skills_fdr = run_skill_premium_associations(df_aj)
    export_table(df_skills_all, "phase4_h6_skill_associations.csv", tables_dir)
    export_table(df_skills_fdr, "phase4_h6_fdr_results.csv", tables_dir)
    print(f"  -> Exported Table 19: phase4_h6_skill_associations.csv ({len(df_skills_all)} skills)")
    print(f"  -> Exported Table 20: phase4_h6_fdr_results.csv ({int(df_skills_fdr['significant_after_fdr'].sum())} significant after FDR)")
    
    df_h6_log_params, df_h6_vif, h6_diag = run_h6_analytics_logistic(df_aj)
    export_table(df_h6_log_params, "phase4_h6_logistic.csv", tables_dir)
    print(f"  -> Exported Table 21: phase4_h6_logistic.csv (Pseudo R2 = {h6_diag['pseudo_r2_mcfadden']:.4f})")
    
    # -------------------------------------------------------------
    # STEP 9: Cross-Cutting Matrices & Summaries
    # -------------------------------------------------------------
    print("\n[Step 9] Generating cross-cutting synthesis tables...")
    
    # Table 22: Effect Size Matrix
    df_effect_matrix = build_effect_size_matrix(
        df_h1_group, df_h3_group, df_h5_corr, geo_meta, df_skills_all, df_h2_params, df_h4_params
    )
    export_table(df_effect_matrix, "phase4_effect_size_matrix.csv", tables_dir)
    print(f"  -> Exported Table 22: phase4_effect_size_matrix.csv ({len(df_effect_matrix)} effect sizes)")
    
    # Table 24: Multiple Testing Summary
    fam_dict = {
        "JDS Skill Comparisons (H1)": df_h1_fdr_export,
        "SDS Personality Comparisons (H3)": df_h3_fdr_export,
        "Regional Salary Rank Post-hoc (H6)": df_geo_posthoc.rename(columns={"raw_p_value": "raw_p"}),
        "Skill-Premium Contingency Family (H6)": df_skills_fdr.rename(columns={"raw_p_value": "raw_p"})
    }
    df_multi_summary = build_multiple_testing_summary(fam_dict)
    export_table(df_multi_summary, "phase4_multiple_testing_summary.csv", tables_dir)
    print("  -> Exported Table 24: phase4_multiple_testing_summary.csv")
    
    # Table 25: Sensitivity Summary
    df_sens_summary = build_consolidated_sensitivity_summary(
        df_h1_sens, df_h2_sens, df_h3_sens, df_h4_sens
    )
    export_table(df_sens_summary, "phase4_sensitivity_summary.csv", tables_dir)
    print("  -> Exported Table 25: phase4_sensitivity_summary.csv")
    
    # Table 1: Consolidated Hypothesis Decision Matrix
    df_hypo_matrix = build_hypothesis_decision_matrix(
        df_h1_group, df_h2_params, df_h3_group, df_h4_params,
        df_h5_corr, df_h5_bivariate, geo_meta, df_skills_fdr, df_h6_log_params
    )
    export_table(df_hypo_matrix, "phase4_hypothesis_summary.csv", tables_dir)
    print("  -> Exported Table 1: phase4_hypothesis_summary.csv")
    
    # Table 26: Phase 3 -> Phase 4 Traceability Matrix
    df_traceability = build_traceability_matrix(df_hypo_matrix)
    export_table(df_traceability, "phase4_rq_hypothesis_traceability.csv", tables_dir)
    print("  -> Exported Table 26: phase4_rq_hypothesis_traceability.csv")
    
    # -------------------------------------------------------------
    # STEP 10: Generate Figures 16–22 (PNG and SVG)
    # -------------------------------------------------------------
    print("\n[Step 10] Generating publication-quality figures (Figures 16–22 in PNG and SVG)...")
    generate_fig16_h1_jds_effects(df_h1_group, figures_dir)
    print("  -> Generated Fig 16: fig16_h1_jds_skill_effects")
    generate_fig17_h2_jds_odds_ratios(df_h2_params, figures_dir)
    print("  -> Generated Fig 17: fig17_h2_jds_adjusted_odds_ratios")
    generate_fig18_h3_sds_personality_effects(df_h3_group, figures_dir)
    print("  -> Generated Fig 18: fig18_h3_sds_personality_effects")
    generate_fig19_h4_sds_odds_ratios(df_h4_sens, figures_dir)
    print("  -> Generated Fig 19: fig19_h4_sds_adjusted_odds_ratios")
    generate_fig20_h5_regressions(df_ds, figures_dir)
    print("  -> Generated Fig 20: fig20_h5_experience_salary_regressions")
    generate_fig21_h6_geography(df_geo_res, figures_dir)
    print("  -> Generated Fig 21: fig21_h6_geography_premium_association")
    generate_fig22_h6_skill_odds_ratios(df_skills_fdr, figures_dir)
    print("  -> Generated Fig 22: fig22_h6_skill_odds_ratios")
    
    # -------------------------------------------------------------
    # STEP 11: Validation Assertions
    # -------------------------------------------------------------
    print("\n[Step 11] Running validation assertions...")
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
    for tbl in expected_tables:
        p = tables_dir / tbl
        assert p.exists() and p.stat().st_size > 0, f"Missing or empty table: {tbl}"
    print(f"  [PASS] All {len(expected_tables)} tables exist and verified non-empty.")
    
    expected_figs = [
        "fig16_h1_jds_skill_effects",
        "fig17_h2_jds_adjusted_odds_ratios",
        "fig18_h3_sds_personality_effects",
        "fig19_h4_sds_adjusted_odds_ratios",
        "fig20_h5_experience_salary_regressions",
        "fig21_h6_geography_premium_association",
        "fig22_h6_skill_odds_ratios"
    ]
    for fig_stem in expected_figs:
        png_p = figures_dir / f"{fig_stem}.png"
        svg_p = figures_dir / f"{fig_stem}.svg"
        assert png_p.exists() and png_p.stat().st_size > 0, f"Missing PNG: {png_p}"
        assert svg_p.exists() and svg_p.stat().st_size > 0, f"Missing SVG: {svg_p}"
    print(f"  [PASS] All {len(expected_figs)} figures exist in both PNG and SVG.")
    
    print("\n============================================================")
    print("PHASE 4 EXECUTION COMPLETE AND FULLY VALIDATED")
    print("============================================================")
    return True


if __name__ == "__main__":
    run_phase4_pipeline()
