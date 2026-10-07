# Missing Value Audit & Completeness Profile (Phase 1)

## 1. Executive Summary

This document presents the empirical completeness audit across all four raw datasets. In strict compliance with Phase 1 Rule 2, **no missing values have been imputed, filled, or dropped**. 

The audit evaluated both actual pandas `NaN` values and string representations of missingness (`""`, `" "`, `"NA"`, `"N/A"`, `"null"`, `"NULL"`, `"-"`, `"--"`, `"unknown"`, `"not available"`). 

The complete column-by-column missingness table is exported in [`outputs/tables/missing_value_profile.csv`](file:///Users/anmolsharma/Desktop/DataScienceTool/outputs/tables/missing_value_profile.csv).

---

## 2. Ranked Missingness Hierarchy Across All Datasets

| Rank | Dataset | Column | Actual NaN Count | String Missing Count | Total Missing Count | Total Rows | Missing % | Severity Category | Missingness Mechanism |
|---|---|---|---|---|---|---|---|---|---|
| **1** | **Analytics Jobs** | `job_type` | 12,011 | 0 | 12,011 | 15,841 | **75.822%** | **>50% (Severe)** | Missing by Omission / Uncategorized |
| **2** | **Analytics Jobs** | `job_description` | 3,508 | 0 | 3,508 | 15,841 | **22.145%** | **20–50% (High)** | Omission by Posting Employer |
| **3** | **JDS Skill Traits** | `id` | 32 | 0 | 32 | 171 | **18.713%** | **5–20% (Moderate)** | Excel File Artifact (Trailing Blank Rows) |
| **4** | **JDS Skill Traits** | `big_data_skills` | 32 | 0 | 32 | 171 | **18.713%** | **5–20% (Moderate)** | Excel File Artifact (Trailing Blank Rows) |
| **5** | **JDS Skill Traits** | `maths-stats_skills`| 32 | 0 | 32 | 171 | **18.713%** | **5–20% (Moderate)** | Excel File Artifact (Trailing Blank Rows) |
| **6** | **JDS Skill Traits** | `coding_skills` | 32 | 0 | 32 | 171 | **18.713%** | **5–20% (Moderate)** | Excel File Artifact (Trailing Blank Rows) |
| **7** | **JDS Skill Traits** | `ai_and_ml_skills` | 32 | 0 | 32 | 171 | **18.713%** | **5–20% (Moderate)** | Excel File Artifact (Trailing Blank Rows) |
| **8** | **JDS Skill Traits** | `dashboard_and_storytelling_skills` | 32 | 0 | 32 | 171 | **18.713%** | **5–20% (Moderate)** | Excel File Artifact (Trailing Blank Rows) |
| **9** | **JDS Skill Traits** | `salary_hike_high_or_low` | 32 | 0 | 32 | 171 | **18.713%** | **5–20% (Moderate)** | Excel File Artifact (Trailing Blank Rows) |
| **10**| **Analytics Jobs** | `key_skills` | 1 | 0 | 1 | 15,841 | **0.006%** | **<1% (Negligible)** | Random Data Omission (MCAR) |
| **11**| **DataScience Jobs** | All 8 Columns | 0 | 0 | 0 | 1,602 | **0.000%** | **0% (Complete)** | Complete Enterprise Dataset |
| **12**| **SDS Personality** | All 7 Columns | 0 | 0 | 0 | 161 | **0.000%** | **0% (Complete)** | Complete Survey Dataset |
| **13**| **Analytics Jobs** | `s_no`, `experience`, `job_desig`, `location`, `salary` | 0 | 0 | 0 | 15,841 | **0.000%** | **0% (Complete)** | Complete Baseline Attributes |

---

## 3. In-Depth Missingness Analysis by Dataset

### 3.1. Analytics Jobs: The `job_type` Anomaly (75.82% Missing)
* **Empirical Count**: 12,011 rows null; only 3,830 rows populated.
* **Distribution of Populated Values**:
  * `'Analytics'`: 2,971
  * `'analytics'`: 746
  * `'ANALYTICS'`: 64
  * `'analytic'`: 30
  * `'Analytic'`: 19
* **Analytical Finding**: All 3,830 populated entries represent casing variations of the exact same category ("Analytics"). There are zero alternative job types (e.g. no "Engineering", "Consulting", "Finance").
* **Mechanism**: Missing Completely at Random / Incomplete Tagging during scraping.
* **Phase 2 Recommended Treatment**: Do not drop the 12,011 postings (which would discard 76% of valid job postings). Standardize the populated entries to `'Analytics'` and classify missing entries as `'Unspecified'`. Because the variable has zero variance beyond "Analytics vs Missing", it must be **excluded from statistical modeling**.

### 3.2. Analytics Jobs: The `job_description` Factor (22.14% Missing)
* **Empirical Count**: 3,508 null rows out of 15,841.
* **Mechanism**: Missing at Random (MAR) depending on whether the job portal scraper extracted full text or only header snippets.
* **Analytical Finding**: While `job_description` has 3,508 missing values, `key_skills` is almost 100% complete (only 1 missing record).
* **Phase 2 Recommended Treatment**: Rely on `key_skills` as the primary technical skill signal; impute missing `job_description` fields with empty strings `""` for text feature extraction.

### 3.3. JDS Skill Traits: The Trailing Blank Row Artifact (18.71% Missing)
* **Empirical Count**: Exactly 32 rows out of 171 contain `NaN` across **every single column** (rows 140–171).
* **Analytical Finding**: These 32 rows are not partially filled employee records; they are empty formatting artifacts at the bottom of the Excel worksheet.
* **Completeness in Valid Sample**: In the valid analytical subset (rows 1–139, $N = 139$), **completeness is exactly 100.0%** across all 5 skill dimensions and the target variable.
* **Phase 2 Recommended Treatment**: Execute `dropna(how='all')` during ingestion to isolate the true $N = 139$ employee sample.

### 3.4. SDS Personality Traits: Complete Case Profile (0.00% Missing)
* **Empirical Finding**: Exactly 0 missing values across all 7 columns for all 161 senior consultants. Complete psychometric profile available for all records.

### 3.5. Data Science Jobs: Complete Case Profile (0.00% Missing)
* **Empirical Finding**: Exactly 0 missing values across all 8 columns for all 1,602 employer requisitions.
