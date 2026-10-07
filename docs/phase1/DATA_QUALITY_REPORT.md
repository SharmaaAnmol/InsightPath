# Comprehensive Data Quality Report (Phase 1 Deliverable)

**Project**: SAS CU Hackathon Analytics Project — Round 2  
**Role**: Lead Data Scientist & Analytics Architecture Team  
**Phase**: **Phase 1 — Data Audit & Quality Profiling (Final Report)**  
**Status**: **AUDIT COMPLETE — NO RAW DATA MODIFIED**

---

## 1. Executive Summary

This report establishes the definitive empirical audit of the four raw datasets provided for the SAS CU Hackathon. Executed in strict compliance with the Phase 1 non-negotiable rules, this audit was conducted without modifying, dropping, cleaning, imputing, transforming, or modeling any source data.

### Summary of Audit Facts
* **Verified Datasets**: 4 datasets audited in memory against byte-for-byte verified raw files (`DataScience Jobs.csv`, `Analytics Jobs.csv`, `JDS Skill Traits.xlsx`, `SDS Personality Traits.xlsx`).
* **Total Audited Records**: 17,775 total rows across the four files (17,743 valid analytical records; 32 blank trailing Excel rows).
* **Target Classes**: Both supervised targets (`salary_hike_high_or_low` in JDS; `success_classification_high_low` in SDS) exhibit near-perfect class balance (~53% positive to ~47% negative).
* **Primary Structural Flaws**:
  1. 32 trailing empty rows in `JDS Skill Traits.xlsx` (18.7% of sheet).
  2. Severe missingness in `Analytics Jobs.csv` `job_type` (75.82%) and moderate missingness in `job_description` (22.14%).
  3. Whitespace anomalies in SDS headers (`' extraversion'`, `'success_ classification_ high_low'`).
  4. String representations for numerical salaries (`'7.8L'`) and discrete salary brackets (`'10to15'`).
  5. Conflicting target classifications on duplicate ID `3291` in JDS.
  6. Zero cross-dataset identifier overlap between JDS and SDS, confirming that row-level joining is invalid.

Throughout this document, findings are explicitly delineated as **[FACT]**, **[INTERPRETATION]**, or **[RECOMMENDATION]**.

---

## 2. Dataset Inventory

* **[FACT]**: All four raw files exist in `/Users/anmolsharma/Desktop/DataScienceTool` and were duplicated into `data/raw/` with verified matching SHA-256 digests.
* **[FACT]**: The original PDF documents (`Data Description Doc.pdf` and `Problem Context Brief...pdf`) were not present in the workspace and are classified as **NOT VERIFIED FROM SOURCE DATA**.

| Dataset Name | Physical Filename | Format | Storage Size | Row Count | Col Count | Sheet Name | Valid Analytical Records |
|---|---|---|---|---|---|---|---|
| Data Science Jobs | `DataScience Jobs.csv` | CSV | 96,390 Bytes | 1,602 | 8 | N/A | 1,602 |
| Analytics Jobs | `Analytics Jobs.csv` | CSV | 3,610,518 Bytes | 15,841 | 8 | N/A | 15,841 |
| JDS Skill Traits | `JDS Skill Traits.xlsx` | XLSX | 16,190 Bytes | 171 | 7 | `['JDS']` | 139 (32 blank rows) |
| SDS Personality Traits| `SDS Personality Traits.xlsx`| XLSX | 14,839 Bytes | 161 | 7 | `['SDS']` | 161 |

---

## 3. Data-Type Findings

* **[FACT]**: In `DataScience Jobs.csv`, `avg_salary`, `min_salary`, and `max_salary` are stored as string `object` types due to the `'L'` suffix (Lakhs notation).
* **[FACT]**: In `Analytics Jobs.csv`, `experience` is stored as text intervals (`'6-10 yrs'`), and `salary` is stored as discrete string intervals (`'10to15'`).
* **[FACT]**: In `JDS Skill Traits.xlsx` and `SDS Personality Traits.xlsx`, all ratings and trait scores are loaded from XML as strings/objects before casting.
* **[INTERPRETATION]**: None of the salary or experience fields can be utilized for mathematical modeling in their current raw state without parser development.
* **[RECOMMENDATION]**: In Phase 2, develop dedicated string parsers to extract numeric salary floats, experience integer bounds, and ordinal salary factors.

---

## 4. Missing Values

* **[FACT]**: Ranked missingness across all 30 audited columns:
  1. `Analytics Jobs.job_type`: 12,011 missing (**75.82%**)
  2. `Analytics Jobs.job_description`: 3,508 missing (**22.14%**)
  3. `JDS Skill Traits` (all 7 columns): 32 missing (**18.71%**)
  4. `Analytics Jobs.key_skills`: 1 missing (**0.006%**)
  5. All other 26 columns across all datasets: **0 missing (0.00%)**.
