# Data Quality Scorecard by Dataset (Phase 1)

## 1. Quality Evaluation Dimensions & Status Definitions

To provide a transparent, standardized assessment of dataset health, each of the four datasets is evaluated across eight standardized data quality dimensions. 

Rather than inventing subjective numerical scores, each dimension is assigned a qualitative status based on rigorous empirical thresholds:
* **GOOD**: Meets all analytical requirements; zero or negligible anomalies; ready for transformation.
* **ATTENTION**: Minor anomalies present (e.g. string formatting, minor skewness, ceiling effects); requires standard preprocessing.
* **PROBLEM**: Substantial quality deficiencies (e.g. high missingness, duplicate keys, severe text noise); requires careful analytical treatment.
* **CRITICAL**: Threatens sample validity or contains fatal label conflicts (e.g. blank rows, conflicting target classifications); requires immediate quarantine or resolution.

---

## 2. Dataset-by-Dataset Quality Scorecards

### 2.1. Scorecard: Data Science Jobs (`DataScience Jobs.csv`)

| Quality Dimension | Status | Empirical Rationale & Evidence |
|---|---|---|
| **Completeness** | **GOOD** | Exactly 0 missing values across all 8 columns ($100.0\%$ complete). |
| **Uniqueness** | **ATTENTION** | 0 exact row duplicates; however, `reference_no` has 142 duplicates (non-unique posting key). |
| **Validity** | **GOOD** | 0 negative or impossible values. `min_salary <= avg_salary <= max_salary` holds for 100% of rows. |
| **Consistency** | **GOOD** | Job titles follow an exact 10-role standardized taxonomy with consistent casing. |
| **Type Correctness** | **ATTENTION** | Salaries are stored as strings with `'L'` suffix rather than native floating-point numbers. |
| **Range Validity** | **ATTENTION** | `num_of_jobs` features extreme right-skewness (max 4,200); `min_experience` reaches 21 years. |
| **Text Quality** | **GOOD** | Minimal text fields; clean company names and role titles. |
| **Target Integrity**| **GOOD** | Unsupervised market dataset; no target variable applicable. |

---

### 2.2. Scorecard: Analytics Jobs (`Analytics Jobs.csv`)

| Quality Dimension | Status | Empirical Rationale & Evidence |
|---|---|---|
| **Completeness** | **PROBLEM** | `job_type` is $75.82\%$ missing (12,011 nulls); `job_description` is $22.14\%$ missing (3,508 nulls). |
| **Uniqueness** | **GOOD** | `s_no` is $100\%$ unique and monotonic (1 to 15,841); 0 exact duplicate rows. |
| **Validity** | **GOOD** | All experience intervals conform to valid patterns (`'X-Y yrs'`); salaries conform to 6 valid bands. |
| **Consistency** | **PROBLEM** | Populated `job_type` entries feature 5 distinct casing variants of "Analytics". |
| **Type Correctness** | **ATTENTION** | Salaries are stored as discrete text intervals (`'10to15'`) and experience as interval strings. |
| **Range Validity** | **GOOD** | All salary brackets and experience bands lie within realistic labor-market limits. |
| **Text Quality** | **ATTENTION** | `job_desig` contains 10,097 free-text strings with significant non-analytics scraping noise. |
| **Target Integrity**| **GOOD** | Unsupervised market posting dataset; no ground-truth target applicable. |

---

### 2.3. Scorecard: Junior Data Scientist Skill Traits (`JDS Skill Traits.xlsx`)

| Quality Dimension | Status | Empirical Rationale & Evidence |
|---|---|---|
| **Completeness** | **CRITICAL** | Exactly 32 completely blank trailing rows (18.71% of sheet) must be stripped. Valid $N=139$ is 100% complete. |
| **Uniqueness** | **CRITICAL** | 2 duplicate IDs; ID `3291` has **conflicting target labels** (0 in row 3; 1 in row 29). |
| **Validity** | **GOOD** | 100% of skill ratings fall strictly within the valid 1.0–5.0 scale bounds. |
| **Consistency** | **ATTENTION** | Header contains hyphen: `maths-stats_skills`. |
| **Type Correctness** | **GOOD** | Ratings loaded cleanly as continuous decimals. |
| **Range Validity** | **ATTENTION** | Extreme ceiling effects in `dashboard_storytelling` (58.3% at 5.0) and `ai_ml` (48.9% at 5.0). |
| **Text Quality** | **GOOD** | Numerical psychometric dataset; minimal text fields. |
| **Target Integrity**| **ATTENTION** | High balance ($52.5\%$ vs $47.5\%$), but compromised by the conflicting label on ID `3291`. |

---

### 2.4. Scorecard: Senior Data Scientist Personality Traits (`SDS Personality Traits.xlsx`)

| Quality Dimension | Status | Empirical Rationale & Evidence |
|---|---|---|
| **Completeness** | **GOOD** | Exactly 0 missing values across all 7 columns for all 161 consultants ($100.0\%$ complete). |
| **Uniqueness** | **ATTENTION** | 9 duplicate IDs across 161 rows; identical IDs have distinct trait scores and distinct targets. |
| **Validity** | **GOOD** | 100% of trait scores fall strictly within the valid psychometric range $[17.0, 68.0]$. |
| **Consistency** | **ATTENTION** | Whitespace anomalies in headers: leading space in `' extraversion'`, spaces in target name. |
| **Type Correctness** | **GOOD** | Trait scores loaded cleanly as integers/floats. |
| **Range Validity** | **GOOD** | Well-dispersed distributions with moderate symmetry; 0 ceiling/floor compression. |
| **Text Quality** | **GOOD** | Numerical psychometric dataset; minimal text fields. |
| **Target Integrity**| **GOOD** | Near-perfect target balance ($52.8\%$ vs $47.2\%$; ratio $1.118:1$). |

---

## 3. Executive Quality Summary Across the Project

```
DATASET                 OVERALL QUALITY READINESS     PRIMARY PHASE 2 REMEDIATION REQUIREMENT
-----------------------------------------------------------------------------------------------
Data Science Jobs       ATTENTION                     Parse currency strings ('L') to float64
Analytics Jobs          PROBLEM                       Manage 75.8% missing job_type & parse text
JDS Skill Traits        CRITICAL                      Strip 32 blank rows & resolve ID 3291 conflict
SDS Personality Traits  ATTENTION                     Sanitize header whitespace & drop ID from ML
```
