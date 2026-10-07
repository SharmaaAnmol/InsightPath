"""
tests/test_phase8_framework.py
------------------------------
Automated test suite for Phase 8: Career-Readiness Framework Construction.
Verifies table generation, figure rendering, non-empty status,
and framework traceability.
"""

from pathlib import Path
import pytest
import pandas as pd


def test_phase8_tables_exist_and_non_empty():
    tables_dir = Path("outputs/tables/phase8")
    expected_tables = [
        "phase8_four_quadrant_matrix.csv",
        "phase8_career_stage_framework.csv",
        "phase8_competency_priorities.csv",
        "phase8_student_blueprint.csv",
        "phase8_university_blueprint.csv",
        "phase8_mentor_blueprint.csv",
        "phase8_employer_blueprint.csv",
        "phase8_evidence_to_action.csv",
        "phase8_success_indicators.csv",
        "phase8_framework_traceability.csv"
    ]
    for table_name in expected_tables:
        p = tables_dir / table_name
        assert p.exists(), f"Missing table: {table_name}"
        df = pd.read_csv(p)
        assert len(df) > 0, f"Table {table_name} is empty"


def test_phase8_figures_exist():
    figures_dir = Path("outputs/figures/phase8")
    expected_figs = [
        "fig45_four_quadrant_talent_matrix",
        "fig46_career_progression_roadmap",
        "fig47_stakeholder_action_map",
        "fig48_competency_priority_matrix"
    ]
    for fig_stem in expected_figs:
        png_p = figures_dir / f"{fig_stem}.png"
        svg_p = figures_dir / f"{fig_stem}.svg"
        assert png_p.exists(), f"Missing PNG: {fig_stem}.png"
        assert svg_p.exists(), f"Missing SVG: {fig_stem}.svg"


def test_four_quadrant_coverage():
    df = pd.read_csv("outputs/tables/phase8/phase8_four_quadrant_matrix.csv")
    assert len(df) == 4
    quad_ids = set(df["quadrant_id"])
    assert quad_ids == {"Q1", "Q2", "Q3", "Q4"}


def test_blueprints_coverage():
    for role in ["student", "university", "mentor", "employer"]:
        p = Path(f"outputs/tables/phase8/phase8_{role}_blueprint.csv")
        assert p.exists()
        df = pd.read_csv(p)
        assert len(df) >= 5
