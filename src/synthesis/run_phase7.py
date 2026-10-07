"""
src/synthesis/run_phase7.py
---------------------------
Master execution runner for Phase 7: Cross-Dataset Analytical Synthesis.
Orchestrates table generation, figure rendering, and consistency validation.
"""

from pathlib import Path
import pandas as pd

from src.synthesis.triangulation import build_all_phase7_synthesis_tables
from src.synthesis.reporting import export_phase7_tables, generate_phase7_figures


def run_phase7_pipeline():
    print("================================================================================")
    print("STARTING PHASE 7: CROSS-DATASET ANALYTICAL SYNTHESIS (METHODOLOGICAL TRIANGULATION)")
    print("================================================================================")

    base_dir = Path("/Users/anmolsharma/Desktop/DataScienceTool")
    tables_dir = base_dir / "outputs" / "tables" / "phase7"
    figures_dir = base_dir / "outputs" / "figures" / "phase7"

    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    # 1. Generate Synthesis Tables
    print("\n[Step 1] Constructing all 9 synthesis tables across the 4 evidence layers...")
    tables = build_all_phase7_synthesis_tables()
    export_phase7_tables(tables, tables_dir)

    # 2. Render Figures
    print("\n[Step 2] Rendering publication figures (Figures 41 - 44 in PNG & SVG)...")
    generate_phase7_figures(figures_dir)

    # 3. Assert Integrity
    print("\n[Step 3] Verifying artifact completeness and non-empty status...")
    for filename in tables.keys():
        p = tables_dir / filename
        assert p.exists(), f"Missing table {filename}"
        assert p.stat().st_size > 0, f"Empty table {filename}"

    for fig_id in ["fig41_career_stage_evidence_map", "fig42_market_skill_progression", "fig43_skill_to_career_stage_matrix", "fig44_evidence_strength_matrix"]:
        assert (figures_dir / f"{fig_id}.png").exists(), f"Missing PNG {fig_id}"
        assert (figures_dir / f"{fig_id}.svg").exists(), f"Missing SVG {fig_id}"

    print("\n================================================================================")
    print("PHASE 7 EXECUTION COMPLETE: All 9 tables and 4 figures generated and verified!")
    print("================================================================================")
    return True


if __name__ == "__main__":
    run_phase7_pipeline()
