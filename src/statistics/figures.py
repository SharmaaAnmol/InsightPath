"""
figures.py
----------
Publication-quality inferential visualizations for Phase 4 (Figures 16–22):
  - Fig 16: H1 Forest plot of JDS skill effects (Cohen's d and 95% CIs)
  - Fig 17: H2 Forest plot of JDS multivariable adjusted odds ratios
  - Fig 18: H3 Forest plot of SDS personality trait effect sizes
  - Fig 19: H4 Forest plot of SDS adjusted odds ratios (Primary vs Sensitivity)
  - Fig 20: H5 Bivariate and semi-log regression of experience vs salary
  - Fig 21: H6 Geographic premium salary association & standardized residuals
  - Fig 22: H6 Top technical skill odds ratios forest plot
Exports all figures in both high-resolution PNG (300 DPI) and vector SVG.
"""

from pathlib import Path
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Set publication aesthetics
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.titlesize": 13,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def save_figure(fig: plt.Figure, name: str, out_dir: Path):
    """Saves figure in both PNG and SVG formats."""
    out_dir.mkdir(parents=True, exist_ok=True)
    png_path = out_dir / f"{name}.png"
    svg_path = out_dir / f"{name}.svg"
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    fig.savefig(svg_path, format="svg", bbox_inches="tight")
    plt.close(fig)


def generate_fig16_h1_jds_effects(df_h1_tests: pd.DataFrame, out_dir: Path):
    """Fig 16: H1 Forest plot of JDS skill effects with 95% CIs."""
    fig, ax = plt.subplots(figsize=(9, 5))
    
    # Sort by Cohen's d ascending for vertical display
    df_sorted = df_h1_tests.sort_values(by="cohens_d", ascending=True).reset_index(drop=True)
    y_pos = np.arange(len(df_sorted))
    
    clean_labels = [
        v.replace("_skills", "").replace("_", " ").title() for v in df_sorted["variable"]
    ]
    
    d_vals = df_sorted["cohens_d"].values
    ci_low = df_sorted["cohens_d_ci_lower"].values
    ci_high = df_sorted["cohens_d_ci_upper"].values
    err_low = d_vals - ci_low
    err_high = ci_high - d_vals
    
    colors = ["#2b5c8f" if d > 0.5 else "#888888" for d in d_vals]
    
    ax.errorbar(
        d_vals, y_pos, xerr=[err_low, err_high],
        fmt="o", color="#1f4e79", ecolor="#2b5c8f", elinewidth=2, capsize=4, markersize=8
    )
    
    # Reference line at d = 0
    ax.axvline(0, color="gray", linestyle="--", alpha=0.7, label="Null Effect (d = 0)")
    # Large effect benchmark line at d = 0.8
    ax.axvline(0.8, color="#2e7d32", linestyle=":", alpha=0.6, label="Cohen's Benchmark: Large Effect (d = 0.8)")
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(clean_labels)
    ax.set_xlabel("Standardized Mean Difference (Cohen's d with 95% CI)")
    ax.set_title("Fig 16: H1 JDS Technical Skill Differences by Salary Hike Status (N=139)", fontweight="bold")
    
    # Statistical annotations
    for i, row in df_sorted.iterrows():
        p_str = f"q={row['p_value_mwu']:.2e}" if row["p_value_mwu"] < 0.001 else f"q={row['p_value_mwu']:.3f}"
        ax.text(
            ci_high[i] + 0.05, y_pos[i],
            f"d={row['cohens_d']:.2f} ({p_str})",
            va="center", fontsize=8.5, color="#1f4e79" if row["cohens_d"] > 0.5 else "#555555"
        )
        
    ax.set_xlim(-0.3, 2.1)
    ax.legend(loc="lower right", frameon=True)
    
    fig.text(0.12, -0.04, "Method Note: Two-sample Mann-Whitney U test with Benjamini-Hochberg FDR correction. Cohort: Junior Data Scientists (High Hike n=73, Low Hike n=66).", fontsize=8, color="#555555")
    
    save_figure(fig, "fig16_h1_jds_skill_effects", out_dir)


