"""
tests/test_final_submission.py
------------------------------
Final comprehensive verification test suite for the InsightPath submission package.
Verifies all deliverables across Phases 6, 7, 8, and 9.
"""

from pathlib import Path
import pytest
import pandas as pd


def test_final_reports_exist():
    md_p = Path("docs/phase9/FINAL_ROUND2_REPORT.md")
    docx_p = Path("outputs/reports/InsightPath_Rusty_Wolves_Final_Report.docx")
    exec_p = Path("docs/phase9/FINAL_EXECUTION_REPORT.md")

    assert md_p.exists() and md_p.stat().st_size > 1000
    assert docx_p.exists() and docx_p.stat().st_size > 1000
    assert exec_p.exists() and exec_p.stat().st_size > 1000


def test_final_presentation_exists():
    pptx_p = Path("outputs/reports/InsightPath_Rusty_Wolves_Final_Presentation.pptx")
    assert pptx_p.exists() and pptx_p.stat().st_size > 1000


def test_final_tables_exist_and_non_empty():
    final_dir = Path("outputs/tables/final")
    expected_tables = [
        "final_rq_traceability.csv",
        "final_hypothesis_traceability.csv",
        "final_evidence_to_recommendation.csv",
        "final_figure_index.csv",
        "final_table_index.csv",
        "final_model_index.csv",
        "final_claim_audit.csv",
        "final_artifact_index.csv"
    ]
    for table_name in expected_tables:
        p = final_dir / table_name
        assert p.exists(), f"Missing table: {table_name}"
        df = pd.read_csv(p)
        assert len(df) > 0, f"Table {table_name} is empty"


def test_figure_index_completeness():
    p = Path("outputs/tables/final/final_figure_index.csv")
    df = pd.read_csv(p)
    assert len(df) == 48, f"Expected exactly 48 figures, got {len(df)}"
    # Check that all png and svg files actually exist on disk
    for _, row in df.iterrows():
        png_p = Path(row["path_png"])
        svg_p = Path(row["path_svg"])
        assert png_p.exists(), f"Missing figure file: {png_p}"
        assert svg_p.exists(), f"Missing figure file: {svg_p}"


def test_claim_audit_safety():
    p = Path("outputs/tables/final/final_claim_audit.csv")
    df = pd.read_csv(p)
    assert len(df) >= 5
    for _, row in df.iterrows():
        status = row["wording_safety_status"]
        assert "VERIFIED" in status


def test_model_index_completeness():
    p = Path("outputs/tables/final/final_model_index.csv")
    df = pd.read_csv(p)
    assert len(df) >= 6
    champions = df[df["status"].str.contains("Champion")]
    assert len(champions) >= 2  # JDS and SDS champions
