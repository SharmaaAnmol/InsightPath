"""
tests/test_phase7_synthesis.py
------------------------------
Automated test suite for Phase 7: Cross-Dataset Analytical Synthesis.
Verifies table generation, figure rendering, non-empty status,
and compliance with the no-row-merge methodological triangulation principle.
"""

from pathlib import Path
import pytest
import pandas as pd


def test_phase7_tables_exist_and_non_empty():
    tables_dir = Path("outputs/tables/phase7")
    expected_tables = [
        "phase7_evidence_matrix.csv",
        "phase7_market_skill_matrix.csv",
        "phase7_career_stage_matrix.csv",
        "phase7_gap_analysis.csv",
        "phase7_skill_progression_map.csv",
        "phase7_evidence_strength.csv",
        "phase7_rq_synthesis.csv",
        "phase7_phase6_phase5_traceability.csv",
        "phase7_recommendation_evidence.csv"
    ]
    for table_name in expected_tables:
        p = tables_dir / table_name
        assert p.exists(), f"Missing table: {table_name}"
        df = pd.read_csv(p)
        assert len(df) > 0, f"Table {table_name} is empty"


def test_phase7_figures_exist():
    figures_dir = Path("outputs/figures/phase7")
    expected_figs = [
        "fig41_career_stage_evidence_map",
        "fig42_market_skill_progression",
        "fig43_skill_to_career_stage_matrix",
        "fig44_evidence_strength_matrix"
    ]
    for fig_stem in expected_figs:
        png_p = figures_dir / f"{fig_stem}.png"
        svg_p = figures_dir / f"{fig_stem}.svg"
        assert png_p.exists(), f"Missing PNG: {fig_stem}.png"
        assert svg_p.exists(), f"Missing SVG: {fig_stem}.svg"


def test_no_row_level_merge_integrity():
    """
    Confirms that all four underlying analytical datasets remain unmerged
    and retain their pristine observed row counts.
    """
    ds_path = Path("data/processed/data_science_jobs_processed.csv")
    aj_path = Path("data/processed/analytics_jobs_processed.csv")
    jds_path = Path("data/processed/jds_processed.csv")
    sds_path = Path("data/processed/sds_processed.csv")

    assert len(pd.read_csv(ds_path)) == 1602
    assert len(pd.read_csv(aj_path)) == 15841
    assert len(pd.read_csv(jds_path)) == 139
    assert len(pd.read_csv(sds_path)) == 161
