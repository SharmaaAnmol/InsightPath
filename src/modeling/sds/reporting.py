"""
src/modeling/sds/reporting.py
-----------------------------
Reporting, artifact serialization, and publication figure generation for Phase 6.
Exports all 23 required CSV tables and 8 publication figures (PNG & SVG).
"""

from pathlib import Path
from typing import Dict, List, Any
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.metrics import roc_curve, auc

from src.modeling.sds.pipelines import SDS_FEATURE_NAMES, SDS_TARGET_NAME


def export_csv_table(df: pd.DataFrame, file_path: Path):
    """Safely writes a DataFrame to CSV with parent directory creation."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)
    print(f"  [Table Exported] {file_path.name} ({len(df)} rows)")


def generate_phase6_figures(
    perf_df: pd.DataFrame,
    fold_df: pd.DataFrame,
    oof_df: pd.DataFrame,
    or_df: pd.DataFrame,
    rules_df: pd.DataFrame,
    rf_imp_df: pd.DataFrame,
    stab_df: pd.DataFrame,
    sens_perf_df: pd.DataFrame,
    output_dir: Path
):
    """
    Renders and saves all 8 required publication figures in PNG (300 DPI) and SVG.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", font="sans-serif")
    palette = sns.color_palette("muted")

    # 1. Figure 33: ROC Curves
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    models_to_plot = ["Logistic_Regression_L2", "Random_Forest", "Gradient_Boosting", "Decision_Tree", "Baseline_Majority"]
    colors = {"Logistic_Regression_L2": "#1f77b4", "Random_Forest": "#2ca02c", "Gradient_Boosting": "#ff7f0e", "Decision_Tree": "#9467bd", "Baseline_Majority": "#7f7f7f"}

    for m in models_to_plot:
        sub = oof_df[oof_df["model_name"] == m]
        if len(sub) == 0:
            continue
        fpr, tpr, _ = roc_curve(sub["true_label"], sub["pred_prob"])
        score = auc(fpr, tpr)
        linestyle = "--" if m == "Baseline_Majority" else "-"
        ax.plot(fpr, tpr, label=f"{m} (AUC = {score:.3f})", color=colors.get(m, "#333333"), linestyle=linestyle, lw=2)

    ax.plot([0, 1], [0, 1], "k--", alpha=0.5)
    ax.set_title("Figure 33: Senior Data Scientist Success ROC Curves (25 Splits)", fontsize=13, weight="bold")
    ax.set_xlabel("False Positive Rate", fontsize=11)
    ax.set_ylabel("True Positive Rate", fontsize=11)
    ax.legend(loc="lower right", frameon=True)
    plt.tight_layout()
    fig.savefig(output_dir / "fig33_sds_model_roc_curves.png", dpi=300)
    fig.savefig(output_dir / "fig33_sds_model_roc_curves.svg")
    plt.close(fig)

    # 2. Figure 34: Model Performance Comparison
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    perf_sub = perf_df[perf_df["model_name"] != "Baseline_Majority"].copy()
    x = np.arange(len(perf_sub))
    width = 0.25

    ax.bar(x - width, perf_sub["roc_auc_mean"], width, label="ROC-AUC", color="#1f77b4", alpha=0.9)
    ax.bar(x, perf_sub["macro_f1_mean"], width, label="Macro F1", color="#2ca02c", alpha=0.9)
    ax.bar(x + width, perf_sub["balanced_accuracy_mean"], width, label="Balanced Acc", color="#ff7f0e", alpha=0.9)

    ax.set_xticks(x)
    ax.set_xticklabels([m.replace("_", "\n") for m in perf_sub["model_name"]], fontsize=9)
    ax.set_ylim(0.7, 1.02)
    ax.set_title("Figure 34: Model Performance Metrics Across 25 Splits (SDS Cohort)", fontsize=13, weight="bold")
    ax.set_ylabel("Score", fontsize=11)
    ax.legend(loc="lower left", frameon=True)
    plt.tight_layout()
    fig.savefig(output_dir / "fig34_sds_model_performance.png", dpi=300)
    fig.savefig(output_dir / "fig34_sds_model_performance.svg")
    plt.close(fig)

    # 3. Figure 35: Logistic Odds Ratios (Forest Plot)
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    y_pos = np.arange(len(or_df))
    ors = or_df["adjusted_odds_ratio"].values
    ci_low = or_df["or_ci_lower_95"].values
    ci_high = or_df["or_ci_upper_95"].values
    labels = [t.replace("_", " ").title() for t in or_df["trait_dimension"].values]

    xerr = [ors - ci_low, ci_high - ors]
    ax.errorbar(ors, y_pos, xerr=xerr, fmt="o", color="#d62728", ecolor="#d62728", elinewidth=2, capsize=5, markersize=8)
    ax.axvline(1.0, color="gray", linestyle="--", alpha=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=10)
    ax.set_xscale("log")
    ax.set_title("Figure 35: Standardized Adjusted Odds Ratios (SDS Big Five, 95% CI)", fontsize=13, weight="bold")
    ax.set_xlabel("Adjusted Odds Ratio (Log Scale, e^beta)", fontsize=11)
    plt.tight_layout()
    fig.savefig(output_dir / "fig35_sds_logistic_odds_ratios.png", dpi=300)
    fig.savefig(output_dir / "fig35_sds_logistic_odds_ratios.svg")
    plt.close(fig)

    # 4. Figure 36: Tree Rules Visualization
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    leaf_names = [f"Leaf {r['leaf_id']}\n(N={r['n_samples']})" for _, r in rules_df.iterrows()]
    probs = rules_df["prob_high_success"].values
    colors_leaf = ["#2ca02c" if p >= 0.5 else "#d62728" for p in probs]

    bars = ax.bar(leaf_names, probs * 100, color=colors_leaf, alpha=0.85, edgecolor="black")
    ax.axhline(50, color="black", linestyle="--", alpha=0.5, label="Decision Boundary (50%)")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 1.5, f"{h:.1f}%", ha="center", fontsize=9, weight="bold")

    ax.set_ylim(0, 115)
    ax.set_title("Figure 36: CART Decision Tree Leaf Nodes & Success Probabilities", fontsize=13, weight="bold")
    ax.set_ylabel("Probability of High Consulting Success (%)", fontsize=11)
    ax.legend(loc="upper left")
    plt.tight_layout()
    fig.savefig(output_dir / "fig36_sds_tree_rules.png", dpi=300)
    fig.savefig(output_dir / "fig36_sds_tree_rules.svg")
    plt.close(fig)

    # 5. Figure 37: Permutation Feature Importance
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    traits_clean = [t.replace("_", " ").title() for t in rf_imp_df["trait_dimension"].values]
    ax.barh(traits_clean[::-1], rf_imp_df["mean_permutation_importance"].values[::-1],
            xerr=rf_imp_df["std_permutation_importance"].values[::-1],
            color="#1f77b4", alpha=0.85, capsize=4)
    ax.set_title("Figure 37: Out-of-Sample Permutation Feature Importance (Random Forest)", fontsize=13, weight="bold")
    ax.set_xlabel("Mean Decrease in Validation ROC-AUC", fontsize=11)
    plt.tight_layout()
    fig.savefig(output_dir / "fig37_sds_permutation_importance.png", dpi=300)
    fig.savefig(output_dir / "fig37_sds_permutation_importance.svg")
    plt.close(fig)

    # 6. Figure 38: Feature Stability Across Splits
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    stab_clean = stab_df.copy()
    stab_clean["trait_label"] = stab_clean["trait_dimension"].str.replace("_", " ").str.title()
    stab_clean = stab_clean.sort_values("top_2_frequency_pct", ascending=True)

    ax.barh(stab_clean["trait_label"], stab_clean["top_2_frequency_pct"], color="#2ca02c", alpha=0.85)
    for i, v in enumerate(stab_clean["top_2_frequency_pct"]):
        ax.text(v + 1, i, f"{v:.1f}%", va="center", fontsize=9, weight="bold")
    ax.set_xlim(0, 115)
    ax.set_title("Figure 38: Trait Rank Stability (% Top-2 Placement Across 25 Splits)", fontsize=13, weight="bold")
    ax.set_xlabel("Percentage of Splits Ranked in Top 2 (%)", fontsize=11)
    plt.tight_layout()
    fig.savefig(output_dir / "fig38_sds_feature_stability.png", dpi=300)
    fig.savefig(output_dir / "fig38_sds_feature_stability.svg")
    plt.close(fig)

    # 7. Figure 39: Confusion Matrix (Champion Model)
    from sklearn.metrics import confusion_matrix
    sub_champ = oof_df[oof_df["model_name"] == "Logistic_Regression_L2"]
    cm = confusion_matrix(sub_champ["true_label"], sub_champ["pred_class"])
    fig, ax = plt.subplots(figsize=(6, 5), dpi=300)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax,
                xticklabels=["Low Success", "High Success"], yticklabels=["Low Success", "High Success"])
    ax.set_title("Figure 39: Out-of-Fold Confusion Matrix (Logistic Regression L2)", fontsize=12, weight="bold")
    ax.set_xlabel("Predicted Label", fontsize=10)
    ax.set_ylabel("True Label", fontsize=10)
    plt.tight_layout()
    fig.savefig(output_dir / "fig39_sds_confusion_matrix.png", dpi=300)
    fig.savefig(output_dir / "fig39_sds_confusion_matrix.svg")
    plt.close(fig)

    # 8. Figure 40: Sensitivity Comparison
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
    x = np.arange(len(sens_perf_df))
    w = 0.35
    ax.bar(x - w / 2, sens_perf_df["roc_auc_mean_primary"], w, label="Primary (N=161)", color="#1f77b4")
    ax.bar(x + w / 2, sens_perf_df["roc_auc_mean_sensitivity"], w, label="Sensitivity (N=152)", color="#ff7f0e")
    ax.set_xticks(x)
    ax.set_xticklabels([m.replace("_", "\n") for m in sens_perf_df["model_name"]], fontsize=9)
    ax.set_ylim(0.7, 1.02)
    ax.set_title("Figure 40: Sensitivity Robustness Comparison (Primary N=161 vs Sensitivity N=152)", fontsize=13, weight="bold")
    ax.set_ylabel("ROC-AUC", fontsize=11)
    ax.legend(loc="lower left")
    plt.tight_layout()
    fig.savefig(output_dir / "fig40_sds_sensitivity_comparison.png", dpi=300)
    fig.savefig(output_dir / "fig40_sds_sensitivity_comparison.svg")
    plt.close(fig)

    print("  [Figures Generated] All 8 Phase 6 publication figures saved (PNG & SVG).")
