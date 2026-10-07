"""
src/framework/reporting.py
--------------------------
Reporting and publication figure generation for Phase 8: Career-Readiness Framework Construction.
Exports all 10 framework CSV tables and renders Figures 45 - 48 (PNG & SVG).
"""

from pathlib import Path
from typing import Dict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def export_phase8_tables(tables: Dict[str, pd.DataFrame], output_dir: Path):
    """Safely writes all 10 framework DataFrames to CSV."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, df in tables.items():
        file_path = output_dir / filename
        df.to_csv(file_path, index=False)
        print(f"  [Table Exported] {filename} ({len(df)} rows)")


def generate_phase8_figures(output_dir: Path):
    """
    Renders Figures 45 - 48 in both 300 DPI PNG and vector SVG.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="white", font="sans-serif")

    # 1. Figure 45: Four-Quadrant Talent Matrix
    fig, ax = plt.subplots(figsize=(9, 8), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axvline(5, color="black", linestyle="--", alpha=0.7, lw=1.5)
    ax.axhline(5, color="black", linestyle="--", alpha=0.7, lw=1.5)

    # Shading quadrants
    ax.fill_between([5, 10], 5, 10, color="#d4edda", alpha=0.5) # Q1: High Tech, High Comm (Green)
    ax.fill_between([0, 5], 5, 10, color="#fff3cd", alpha=0.5) # Q2: Low Tech, High Comm (Yellow)
    ax.fill_between([5, 10], 0, 5, color="#cce5ff", alpha=0.5) # Q3: High Tech, Low Comm (Blue)
    ax.fill_between([0, 5], 0, 5, color="#f8d7da", alpha=0.5) # Q4: Low Tech, Low Comm (Red)

    # Quadrant Texts
    ax.text(7.5, 8.5, "QUADRANT 1: ADVANCED READINESS\n(Strategic Impact)", ha="center", va="center", fontsize=11, weight="bold", color="#155724")
    ax.text(7.5, 6.8, "High Tech (Maths >= 3.65) + High Comm (Storytelling >= 4.15)\n- JDS CART Rule 1: 100% High Salary Hike (N=45)\n- SDS Leaf 4: 94.3% Consulting Success (N=88)\n- Strategic fast-track compensation band (>15L INR)", ha="center", va="center", fontsize=8.5, color="#155724")

    ax.text(2.5, 8.5, "QUADRANT 3: BUSINESS FACILITATOR\n(Communication Strong, Technical Gap)", ha="center", va="center", fontsize=10.5, weight="bold", color="#856404")
    ax.text(2.5, 6.8, "Low Tech (Maths < 3.65) + High Comm (Storytelling >= 4.15)\n- JDS CART Rule 2: 71.4% High Hike (Communication compensates)\n- Product & Analytics Translation roles\n- Ceiling risk without statistical modeling depth", ha="center", va="center", fontsize=8.5, color="#856404")

    ax.text(7.5, 3.5, "QUADRANT 2: THE EXECUTION ENGINE\n(Technically Strong, Communication Gap)", ha="center", va="center", fontsize=10.5, weight="bold", color="#004085")
    ax.text(7.5, 1.8, "High Tech (Maths >= 3.65) + Low Comm (Storytelling < 4.15)\n- JDS CART Rules 3 & 4: Velocity drops to 66-82%\n- Backend pipeline & algorithm research\n- Plateau risk due to lack of business translation", ha="center", va="center", fontsize=8.5, color="#004085")

    ax.text(2.5, 3.5, "QUADRANT 4: FOUNDATIONAL DEVELOPMENT\n(Early Stage / Stagnation Trap)", ha="center", va="center", fontsize=10.5, weight="bold", color="#721c24")
    ax.text(2.5, 1.8, "Low Tech (Maths < 3.65) + Low Comm (Storytelling < 4.15)\n- JDS CART Rule 6: 97.7% Low Salary Hike (N=44)\n- SDS Leaf 1 & 2: 100% Low Consulting Success\n- Entry-level routine tasks (<6L INR); high automation risk", ha="center", va="center", fontsize=8.5, color="#721c24")

    ax.set_title("Figure 45: Evidence-Based Four-Quadrant Talent Framework", fontsize=13, weight="bold", pad=15)
    ax.set_xlabel("Technical Foundation & Modeling Rigor (Maths/Stats, Machine Learning, Coding)  ──►", fontsize=11, weight="bold")
    ax.set_ylabel("Business Storytelling & Consulting Adaptability (Storytelling, Openness)  ──►", fontsize=11, weight="bold")
    ax.set_xticks([])
    ax.set_yticks([])
    plt.tight_layout()
    fig.savefig(output_dir / "fig45_four_quadrant_talent_matrix.png", dpi=300)
    fig.savefig(output_dir / "fig45_four_quadrant_talent_matrix.svg")
    plt.close(fig)

    # 2. Figure 46: Career Progression Roadmap
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    stages = ["Stage 1: Foundation\n(0-2 yrs)", "Stage 2: Velocity\n(2-5 yrs)", "Stage 3: Expansion\n(5-8 yrs)", "Stage 4: Leadership\n(8+ yrs)"]
    y_pos = [1, 2, 3, 4]
    ax.plot(stages, y_pos, marker="o", color="#1f77b4", lw=3, markersize=10)

    milestones = [
        "Gate: SQL & Python Table Stakes\nFocus: Data Wrangling & Hygiene\nComp: 3.5L - 8.0L INR",
        "Driver: Storytelling (AOR=3.23) + Maths (AOR=3.65)\nFocus: Insight Translation & Dashboards\nComp: 7.5L - 16.0L INR",
        "Premia: Spark (AOR=1.59) + ML (AOR=1.58)\nFocus: Production Systems & Scoping\nComp: 14.0L - 28.0L INR",
        "Driver: Openness (AOR=7.72) + Rigor (AOR=8.11)\nFocus: Trusted Advisory & Client Adaptability\nComp: 25.0L - 50.0L+ INR"
    ]

    for i, (stage, y, text) in enumerate(zip(stages, y_pos, milestones)):
        ax.text(i, y + 0.25, text, ha="center", va="bottom", fontsize=8.5,
                bbox=dict(boxstyle="round,pad=0.4", fc="#f8f9fa", ec="#ced4da", lw=1))

    ax.set_ylim(0.5, 5.2)
    ax.set_title("Figure 46: Career-Stage Progression Roadmap & Competency Milestones", fontsize=12, weight="bold")
    ax.set_ylabel("Career Elevation Stage", fontsize=10)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(["Level 1", "Level 2", "Level 3", "Level 4"])
    plt.tight_layout()
    fig.savefig(output_dir / "fig46_career_progression_roadmap.png", dpi=300)
    fig.savefig(output_dir / "fig46_career_progression_roadmap.svg")
    plt.close(fig)

    # 3. Figure 47: Stakeholder Action Map
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    stakeholders = ["Students & Job Seekers", "Universities & Bootcamps", "Mentors & Coaches", "Employers & HR Teams"]
    actions = [
        "Build dual-artifact portfolios (Code + PowerBI Dashboard);\nde-emphasize standalone LeetCode grind.",
        "Mandate oral project defenses; reallocate lab hours from\nBig Data infrastructure to experimental design & BI.",
        "Conduct client ambiguity roleplay simulations; instill\ndelivery conscientiousness audits.",
        "Calibrate job postings; evaluate business narrative defense;\nstrictly ban automated personality hiring filters."
    ]
    colors_st = ["#1f77b4", "#2ca02c", "#ff7f0e", "#d62728"]
    y_s = np.arange(len(stakeholders))

    ax.barh(y_s, [10, 10, 10, 10], color=colors_st, alpha=0.2, edgecolor=colors_st, lw=2)
    for i, (st, act, col) in enumerate(zip(stakeholders, actions, colors_st)):
        ax.text(0.3, i, f"{st.upper()}:\n{act}", va="center", fontsize=9.5, weight="bold", color="#212529")

    ax.set_xlim(0, 10)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title("Figure 47: Evidence-to-Action Blueprint Across 4 Stakeholders", fontsize=12, weight="bold")
    plt.tight_layout()
    fig.savefig(output_dir / "fig47_stakeholder_action_map.png", dpi=300)
    fig.savefig(output_dir / "fig47_stakeholder_action_map.svg")
    plt.close(fig)

    # 4. Figure 48: Competency Priority Matrix
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
    comps = ["Executive Storytelling", "Maths & Statistics", "Client Openness", "Delivery Conscientiousness", "Specialized ML & Spark", "SQL & Python Syntax"]
    priority_scores = [9.5, 9.2, 9.0, 9.1, 7.8, 6.0]
    colors_cp = ["#d62728", "#d62728", "#d62728", "#d62728", "#2ca02c", "#7f7f7f"]

    bars = ax.barh(comps[::-1], priority_scores[::-1], color=colors_cp[::-1], alpha=0.85, edgecolor="black")
    for bar, val in zip(bars, priority_scores[::-1]):
        ax.text(bar.get_width() + 0.15, bar.get_y() + bar.get_height() / 2, f"{val:.1f} / 10", va="center", fontsize=9, weight="bold")

    ax.set_xlim(0, 11)
    ax.set_title("Figure 48: Evidence-Calibrated Competency Priority Hierarchy", fontsize=12, weight="bold")
    ax.set_xlabel("Strategic Development Priority Score (Out of 10)", fontsize=10)
    plt.tight_layout()
    fig.savefig(output_dir / "fig48_competency_priority_matrix.png", dpi=300)
    fig.savefig(output_dir / "fig48_competency_priority_matrix.svg")
    plt.close(fig)

    print("  [Figures Generated] All 4 Phase 8 publication figures saved (PNG & SVG).")