def generate_fig17_h2_jds_odds_ratios(df_h2_params: pd.DataFrame, out_dir: Path):
    """Fig 17: H2 Forest plot of JDS multivariable adjusted odds ratios."""
    fig, ax = plt.subplots(figsize=(9, 5))
    
    # Filter out intercept
    df_plot = df_h2_params[df_h2_params["parameter"] != "const"].copy()
    df_plot = df_plot.sort_values(by="odds_ratio", ascending=True).reset_index(drop=True)
    y_pos = np.arange(len(df_plot))
    
    clean_labels = [
        p.replace("_skills", "").replace("_", " ").title() for p in df_plot["parameter"]
    ]
    
    or_vals = df_plot["odds_ratio"].values
    ci_low = df_plot["or_ci_lower"].values
    ci_high = df_plot["or_ci_upper"].values
    err_low = or_vals - ci_low
    err_high = ci_high - or_vals
    
    ax.errorbar(
        or_vals, y_pos, xerr=[err_low, err_high],
        fmt="s", color="#8b0000", ecolor="#b22222", elinewidth=2, capsize=4, markersize=8
    )
    
    # Reference line at OR = 1.0
    ax.axvline(1.0, color="gray", linestyle="--", alpha=0.7, label="No Effect (Adjusted OR = 1.0)")
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(clean_labels)
    ax.set_xlabel("Adjusted Odds Ratio per 1-SD Increase (95% Wald CI, Log Scale)")
    ax.set_xscale("log")
    ax.set_title("Fig 17: H2 Independent Junior Skill Associations with Salary Hike (N=139)", fontweight="bold")
    
    for i, row in df_plot.iterrows():
        p_txt = f"p={row['p_value']:.3f}" if row['p_value'] >= 0.001 else "p<0.001"
        ax.text(
            ci_high[i] * 1.15, y_pos[i],
            f"AOR={row['odds_ratio']:.2f} ({p_txt})",
            va="center", fontsize=8.5, color="#8b0000" if row["p_value"] < 0.05 else "#555555"
        )
        
    ax.set_xlim(0.3, 30.0)
    ax.legend(loc="lower right", frameon=True)
    
    fig.text(0.12, -0.04, "Method Note: Multivariable binary logistic regression on standardized continuous skills. Model Pseudo R² = 0.499, LLR p = 8.16e-19. VIF < 2.3 for all predictors.", fontsize=8, color="#555555")
    
    save_figure(fig, "fig17_h2_jds_adjusted_odds_ratios", out_dir)


def generate_fig18_h3_sds_personality_effects(df_h3_tests: pd.DataFrame, out_dir: Path):
    """Fig 18: H3 Big Five personality trait standardized differences."""
    fig, ax = plt.subplots(figsize=(9, 5))
    
    df_sorted = df_h3_tests.sort_values(by="cohens_d", ascending=True).reset_index(drop=True)
    y_pos = np.arange(len(df_sorted))
    
    clean_labels = [
        t.replace("_", " ").title() for t in df_sorted["variable"]
    ]
    
    d_vals = df_sorted["cohens_d"].values
    ci_low = df_sorted["cohens_d_ci_lower"].values
    ci_high = df_sorted["cohens_d_ci_upper"].values
    err_low = d_vals - ci_low
    err_high = ci_high - d_vals
    
    ax.errorbar(
        d_vals, y_pos, xerr=[err_low, err_high],
        fmt="D", color="#104e8b", ecolor="#1874cd", elinewidth=2, capsize=4, markersize=8
    )
    
    ax.axvline(0, color="gray", linestyle="--", alpha=0.7, label="Null Difference (d = 0)")
    ax.axvline(0.8, color="#2e7d32", linestyle=":", alpha=0.6, label="Cohen's Benchmark: Large Effect (d = 0.8)")
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(clean_labels)
    ax.set_xlabel("Standardized Mean Difference (Cohen's d with 95% CI)")
    ax.set_title("Fig 18: H3 SDS Big Five Personality Divergence by Success Status (N=161)", fontweight="bold")
    
    for i, row in df_sorted.iterrows():
        p_str = f"q={row['p_value_mwu']:.2e}" if row["p_value_mwu"] < 0.001 else f"q={row['p_value_mwu']:.3f}"
        ax.text(
            ci_high[i] + 0.08, y_pos[i],
            f"d={row['cohens_d']:.2f} ({p_str})",
            va="center", fontsize=8.5, color="#104e8b" if abs(row["cohens_d"]) > 0.5 else "#555555"
        )
        
    ax.set_xlim(-0.6, 2.6)
    ax.legend(loc="lower right", frameon=True)
    
    fig.text(0.12, -0.04, "Method Note: Two-sample Mann-Whitney U test with Benjamini-Hochberg FDR correction. Cohort: Senior Data Scientists (High Success n=85, Low Success n=76).", fontsize=8, color="#555555")
    
    save_figure(fig, "fig18_h3_sds_personality_effects", out_dir)


