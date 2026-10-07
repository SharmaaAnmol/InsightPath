"""
src/framework/run_phase8.py
---------------------------
Master runner for Phase 8: Career-Readiness Framework Construction.
Orchestrates table generation, publication figure rendering, and artifact verification.
"""

from pathlib import Path
from src.framework.quadrant_matrix import build_four_quadrant_tables
from src.framework.blueprints import build_blueprint_tables
from src.framework.reporting import export_phase8_tables, generate_phase8_figures


def run_phase8_pipeline():
    print("================================================================================")
    print("STARTING PHASE 8: CAREER-READINESS FRAMEWORK & STAKEHOLDER BLUEPRINTS")
    print("================================================================================")

    base_dir = Path("/Users/anmolsharma/Desktop/DataScienceTool")
    tables_dir = base_dir / "outputs" / "tables" / "phase8"
    figures_dir = base_dir / "outputs" / "figures" / "phase8"

    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    # 1. Generate Tables
    print("\n[Step 1] Constructing all 10 framework and blueprint tables...")
    tables = {}
    tables.update(build_four_quadrant_tables())
    tables.update(build_blueprint_tables())
    export_phase8_tables(tables, tables_dir)

    # 2. Render Figures
    print("\n[Step 2] Rendering publication figures (Figures 45 - 48 in PNG & SVG)...")
    generate_phase8_figures(figures_dir)

    # 3. Assert Integrity
    print("\n[Step 3] Verifying completeness of all Phase 8 deliverables...")
    for filename in tables.keys():
        p = tables_dir / filename
        assert p.exists(), f"Missing table {filename}"
        assert p.stat().st_size > 0, f"Empty table {filename}"

    for fig_id in ["fig45_four_quadrant_talent_matrix", "fig46_career_progression_roadmap", "fig47_stakeholder_action_map", "fig48_competency_priority_matrix"]:
        assert (figures_dir / f"{fig_id}.png").exists(), f"Missing PNG {fig_id}"
        assert (figures_dir / f"{fig_id}.svg").exists(), f"Missing SVG {fig_id}"

    print("\n================================================================================")
    print("PHASE 8 EXECUTION COMPLETE: All 10 tables and 4 figures generated and verified!")
    print("================================================================================")
    return True


if __name__ == "__main__":
    run_phase8_pipeline()
