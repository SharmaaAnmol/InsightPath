# JDS Duplicate Handling & Sensitivity Strategy

**Project**: InsightPath — SAS CU Hackathon Round 2 Analytics  
**Document**: `docs/phase2/JDS_DUPLICATE_HANDLING.md`  
**Phase**: Phase 2 — Data Cleaning & Transformation  
**Governing Standard**: Reproducible Analytics & Pre-Registered Sensitivity Protocols  

---

## 1. Executive Summary & Empirical Context

During the rigorous Phase 1 audit of `JDS Skill Traits.xlsx` (`docs/phase1/DUPLICATE_AUDIT.md`, `docs/phase1/IDENTIFIER_AUDIT.md`), exactly one duplicated identifier was detected within the populated analytical rows ($N = 139$): **Subject ID 3291**.

This identifier appears in two distinct rows of the dataset:
1. **Row 3** (Index 2 in 0-indexed DataFrame)
2. **Row 29** (Index 28 in 0-indexed DataFrame)

A forensic comparison of these two records reveals a critical analytical anomaly: **identical skill feature vectors paired with contradictory target classifications**.

---

## 2. Forensic Profile of Subject ID 3291

| Attribute / Field | Row 3 Record | Row 29 Record | Delta / Status |
| :--- | :--- | :--- | :--- |
| **`id`** | `3291` | `3291` | Duplicate identifier |
| **`big_data_skills`** | `2.2` | `2.2` | Exact match ($\Delta = 0.0$) |
| **`maths_stats_skills`** | `1.9` | `1.9` | Exact match ($\Delta = 0.0$) |
| **`coding_skills`** | `2.4` | `2.4` | Exact match ($\Delta = 0.0$) |
| **`ai_and_ml_skills`** | `3.6` | `3.6` | Exact match ($\Delta = 0.0$) |
| **`dashboard_and_storytelling_skills`** | `1.8` | `1.8` | Exact match ($\Delta = 0.0$) |
| **`salary_hike_high_or_low` (Target)** | **`0` (Low Hike)** | **`1` (High Hike)** | **CONTRADICTORY TARGET** |

### Analytical Interpretation
- The candidate's technical profile is completely invariant across all 5 continuous domains:
  $$\mathbf{x}_{3} = \mathbf{x}_{29} = [2.2, 1.9, 2.4, 3.6, 1.8]^T$$
- However, the binary target reveals contradictory outcomes:
  $$y_3 = 0 \quad \text{vs.} \quad y_{29} = 1$$
- In statistical classification theory, this represents **irreducible label ambiguity** or **measurement noise**. If both observations are retained in model training, no deterministic classifier $f(\mathbf{x})$ can achieve $100\%$ accuracy on this feature vector; the Bayes optimal decision rule would simply predict the empirical posterior probability $P(Y=1 \mid \mathbf{x}) = 0.5$.

---

## 3. Potential Causal Hypotheses

1. **Unobserved Latent Confounders**:
   The two records may represent two distinct junior data scientists who genuinely possess identical technical skill ratings (e.g., graduated from the same training batch), but one secured a high hike due to unmeasured factors such as domain expertise, prior negotiation, educational prestige, or managerial sponsorship.
2. **Data Logging / Longitudinal Replication**:
   The candidate may have been evaluated at two distinct evaluation windows (e.g., Year 1 vs Year 2) where their skills remained static but compensation adjustments differed.
3. **Typographical Key-Punch Error**:
   A data entry specialist may have duplicated the ID or accidentally inverted the binary flag during recording.

Because Phase 2 operates strictly under empirical evidence without access to original survey respondents, we cannot arbitrate between these causal mechanisms.

---

## 4. Governance & Methodological Decision: Dual-Dataset Strategy

Arbitrarily dropping one record or both records without documented justification violates Rule 4 ("No Unjustified Analytical Decisions"). Conversely, ignoring the contradiction could distort regularized logistic regression loss functions or create erratic tree splits.

Therefore, we implement a **Pre-Registered Dual-Dataset Protocol**:

```
                       ┌────────────────────────────────────────┐
                       │   JDS Cleaned Population (N = 139)     │
                       └───────────────────┬────────────────────┘
                                           │
                 ┌─────────────────────────┴─────────────────────────┐
                 ▼                                                   ▼
┌─────────────────────────────────┐                 ┌─────────────────────────────────┐
│     JDS Baseline Dataset        │                 │    JDS Sensitivity Dataset      │
│      `jds_processed.csv`        │                 │ `jds_sensitivity_3291_removed`  │
│           (N = 139)             │                 │           (N = 137)             │
├─────────────────────────────────┤                 ├─────────────────────────────────┤
│ • Retains all valid respondents │                 │ • Excludes both rows of ID 3291 │
│ • Preserves complete N          │                 │ • Purged of label contradiction │
│ • Target: 73 High / 66 Low      │                 │ • Target: 72 High / 65 Low      │
│ • Primary benchmark             │                 │ • Robustness check benchmark    │
└─────────────────────────────────┘                 └─────────────────────────────────┘
```

### Dataset Specifications

### 1. `jds_processed.csv` (Primary Baseline)
- **Sample Size**: $N = 139$
- **Target Distribution**: Class 1 ($52.52\%$, $n = 73$), Class 0 ($47.48\%$, $n = 66$)
- **Purpose**: Serves as the authoritative benchmark dataset for Phase 3 (EDA), Phase 4 (Statistical Testing), and Phase 5 (Primary Skill Modeling).

### 2. `jds_sensitivity_3291_removed.csv` (Sensitivity Benchmark)
- **Sample Size**: $N = 137$
- **Target Distribution**: Class 1 ($52.55\%$, $n = 72$), Class 0 ($47.45\%$, $n = 65$)
- **Purpose**: Serves as the control dataset to evaluate whether model parameter estimates, coefficient signs, odds ratios, or ROC-AUC scores are sensitive to the removal of this ambiguous observation.

---

## 5. Phase 5 Modeling Protocol & Acceptance Criteria

When training machine-learning models in Phase 5:
1. Every candidate algorithm (Logistic Regression, ElasticNet, Random Forest, XGBoost) will be trained on `jds_processed.csv` using 5-fold stratified cross-validation.
2. The identical pipeline and hyperparameter grid will be evaluated on `jds_sensitivity_3291_removed.csv`.
3. **Sensitivity Threshold**:
   - If $|\text{AUC}_{\text{baseline}} - \text{AUC}_{\text{sensitivity}}| \le 0.02$ and skill feature coefficient ranks remain invariant, the findings will be reported as **robust to observational noise**.
   - If significant divergence occurs, both sets of coefficients will be reported transparently in the final Round 2 report to demonstrate methodological integrity to the judging panel.