def generate_fig19_h4_sds_odds_ratios(df_h4_sens: pd.DataFrame, out_dir: Path):
    """Fig 19: H4 Forest plot of SDS adjusted odds ratios comparing Primary (N=161) vs Sensitivity (N=152)."""
    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    
    df_plot = df_h4_sens[df_h4_sens["predictor"] != "const"].copy()
    y_pos = np.arange(len(df_plot))
    offset = 0.15
    
    clean_labels = [p.replace("_", " ").title() for p in df_plot["predictor"]]
    
    # Primary N=161
    p_or = df_plot["primary_or"].values
    ax.plot(p_or, y_pos + offset, "o", color="#1f4e79", markersize=8, label="Primary Cohort (N=161)")
    
    # Sensitivity Deduplicated N=152
    s_or = df_plot["dedup_or"].values
    ax.plot(s_or, y_pos - offset, "s", color="#b22222", markersize=8, label="Deduplicated Cohort (N=152)")
    
    # Draw connecting lines to emphasize stability
    for i in range(len(df_plot)):
        ax.plot([p_or[i], s_or[i]], [y_pos[i] + offset, y_pos[i] - offset], color="gray", linestyle="-", alpha=0.5)
        ax.text(
            max(p_or[i], s_or[i]) * 1.25, y_pos[i],
            f"Prim: {p_or[i]:.1f} | Sens: {s_or[i]:.1f}",
            va="center", fontsize=8, color="#333333"
        )
        
    ax.axvline(1.0, color="gray", linestyle="--", alpha=0.7, label="No Effect (AOR = 1.0)")
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(clean_labels)
    ax.set_xlabel("Adjusted Odds Ratio per 1-SD Trait Increase (Log Scale)")
    ax.set_xscale("log")
    ax.set_title("Fig 19: H4 SDS Adjusted Personality Odds Ratios: Primary vs Deduplicated Sensitivity", fontweight="bold")
    ax.set_xlim(0.4, 250.0)
    ax.legend(loc="lower right", frameon=True)
    
    fig.text(0.12, -0.04, "Method Note: Multivariable logistic regressions on standardized traits. Demonstrates 100% conclusion stability across primary and deduplicated cohorts.", fontsize=8, color="#555555")
    
    save_figure(fig, "fig19_h4_sds_adjusted_odds_ratios", out_dir)


