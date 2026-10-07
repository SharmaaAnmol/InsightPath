# Target Variable & Class Balance Audit (Phase 1)

## 1. Executive Summary

This document establishes the empirical class balance audit for the supervised classification targets in `JDS Skill Traits.xlsx` and `SDS Personality Traits.xlsx`. In strict compliance with Phase 1 Rule 4 and Rule 13:
* **No rebalancing, oversampling, undersampling, or synthetic data generation (SMOTE) has been performed.**
* Both target variables exhibit **exceptional empirical balance** (~53% positive class to ~47% negative class).

The machine-readable summary table is exported in [`outputs/tables/target_class_balance.csv`](file:///Users/anmolsharma/Desktop/DataScienceTool/outputs/tables/target_class_balance.csv).

---

## 2. Target Class Balance Audit Table

| Dataset | Target Variable Name | Total Valid Records | Class 0 Count (Negative) | Class 0 % | Class 1 Count (Positive) | Class 1 % | Majority Class | Minority Class | Imbalance Ratio |
|---|---|---|---|---|---|---|---|---|---|
| **JDS Skill Traits** | `salary_hike_high_or_low` | 139 | 66 | 47.48% | 73 | 52.52% | Class 1 (High Hike) | Class 0 (Low Hike) | **1.106 : 1** |
| **SDS Personality Traits**| `success_ classification_ high_low`| 161 | 76 | 47.20% | 85 | 52.80% | Class 1 (High Success)| Class 0 (Low Success)| **1.118 : 1** |

---

## 3. In-Depth Class Balance Diagnostics

### 3.1. JDS Target: `salary_hike_high_or_low`
* **Semantic Definition**: 
  * `1` = Junior Data Scientist received an above-average / high salary hike during performance review.
  * `0` = Junior Data Scientist received a standard / below-average salary hike.
* **Sample Size**: 139 valid employee instances (after excluding the 32 empty trailing rows).
* **Baseline Naive Classifier Accuracy**: $52.52\%$ (majority class accuracy).
* **Imbalance Assessment**: An imbalance ratio of $1.106 : 1$ indicates essentially negligible asymmetry. Synthetic oversampling (e.g. SMOTE) on an $N=139$ dataset would risk creating artificial data points and severe overfitting without any substantive benefit.

### 3.2. SDS Target: `success_ classification_ high_low`
* **Semantic Definition**:
  * `1` = Senior / customer-facing Data Scientist observed as highly successful in client-facing consulting.
  * `0` = Senior Data Scientist observed as low-performing / struggling in client-facing engagements.
* **Sample Size**: 161 consultant instances.
* **Baseline Naive Classifier Accuracy**: $52.80\%$ (majority class accuracy).
* **Imbalance Assessment**: An imbalance ratio of $1.118 : 1$ represents near-parity. Stratified splitting preserves exact 53:47 representation across training and validation splits.

---

## 4. Modeling Implications for Phase 5 and Phase 6

1. **Stratification Protocol**: Use `StratifiedKFold` (5 folds $\times$ 5 repeats = 25 splits) to ensure every fold contains exactly $\sim 15$ positive and $\sim 13$ negative cases in JDS, and $\sim 17$ positive and $\sim 15$ negative cases in SDS.
2. **Metric Selection**: Because classes are balanced, standard Accuracy and Balanced Accuracy will align closely. However, evaluation will prioritize **ROC-AUC** (discrimination ability) and **Macro F1-Score** (harmonic mean of class precision and recall) to detect any asymmetric errors.
3. **Threshold Calibration**: The standard decision threshold ($P \ge 0.50$) serves as a well-calibrated initial baseline.