* **[FACT]**: String representation audit (`" "`, `"NA"`, `"null"`, `"-"`, etc.) revealed 0 hidden textual missing values.
* **[INTERPRETATION]**: The 32 null rows in JDS are Excel formatting artifacts; excluding them leaves a 100% complete analytical sample ($N = 139$). The 75.8% missingness in `job_type` renders it uninformative for predictive modeling.
* **[RECOMMENDATION]**: Drop trailing empty rows in JDS; impute `job_description` with `""`; impute `key_skills` with `"Not Specified"`; exclude `job_type` from modeling.

---

## 5. Duplicate Records

* **[FACT]**: Exactly **0 full-row duplicate records** exist across any of the four datasets.
* **[FACT]**: Primary identifier multiplicity is present:
  * `DataScience Jobs.reference_no`: 142 duplicate values (shared across different companies).
  * `Analytics Jobs.s_no`: 0 duplicate values (100% unique sequence).
  * `JDS Skill Traits.id`: 2 duplicate values (`id` 2223 and `id` 3291).
  * `SDS Personality Traits.id`: 9 duplicate values (e.g. `id` 8065, 8198).
* **[FACT]**: In JDS, `id = 3291` has conflicting target values: `target = 0` in row 3, and `target = 1` in row 29.
* **[INTERPRETATION]**: Identifiers are non-unique posting codes or anonymized subject hashes, not unique primary keys. The conflicting target on ID 3291 creates label noise.
* **[RECOMMENDATION]**: In Phase 2, quarantine `id = 3291` to evaluate model sensitivity with ($N=139$) and without ($N=137$) conflicting labels. Drop all identifiers from modeling feature sets.

---

## 6. Identifier Integrity & Cross-Dataset Non-Overlap

* **[FACT]**: JDS `id` values range from 2007 to 4000. SDS `id` values range from 8001 to 8979.
* **[FACT]**: **Zero overlapping IDs exist between JDS and SDS** ($N_{\text{overlap}} = 0$).
* **[FACT]**: The 21 collisions between JDS IDs and Data Science Jobs `reference_no` represent coincidental integer overlap between employee IDs and external job requisition numbers.
* **[INTERPRETATION]**: Any attempt to perform row-level merging across datasets would fabricate non-existent relationships and invalidate the analysis.
* **[RECOMMENDATION]**: Enforce conceptual evidence triangulation; strictly prohibit row-level joins.

---

## 7. Numerical Variables & Outlier Profile

* **[FACT]**: In `DataScience Jobs.csv`:
  * `min_experience`: Mean = 2.80 yrs, Median = 2.0 yrs, Max = 21 yrs. 39 records ($2.43\%$) exceed Tukey upper bound ($8.5$ yrs).
  * `num_of_jobs`: Mean = 58.06, Median = 22.0, Max = 4,200. 164 records ($10.24\%$) exceed Tukey upper bound ($103.6$), creating severe skewness ($+12.83$).
* **[FACT]**: In `JDS Skill Traits.xlsx` ($N = 139$):
  * All 5 skills conform strictly to the $[1.0, 5.0]$ boundary.
  * Ceiling compression at 5.0: Storytelling ($58.27\%$), AI/ML ($48.92\%$), Coding ($44.60\%$), Math/Stats ($41.01\%$), Big Data ($17.99\%$).
  * AI/ML features 18 Tukey low outliers ($[2.2, 3.4]$) due to tight clustering near 5.0.
* **[FACT]**: In `SDS Personality Traits.xlsx` ($N = 161$):
  * Trait scores span $[17.0, 68.0]$ (raw psychometric inventory scores).
  * Agreeableness features 5 low outliers ($[17, 20]$).
* **[INTERPRETATION]**: Outliers in `num_of_jobs` represent genuine enterprise bulk hiring. Ceiling effects in JDS reflect high technical ratings across junior cohorts, mandating non-parametric testing.
* **[RECOMMENDATION]**: Retain all outliers. Engineer $\log_{10}(\text{num\_of\_jobs})$ in Phase 2. Use Mann–Whitney U tests in Phase 4.

---

## 8. Categorical Variables

* **[FACT]**: `DataScience Jobs.job_title` has exactly 10 standardized titles with zero casing or whitespace anomalies.
* **[FACT]**: `Analytics Jobs.job_type` has 5 casing variants of "Analytics" (`'Analytics'`, `'analytics'`, `'ANALYTICS'`, `'analytic'`, `'Analytic'`).
* **[FACT]**: `Analytics Jobs.salary` contains 6 discrete ordinal brackets (`'10to15'`, `'15to25'`, `'6to10'`, `'0to3'`, `'3to6'`, `'25to50'`) covering 100% of rows.
* **[FACT]**: `Analytics Jobs.location` contains 1,355 unique strings with frequent multi-city combinations.
* **[RECOMMENDATION]**: Standardize `job_type` casing; encode `salary` as ordinal ranks and midpoints; cluster `location` into 7 primary metropolitan hubs.

---

## 9. Text Variables