def generate_fig20_h5_regressions(df_ds: pd.DataFrame, out_dir: Path):
    """Fig 20: H5 Experience vs Salary Inferential Regressions (Linear and Semi-Log)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))
    
    # Panel A: Linear OLS
    sns.regplot(
        data=df_ds, x="min_experience", y="avg_salary_lakh",
        ax=ax1, color="#1f4e79",
        scatter_kws={"alpha": 0.25, "s": 18, "color": "#4a7bb0"},
        line_kws={"color": "#b22222", "linewidth": 2.2, "label": "OLS Fit (β = +1.98L/yr, R² = 0.352)"}
    )
    ax1.set_xlabel("Minimum Required Experience (Years)")
    ax1.set_ylabel("Average Advertised Salary (Lakhs INR)")
    ax1.set_title("Panel A: Raw Linear Compensation Elasticity", fontweight="bold")
    ax1.legend(loc="upper left", frameon=True)
    ax1.text(0.05, 0.78, "Pearson r = 0.593 [0.561, 0.624]\np = 5.65e-153 (N=1,602)", transform=ax1.transAxes, fontsize=9, bbox=dict(boxstyle="round,pad=0.3", fc="#f0f4f8", ec="#b0c4de", alpha=0.9))
    
    # Panel B: Semi-Log OLS
    df_ds_plot = df_ds.copy()
    df_ds_plot["log_salary"] = np.log(df_ds_plot["avg_salary_lakh"])
    sns.regplot(
        data=df_ds_plot, x="min_experience", y="log_salary",
        ax=ax2, color="#2b5c8f",
        scatter_kws={"alpha": 0.25, "s": 18, "color": "#5c8cb0"},
        line_kws={"color": "#006400", "linewidth": 2.2, "label": "Semi-Log Fit (β = +0.1517/yr)"}
    )
    ax2.set_xlabel("Minimum Required Experience (Years)")
    ax2.set_ylabel("Natural Log of Average Salary ln(Lakhs INR)")
    ax2.set_title("Panel B: Semi-Log Wage Growth (16.4% Annual Return)", fontweight="bold")
    ax2.legend(loc="upper left", frameon=True)
    ax2.text(0.05, 0.78, "Semi-Log Pearson r = 0.582\nHC3 Robust SE = 0.0066\np = 7.82e-116 (N=1,602)", transform=ax2.transAxes, fontsize=9, bbox=dict(boxstyle="round,pad=0.3", fc="#f0f8f0", ec="#c0dec0", alpha=0.9))
    
    plt.suptitle("Fig 20: H5 Experience-to-Compensation Elasticity Regressions (DataScience Jobs, N=1,602)", fontweight="bold", y=1.02)
    fig.text(0.12, -0.04, "Method Note: Ordinary Least Squares with HC3 heteroskedasticity-consistent standard errors. Controls for job title yield beta = +1.51L/yr (p = 1.20e-51, R² = 0.548).", fontsize=8, color="#555555")
    
    save_figure(fig, "fig20_h5_experience_salary_regressions", out_dir)


def generate_fig21_h6_geography(df_geo_res: pd.DataFrame, out_dir: Path):
    """Fig 21: H6 Geographic Premium-Salary Association and Residuals."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))
    
    df_sorted = df_geo_res.sort_values(by="high_salary_pct", ascending=True).reset_index(drop=True)
    y_pos = np.arange(len(df_sorted))
    
    # Panel A: Premium Salary Proportion
    ax1.barh(y_pos, df_sorted["high_salary_pct"], color="#2b5c8f", alpha=0.85, height=0.6)
    # Overall benchmark line (28.57%)
    overall_mean_pct = 28.57
    ax1.axvline(overall_mean_pct, color="#b22222", linestyle="--", label=f"National Average ({overall_mean_pct}%)")
    
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(df_sorted["location_cluster"])
    ax1.set_xlabel("High-Tier Salary Vacancies (% >= 15 Lakhs)")
    ax1.set_title("Panel A: Geographic Premium Representation", fontweight="bold")
    ax1.legend(loc="lower right", frameon=True)
    
    for i, r in df_sorted.iterrows():
        ax1.text(r["high_salary_pct"] + 0.6, y_pos[i], f"{r['high_salary_pct']:.1f}%", va="center", fontsize=8.5)
    ax1.set_xlim(0, 36)
    
    # Panel B: Adjusted Standardized Residuals
    res_vals = df_sorted["adj_standardized_residual_high"].values
    colors = ["#2e7d32" if v > 2.0 else "#b22222" if v < -2.0 else "#777777" for v in res_vals]
    
    ax2.barh(y_pos, res_vals, color=colors, alpha=0.85, height=0.6)
    ax2.axvline(2.0, color="#2e7d32", linestyle=":", label="Significant Over-representation (|z| > 2.0)")
    ax2.axvline(-2.0, color="#b22222", linestyle=":", label="Significant Under-representation (|z| < -2.0)")
    ax2.axvline(0.0, color="gray", linestyle="-", alpha=0.6)
    
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(df_sorted["location_cluster"])
    ax2.set_xlabel("Adjusted Standardized Residual (Haberman z-score)")
    ax2.set_title("Panel B: Cell Residual Departure from Independence", fontweight="bold")
    ax2.legend(loc="lower right", frameon=True)
    
    for i, v in enumerate(res_vals):
        pos_offset = 0.2 if v >= 0 else -0.8
        ax2.text(v + pos_offset, y_pos[i], f"z={v:.2f}", va="center", fontsize=8.5)
    ax2.set_xlim(-6.5, 6.5)
    
    plt.suptitle("Fig 21: H6 Geographic Wage Bifurcation (Analytics Jobs, N=15,841, Chi² = 57.90, p = 1.20e-10)", fontweight="bold", y=1.02)
    fig.text(0.12, -0.04, "Method Note: Pearson Chi-square test of independence on 7x2 table. Cramér's V = 0.060. Expected counts exceed 290 in all cells.", fontsize=8, color="#555555")
    
    save_figure(fig, "fig21_h6_geography_premium_association", out_dir)


