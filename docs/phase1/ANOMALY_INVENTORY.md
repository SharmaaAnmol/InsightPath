# Consolidated Anomaly & Quality Issue Inventory (Phase 1)

## 1. Executive Summary

This document establishes the centralized inventory of all data quality anomalies, structural flaws, and formatting issues identified across the four datasets during Phase 1. 

In strict adherence to Phase 1 non-negotiable rules:
* **Zero anomalies have been modified, removed, or imputed.**
* Every anomaly is classified by severity (**CRITICAL**, **HIGH**, **MEDIUM**, **LOW**) with an explicit recommended remediation protocol for Phase 2.

The machine-readable summary table is exported in [`outputs/tables/anomaly_inventory.csv`](file:///Users/anmolsharma/Desktop/DataScienceTool/outputs/tables/anomaly_inventory.csv).

---

## 2. Consolidated Anomaly Inventory Table

| # | Dataset | Column / Location | Anomaly Type | Affected Count | Affected % | Example Values | Severity | Recommended Phase 2 Remediation Protocol |
|---|---|---|---|---|---|---|---|---|
| **1** | **JDS Skill Traits** | Rows 140–171 (All Columns) | Trailing Empty Rows | 32 rows | 18.71% | All 7 fields `None` / `NaN` | **CRITICAL** | Filter out completely blank trailing rows (`dropna(how='all')`); analytical sample $N = 139$. |
| **2** | **JDS Skill Traits** | `id` | Conflicting Target Labels for Duplicate ID | 4 rows (2 IDs) | 2.88% | ID `3291` has target 0 in row 3, target 1 in row 29 | **CRITICAL** | Audit feature vector similarity; evaluate model training sensitivity with and without `id = 3291` ($N = 137$). |
| **3** | **SDS Personality Traits**| Headers: `' extraversion'`, `'success_ classification_ high_low'` | Whitespace in Column Names | 2 headers | 28.57% | Leading space in extraversion; internal spaces in target | **HIGH** | Sanitize column headers: `.str.strip().str.replace(' ', '_').str.lower()`. |
| **4** | **Analytics Jobs** | `job_type` | Extreme Missingness & Casing Collision | 12,011 rows | 75.82% | 12,011 nulls; populated entries: `'Analytics'`, `'analytics'`, `'ANALYTICS'` | **HIGH** | Standardize casing; document as uninformative due to $>75\%$ nulls; exclude from ML models. |
| **5** | **DataScience Jobs** | `avg_salary`, `min_salary`, `max_salary` | String Representation of Continuous Currency | 1,602 rows | 100.0% | `'7.8L'`, `'4.5L'`, `'16.0L'` | **HIGH** | Build parser stripping `'L'`, cast to `float64` (Lakhs INR); derive `salary_spread`. |
| **6** | **Analytics Jobs** | `salary` | Textual Categorical Salary Intervals | 15,841 rows | 100.0% | `'10to15'`, `'15to25'`, `'6to10'` | **HIGH** | Map to ordered factor ($1 \dots 6$) and interval midpoints ($[1.5, 4.5, \dots, 37.5]$). |
| **7** | **Analytics Jobs** | `experience` | Unstructured String Intervals | 15,841 rows | 100.0% | `'6-10 yrs'`, `'2-5 yrs'`, `'5-10 yrs'` | **HIGH** | Regex extraction of `min_experience`, `max_experience`, and `midpoint_experience`. |
| **8** | **SDS Personality Traits**| `id` | Anonymized ID Multiplicity | 18 rows (9 IDs) | 11.18% | ID `8065` appears twice with different traits and targets | **HIGH** | Do NOT treat ID as primary key; treat rows as distinct observations; drop ID from modeling. |
| **9** | **Analytics Jobs** | `job_description` | Moderate-to-High Missingness | 3,508 rows | 22.14% | `NaN` | **MEDIUM** | Impute missing descriptions with `""`; rely on `key_skills` as primary skill signal. |
| **10**| **DataScience Jobs** | `reference_no` | Non-Unique Requisition Identifiers | 142 rows | 8.86% | Ref `1024` shared by Exl India & IHS Markit | **MEDIUM** | Retain rows as distinct postings; strictly exclude `reference_no` from analytical modeling. |
| **11**| **DataScience Jobs** | `num_of_jobs` | Extreme Right Skewness & Bulk Hiring Outliers | 164 rows | 10.24% | Max = 4,200 vs Median = 22 | **MEDIUM** | Retain all records (genuine bulk hiring); engineer $\log_{10}(\text{num\_of\_jobs})$ for sensitivity. |
| **12**| **JDS Skill Traits** | `ai_and_ml_skills`, `storytelling_skills` | Severe Ceiling Compression | 81 rows (Storytelling) | 58.27% | 58.3% of juniors score 5.0 | **MEDIUM** | Use non-parametric comparative tests (Mann–Whitney U) rather than t-tests. |
| **13**| **JDS Skill Traits** | `maths-stats_skills` | Hyphen in Column Identifier | 1 header | 14.29% | `maths-stats_skills` | **LOW** | Rename to snake_case `maths_stats_skills`. |
| **14**| **Analytics Jobs** | `key_skills` | Single Missing Record | 1 row | 0.006% | `NaN` in row 10,482 | **LOW** | Impute with `"Not Specified"`. |

---

## 3. Severity Level Definitions

* **CRITICAL**: Threatens data integrity, sample size validity, or creates fatal label contradictions if unaddressed. Requires immediate resolution prior to modeling.
* **HIGH**: Inhibits mathematical operations, introduces string/case collisions, or corrupts column references. Requires standard programmatic parsing in Phase 2.
* **MEDIUM**: Substantial missingness, non-unique identifiers, or extreme skewness that could bias statistical estimates if unmanaged.
* **LOW**: Minor syntactic, punctuation, or single-record omissions that do not compromise overarching analytical validity.
