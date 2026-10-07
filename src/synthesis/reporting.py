"""
src/synthesis/reporting.py
--------------------------
Reporting and visualization module for Phase 7: Cross-Dataset Analytical Synthesis.
Exports all 9 synthesis CSV tables and renders publication figures (Figures 41 - 44).
"""

from pathlib import Path
from typing import Dict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def export_phase7_tables(tables: Dict[str, pd.DataFrame], output_dir: Path):
    """Safely writes all 9 synthesis DataFrames to CSV."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, df in tables.items():
        file_path = output_dir / filename
        df.to_csv(file_path, index=False)
        print(f"  [Table Exported] {filename} ({len(df)} rows)")


def generate_phase7_figures(output_dir: Path):
    """
    Renders and saves Figures 41 - 44 in both 300 DPI PNG and vector SVG.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", font="sans-serif")

    # 1. Figure 41: Career Stage Evidence Map
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    stages = ["Stage 1: Entry / Foundation\n(0-2 yrs)", "Stage 2: Junior / Velocity\n(2-5 yrs)", "Stage 3: Mid-Career / Expansion\n(5-8 yrs)", "Stage 4: Senior / Leadership\n(8+ yrs)"]
    salary_mins = [3.5, 7.5, 14.0, 25.0]
    salary_maxs = [8.0, 16.0, 28.0, 50.0]
    midpoints = [(l + h) / 2 for l, h in zip(salary_mins, salary_maxs)]

    y_err = [np.array(midpoints) - np.array(salary_mins), np.array(salary_maxs) - np.array(midpoints)]
    bars = ax.bar(stages, midpoints, yerr=y_err, capsize=6, color="#1f77b4", alpha=0.85, edgecolor="black")

    annotations = [
        "Table Stakes:\nSQL (48%), Python (40%)\nBasic Wrangling",
        "Velocity Drivers:\nStorytelling (AOR=3.23)\nMaths/Stats (AOR=3.65)",
        "Specialized Premia:\nSpark (AOR=1.59)\nML (AOR=1.58), R/SAS",
        "Executive Success:\nOpenness (AOR=7.72)\nConscientiousness (AOR=8.11)"
    ]

    for bar, text in zip(bars, annotations):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h / 2, text, ha="center", va="center",
                fontsize=8.5, weight="bold", color="white", bbox=dict(boxstyle="round,pad=0.3", fc="#08306b", ec="none", alpha=0.85))

    ax.set_title("Figure 41: Career-Stage Compensation Envelopes & Dominant Evidence Drivers", fontsize=13, weight="bold")
    ax.set_ylabel("Compensation Band (Lakhs INR)", fontsize=11)
    ax.set_ylim(0, 55)
    plt.tight_layout()
    fig.savefig(output_dir / "fig41_career_stage_evidence_map.png", dpi=300)
    fig.savefig(output_dir / "fig41_career_stage_evidence_map.svg")
    plt.close(fig)

    # 2. Figure 42: Market Skill Progression & Odds Ratios
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    skills = ["Spark (Big Data)", "Machine Learning", "R Language", "SAS Enterprise", "Storytelling (JDS)", "Maths/Stats (JDS)", "Python (Market)", "SQL (Market)"]
    aors = [1.587, 1.581, 1.561, 1.466, 3.234, 3.652, 1.059, 0.986]
    colors = ["#2ca02c" if v > 1.4 and v < 2.0 else "#d62728" if v > 2.0 else "#7f7f7f" for v in aors]

    bars = ax.barh(skills, aors, color=colors, alpha=0.85, edgecolor="black")
    ax.axvline(1.0, color="black", linestyle="--", alpha=0.6, label="Neutral Odds Ratio (1.0)")

    for bar, aor in zip(bars, aors):
        w = bar.get_width()
        ax.text(w + 0.08, bar.get_y() + bar.get_height() / 2, f"{aor:.2f}x", va="center", fontsize=9, weight="bold")

    ax.set_xlim(0, 4.3)
    ax.set_title("Figure 42: Adjusted Odds Ratios: Market Salary Premia vs Junior Promotion Velocity", fontsize=12, weight="bold")
    ax.set_xlabel("Adjusted Odds Ratio (AOR, Multiplier on Success / High Salary)", fontsize=10)
    ax.legend(loc="lower right")
    plt.tight_layout()
    fig.savefig(output_dir / "fig42_market_skill_progression.png", dpi=300)
    fig.savefig(output_dir / "fig42_market_skill_progression.svg")
    plt.close(fig)

    # 3. Figure 43: Skill to Career Stage Heatmap Matrix
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)
    stages_short = ["Entry (0-2y)", "Junior (2-5y)", "Mid-Career (5-8y)", "Senior (8+y)"]
    skills_rows = ["SQL / Databases", "Python Programming", "Maths & Statistics", "Data Storytelling", "Machine Learning", "Distributed Spark", "Client Openness", "Delivery Conscientiousness"]

    # Heatmap values: 1=Baseline/Low, 2=Moderate, 3=High Differentiator, 4=Dominant Driver
    matrix_data = np.array([
        [4, 2, 1, 1],  # SQL
        [4, 3, 2, 1],  # Python
        [2, 4, 3, 2],  # Maths/Stats
        [1, 4, 4, 3],  # Storytelling
        [1, 3, 4, 3],  # ML
        [1, 1, 3, 2],  # Spark
        [1, 1, 2, 4],  # Openness
        [2, 2, 3, 4]   # Conscientiousness
    ])

    sns.heatmap(matrix_data, annot=True, cmap="Blues", cbar=True, ax=ax,
                xticklabels=stages_short, yticklabels=skills_rows,
                fmt="d", linewidths=0.5, cbar_kws={'label': 'Strategic Importance (1=Low to 4=Critical)'})
    ax.set_title("Figure 43: Competency Priority Matrix Across Career Stages", fontsize=12, weight="bold")
    plt.tight_layout()
    fig.savefig(output_dir / "fig43_skill_to_career_stage_matrix.png", dpi=300)
    fig.savefig(output_dir / "fig43_skill_to_career_stage_matrix.svg")
    plt.close(fig)

    # 4. Figure 44: Evidence Strength Matrix
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
    findings = [
        "Experience-Salary Elasticity\n(N=1,602 & 15,841)",
        "Foundational vs Premium Skills\n(N=15,841 Market Postings)",
        "Junior Promotion Drivers\n(N=139 JDS, 25 Splits CV)",
        "Senior Consulting Success\n(N=161 SDS, Grouped CV)",
        "Neuroticism Suppressor Nuance\n(Parametric vs Permutation)"
    ]
    confidence_levels = [3, 3, 3, 3, 2] # 3=High Confidence, 2=Moderate/Nuanced
    colors_conf = ["#2ca02c", "#2ca02c", "#2ca02c", "#2ca02c", "#ff7f0e"]

    bars = ax.barh(findings, confidence_levels, color=colors_conf, alpha=0.85, edgecolor="black")
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(["Preliminary", "Moderate / Nuanced", "High Confidence (Empirically Validated)"], fontsize=10)
    ax.set_xlim(0, 3.5)
    ax.set_title("Figure 44: Methodological Evidence Strength Grading", fontsize=13, weight="bold")
    ax.set_xlabel("Empirical Confidence Level", fontsize=11)
    plt.tight_layout()
    fig.savefig(output_dir / "fig44_evidence_strength_matrix.png", dpi=300)
    fig.savefig(output_dir / "fig44_evidence_strength_matrix.svg")
    plt.close(fig)

    print("  [Figures Generated] All 4 Phase 7 publication figures saved (PNG & SVG).")