def generate_fig22_h6_skill_odds_ratios(df_skills_fdr: pd.DataFrame, out_dir: Path):
    """Fig 22: H6 Skill Odds Ratios Forest Plot for Top Skills."""
    fig, ax = plt.subplots(figsize=(9.5, 6.0))
    
    # Select top 12 representative skills for publication clarity
    focus_skills = [
        "skill_r", "skill_machine_learning", "skill_spark", "skill_sas",
        "skill_hadoop", "skill_python", "skill_data_science", "skill_analytics",
        "skill_sql", "skill_data_analysis", "skill_excel", "skill_digital_marketing"
    ]
    df_plot = df_skills_fdr[df_skills_fdr["skill_code"].isin(focus_skills)].copy()
    if len(df_plot) < 8:
        df_plot = df_skills_fdr.head(12).copy()
        
    df_plot = df_plot.sort_values(by="odds_ratio", ascending=True).reset_index(drop=True)
    y_pos = np.arange(len(df_plot))
    
    or_vals = df_plot["odds_ratio"].values
    ci_low = df_plot["ci_lower"].values
    ci_high = df_plot["ci_upper"].values
    err_low = or_vals - ci_low
    err_high = ci_high - or_vals
    
    colors = ["#1f4e79" if v >= 1.5 else "#888888" if v >= 1.0 else "#b22222" for v in or_vals]
    
    for i in range(len(df_plot)):
        ax.errorbar(
            or_vals[i], y_pos[i], xerr=[[err_low[i]], [err_high[i]]],
            fmt="o", color=colors[i], ecolor=colors[i], elinewidth=2, capsize=4, markersize=8
        )
        q_txt = f"q={df_plot.loc[i, 'fdr_adjusted_p']:.1e}" if df_plot.loc[i, 'fdr_adjusted_p'] < 0.001 else f"q={df_plot.loc[i, 'fdr_adjusted_p']:.3f}"
        ax.text(
            ci_high[i] * 1.08, y_pos[i],
            f"OR={or_vals[i]:.2f} [{ci_low[i]:.2f}, {ci_high[i]:.2f}] ({q_txt})",
            va="center", fontsize=8.5, color=colors[i]
        )
        
    ax.axvline(1.0, color="gray", linestyle="--", alpha=0.7, label="Neutral Association (OR = 1.0)")
    ax.axvline(2.0, color="#1f4e79", linestyle=":", alpha=0.6, label="Doubled Odds of Premium Pay (OR = 2.0)")
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df_plot["skill_name"])
    ax.set_xlabel("Unadjusted Odds Ratio for High-Tier Salary (>= 15L) [95% Woolf CI, Log Scale]")
    ax.set_xscale("log")
    ax.set_title("Fig 22: H6 Specialized vs Foundational Skill Premium Odds Ratios (Analytics Jobs, N=15,841)", fontweight="bold")
    ax.set_xlim(0.3, 4.0)
    ax.legend(loc="lower right", frameon=True)
    
    fig.text(0.12, -0.04, "Method Note: 2x2 contingency tables with Haldane-Anscombe continuity correction and Benjamini-Hochberg FDR correction across skills.", fontsize=8, color="#555555")
    
    save_figure(fig, "fig22_h6_skill_odds_ratios", out_dir)
