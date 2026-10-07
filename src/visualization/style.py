"""
style.py
--------
Unified, publication-quality visual design system for Phase 3 EDA.
Configures consistent typography, color palettes, grid styles,
and standardized dual-format (PNG + SVG) export.
"""

import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# Set writable cache directory for Matplotlib
os.environ["MPLCONFIGDIR"] = "/tmp/mpl_config"

# Primary Publication Color Palette
PALETTE_PRIMARY = ["#1f4e79", "#2e75b6", "#5b9bd5", "#41719c", "#1b365d"]
PALETTE_CATEGORICAL = [
    "#1f4e79",  # Deep Navy
    "#e26b00",  # Amber/Coral
    "#385723",  # Forest Green
    "#7030a0",  # Royal Purple
    "#008080",  # Teal
    "#c00000",  # Crimson
    "#595959"   # Charcoal
]

# Binary Comparison Colors (High vs Low)
COLOR_HIGH = "#1f4e79"  # Navy for High-Hike / High-Success
COLOR_LOW = "#d9534f"   # Coral/Red for Low-Hike / Low-Success
COLOR_NEUTRAL = "#6c757d" # Gray

def apply_publication_theme():
    """Apply consistent styling across all Matplotlib and Seaborn figures."""
    sns.set_theme(style="whitegrid")
    
    mpl.rcParams.update({
        # Typography
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial", "sans-serif"],
        "font.size": 10,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "axes.labelweight": "semibold",
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "legend.fontsize": 9.5,
        "legend.title_fontsize": 10.5,
        
        # Grid and Axes
        "axes.grid": True,
        "grid.color": "#e0e0e0",
        "grid.linestyle": "--",
        "grid.linewidth": 0.7,
        "axes.edgecolor": "#333333",
        "axes.linewidth": 0.9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        
        # Figure Layout
        "figure.autolayout": True,
        "figure.facecolor": "#ffffff",
        "axes.facecolor": "#ffffff",
        "savefig.facecolor": "#ffffff",
        "savefig.edgecolor": "none",
        "savefig.dpi": 300
    })


def save_publication_figure(
    fig: plt.Figure,
    base_filename: str,
    output_dir: str = "outputs/figures/phase3"
):
    """
    Save figure in both high-resolution PNG (300 DPI) and scalable vector SVG formats.
    
    Args:
        fig: Matplotlib Figure object
        base_filename: Filename without extension (e.g. 'fig01_missingness_matrix')
        output_dir: Destination directory
    """
    os.makedirs(output_dir, exist_ok=True)
    
    png_path = os.path.join(output_dir, f"{base_filename}.png")
    svg_path = os.path.join(output_dir, f"{base_filename}.svg")
    
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    fig.savefig(svg_path, format="svg", bbox_inches="tight")
    plt.close(fig)
    return png_path, svg_path
