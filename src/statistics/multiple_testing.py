"""
multiple_testing.py
--------------------
Controls False Discovery Rate (FDR) using Benjamini-Hochberg procedure:
  - Definition of structured test families
  - Mapping raw p-values to adjusted q-values
  - Evaluation of significance thresholds at alpha = 0.05
  - Multiple testing summary table generation
"""

from typing import List, Dict, Optional
import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests


def apply_benjamini_hochberg(
    df: pd.DataFrame,
    p_col: str,
    alpha: float = 0.05,
    prefix: str = "bh_"
) -> pd.DataFrame:
    """
    Applies the Benjamini-Hochberg (BH) FDR correction to a DataFrame column of p-values.
    Appends:
      - fdr_adjusted_p: adjusted p-value (q-value)
      - significant_after_fdr: boolean indicator whether adjusted p < alpha
    """
    res_df = df.copy()
    raw_p = res_df[p_col].values
    
    # Run multipletests
    reject, pvals_corrected, _, _ = multipletests(raw_p, alpha=alpha, method="fdr_bh")
    
    res_df[f"{prefix}adjusted_p"] = [round(float(p), 6) for p in pvals_corrected]
    res_df[f"{prefix}significant"] = reject
    res_df[f"{prefix}alpha"] = alpha
    
    return res_df


def build_multiple_testing_summary(
    family_tables: Dict[str, pd.DataFrame]
) -> pd.DataFrame:
    """
    Constructs the consolidated multiple testing summary table across all testing families:
      - Hypothesis
      - Test Family Name
      - Number of Comparisons (m)
      - Number Significant (Raw p < 0.05)
      - Number Significant (FDR q < 0.05)
      - False Discovery Rate Target (alpha)
      - Summary Decision
    """
    records = []
    for family_name, df_fam in family_tables.items():
        m = len(df_fam)
        sig_raw = int((df_fam["raw_p"] < 0.05).sum()) if "raw_p" in df_fam else int((df_fam["p_value"] < 0.05).sum())
        adj_col = [c for c in df_fam.columns if "adjusted_p" in c or "fdr" in c and "p" in c]
        if adj_col:
            sig_adj = int((df_fam[adj_col[0]] < 0.05).sum())
        else:
            sig_adj = np.nan
            
        hypo = df_fam["hypothesis"].iloc[0] if "hypothesis" in df_fam else "N/A"
        
        records.append({
            "hypothesis": hypo,
            "test_family": family_name,
            "num_comparisons_m": m,
            "num_sig_raw_p": sig_raw,
            "num_sig_fdr_q": sig_adj,
            "fdr_alpha": 0.05,
            "family_verdict": f"{sig_adj} / {m} tests survived FDR correction"
        })
        
    return pd.DataFrame(records)