* **[FACT]**: `Analytics Jobs.job_description` has short character lengths (Median = 104, Max = 109 chars) and word counts (Median = 15 words), representing truncated teaser snippets.
* **[FACT]**: `Analytics Jobs.key_skills` has an average of 5.0 comma-delimited tokens per posting (1 missing record).
* **[FACT]**: Whitespace in headers: SDS Header 3 has a leading space (`' extraversion'`); Header 7 has internal spaces (`'success_ classification_ high_low'`). JDS Header 3 contains a hyphen (`maths-stats_skills`).
* **[RECOMMENDATION]**: Impute `job_description` with `""`; tokenize `key_skills` into binary multi-hot indicators; sanitize column headers in Phase 2.

---

## 10. Data Science Jobs Specific Findings

* **[FACT]**: All 1,602 rows satisfy mathematical salary consistency: $\text{min\_salary} \le \text{avg\_salary} \le \text{max\_salary}$.
* **[FACT]**: Parsed salary ranges in Lakhs INR: Min salary ranges $0.2\text{L} - 55.0\text{L}$; Avg salary ranges $1.4\text{L} - 82.0\text{L}$; Max salary ranges $2.0\text{L} - 102.0\text{L}$.
* **[RECOMMENDATION]**: Derive `salary_spread = max_salary - min_salary` as a proxy for employer compensation flexibility.

---

## 11. Analytics Jobs Specific Findings

* **[FACT]**: Scraped designations in `job_desig` (10,097 unique strings) include non-analytics roles (e.g. data entry, telecalling, SEO).
* **[RECOMMENDATION]**: Filter and categorize `job_desig` into 5 core analytical role families using keyword matching in Phase 2.

---

## 12. JDS Specific Findings

* **[FACT]**: Sheet contains 171 rows; rows 140–171 (32 rows) are completely blank trailing Excel artifacts.
* **[FACT]**: Valid sample $N = 139$ is 100% complete across all 5 skills and the target.
* **[FACT]**: Duplicate ID `3291` has conflicting target values (0 vs 1).
* **[RECOMMENDATION]**: Filter 32 blank rows; prepare sensitivity subset with ID 3291 quarantined.

---

## 13. SDS Specific Findings

* **[FACT]**: Trait scores represent raw psychometric inventory scales $[17, 68]$ rather than 1–5 Likert scales.
* **[FACT]**: 9 duplicate IDs represent repeated evaluations or subject hashes with distinct scores.
* **[RECOMMENDATION]**: Standardize trait scores strictly within cross-validation folds in Phase 6.

---

## 14. Target Balance

* **[FACT]**: JDS Target (`salary_hike_high_or_low`): Class 1 = 73 ($52.52\%$), Class 0 = 66 ($47.48\%$). Imbalance ratio = $1.106:1$.
* **[FACT]**: SDS Target (`success_classification_high_low`): Class 1 = 85 ($52.80\%$), Class 0 = 76 ($47.20\%$). Imbalance ratio = $1.118:1$.
* **[INTERPRETATION]**: Both targets exhibit near-parity. Synthetic rebalancing (SMOTE) is unnecessary and methodologically inappropriate.
* **[RECOMMENDATION]**: Use Stratified K-Fold CV without synthetic sampling in Phases 5 and 6.

---

## 15. Consolidated Anomaly Inventory

* **[FACT]**: 14 distinct data quality anomalies cataloged across all datasets, spanning 2 Critical, 6 High, 4 Medium, and 2 Low severity items.
* Full details documented in [`docs/phase1/ANOMALY_INVENTORY.md`](file:///Users/anmolsharma/Desktop/DataScienceTool/docs/phase1/ANOMALY_INVENTORY.md).

---

## 16. Cross-Dataset Observations

* **[FACT]**: Datasets represent distinct observational units (postings, vacancies, junior employees, senior consultants).
* **[INTERPRETATION]**: The four datasets provide complementary evidence across the career lifecycle. Methodological triangulation is the only defensible synthesis strategy.

---

## 17. Phase 2 Cleaning Requirements

* **[RECOMMENDATION]**: 14 prioritized cleaning and transformation requirements specified in [`docs/phase1/PHASE_2_CLEANING_REQUIREMENTS.md`](file:///Users/anmolsharma/Desktop/DataScienceTool/docs/phase1/PHASE_2_CLEANING_REQUIREMENTS.md).

---

## 18. Risks & Analytical Considerations

1. **Small Sample Power in JDS ($N=139$) and SDS ($N=161$)**: Complex non-linear models run high risks of overfitting. Regularized, shallow architectures are mandatory.
2. **Ceiling Compression in JDS**: High proportion of perfect 5.0 scores requires non-parametric comparative testing.
3. **Observational Framing**: Findings represent observed associations; causal language must be strictly avoided.

---

## 19. Phase 1 Conclusion

Phase 1 has achieved complete, reproducible data profiling across all four datasets. The data quality terrain is fully mapped, anomalies are documented, and remediation requirements are defined. **Phase 1 is complete. No Phase 2 actions have been initiated.**
