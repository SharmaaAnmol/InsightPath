# Detailed Dataset Audit: Junior Data Scientist Skill Traits (Phase 1)

## 1. Executive Summary

This document establishes the dedicated audit for `JDS Skill Traits.xlsx`. In strict compliance with Phase 1 Rule 1, Rule 2, and Rule 3, **no rows have been dropped, and no scores have been altered**.

The dataset contains employee-level technical skill ratings across five core competencies on a 1.0–5.0 scale alongside a binary salary hike classification target (`salary_hike_high_or_low`). 

The machine-readable summary tables are exported in:
* [`outputs/tables/jds_skill_range_audit.csv`](file:///Users/anmolsharma/Desktop/DataScienceTool/outputs/tables/jds_skill_range_audit.csv)
* [`outputs/tables/jds_target_distribution.csv`](file:///Users/anmolsharma/Desktop/DataScienceTool/outputs/tables/jds_target_distribution.csv)

---

## 2. Structural Dimensions & Trailing Empty Rows Audit

* **Workbook Worksheets**: Exactly 1 sheet named `JDS`.
* **Raw XML Table Rows**: 171 rows, 7 columns.
* **Empirical Row Structure**:
  * Rows 1–139 (Index 0 to 138): **139 valid employee records**.
  * Rows 140–171 (Index 139 to 170): **Exactly 32 completely empty rows** (100% null across all 7 columns).
* **Valid Sample Size**: $N = 139$.
* **Completeness in Valid Sample**: **100.0% completeness** (0 missing values across all skills and target).
* **Phase 2 Directive**: Filter trailing empty cells (`dropna(how='all')`) during data preparation to establish the true analytical sample of $N = 139$.

---

## 3. Skill Dimension Scale & Range Audit (N = 139 Valid Records)

All skill ratings represent continuous decimal evaluations on a 1.0–5.0 scale.

| Skill Dimension | Column Name | Min Score | Q1 | Median | Mean | Q3 | Max Score | Within [1.0, 5.0] | Ceiling 5.0 Count | Ceiling 5.0 % | Skewness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Big Data** | `big_data_skills` | 2.30 | 3.10 | 3.80 | 3.850 | 4.60 | 5.00 | **True** | 25 | 17.99% | -0.198 |
| **Math & Stats** | `maths-stats_skills`| 2.20 | 3.80 | 4.60 | 4.294 | 5.00 | 5.00 | **True** | 57 | 41.01% | -0.999 |
| **Coding** | `coding_skills` | 2.20 | 3.35 | 4.60 | 4.268 | 5.00 | 5.00 | **True** | 62 | 44.60% | -0.932 |
| **AI & ML** | `ai_and_ml_skills` | 2.20 | 4.40 | 4.90 | 4.566 | 5.00 | 5.00 | **True** | 68 | 48.92% | -1.583 |
| **Storytelling** | `dashboard_and_storytelling_skills`| 2.30 | 3.75 | 5.00 | 4.355 | 5.00 | 5.00 | **True** | 81 | **58.27%** | -1.092 |

### Critical Analytical Observations on Skill Distributions:
1. **Valid Boundary Compliance**: 100% of skill ratings fall strictly within $[1.0, 5.0]$. Zero ratings $< 1.0$ or $> 5.0$.
2. **Massive Ceiling Effects**:
   * In `dashboard_and_storytelling_skills`, **58.27% of all junior data scientists received a perfect 5.0 rating** (Median = 5.00).
   * In `ai_and_ml_skills`, **48.92% received a perfect 5.0 rating** (Median = 4.90).
   * In `coding_skills`, **44.60% received a perfect 5.0 rating** (Median = 4.60).
3. **Differentiation Potential**: `big_data_skills` exhibits the lowest ceiling compression ($17.99\%$ at 5.0) and the widest dispersion ($\text{IQR} = 1.50$), indicating it may offer stronger variance to separate high-hike from low-hike candidates.
4. **Header Syntax Anomaly**: `maths-stats_skills` contains a hyphen `-`. Phase 2 action: rename to `maths_stats_skills`.

---

## 4. Target Variable Distribution: `salary_hike_high_or_low`

* **Target Variable**: `salary_hike_high_or_low` $\in \{0, 1\}$
* **Total Valid Instances**: 139
* **Class Frequencies**:
  * **Class 1 (High Salary Hike)**: $N = 73$ ($52.52\%$)
  * **Class 0 (Low Salary Hike)**: $N = 66$ ($47.48\%$)
* **Majority Class**: Class 1
* **Imbalance Ratio**: $1.106 : 1$
* **Assessment**: Near-perfect class balance (~53:47). No synthetic balancing (SMOTE) or threshold shifting is warranted.

---

## 5. Duplicate Identifier & Label Conflict Audit

* **Unique IDs**: 137 unique IDs across 139 rows.
* **Duplicated IDs**: Exactly 2 IDs appear twice:
  * `id = 2223` (Rows 58 & 101): Both instances have consistent outcome `target = 0`.
  * `id = 3291` (Rows 3 & 29): **Conflicting outcome classifications** (Row 3 has `target = 0`; Row 29 has `target = 1`).
* **Phase 2 Directive**: In Phase 2, evaluate model sensitivity with `id = 3291` quarantined vs retained. Ensure `id` is strictly dropped from predictive feature matrices.
