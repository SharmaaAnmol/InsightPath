# Dataset Inventory & Empirical Audit (Phase 0)

## 1. Overview and Environment Audit

This document establishes the empirical inventory and structural audit of all files provided for the SAS CU Hackathon analytics project. The inspection was conducted directly against the filesystem in `/Users/anmolsharma/Desktop/DataScienceTool` using Python runtime inspection (pandas, zipfile/XML parsing) to verify raw schemas, dimensions, missing values, duplicate keys, and formatting anomalies before any data manipulation.

---

## 2. Inventory Summary Table

| Dataset / File Name | File Type | Physical Size | Total Rows | Valid Rows | Columns | Target Variable | Primary Missingness | Key Structural Observation |
|---|---|---|---|---|---|---|---|---|
| `DataScience Jobs.csv` | CSV | 96.4 KB | 1,602 | 1,602 | 8 | None (Unsupervised / Market Data) | 0 missing | Filename has no space; Salary in Lakhs (`'4.5L'`); 142 duplicate `reference_no` |
| `Analytics Jobs.csv` | CSV | 3.61 MB | 15,841 | 15,841 | 8 | None (Market Postings) | `job_type` (75.8%), `job_description` (22.1%) | Free-text titles (10,097 unique); Salary in 6 discrete bands (`'10to15'`, etc.) |
| `JDS Skill Traits.xlsx` | Excel (XLSX) | 16.2 KB | 171 | 139 | 7 | `salary_hike_high_or_low` (Binary 0/1) | 32 completely blank trailing rows | Scores continuous 2.2–5.0; Column `maths-stats_skills` has hyphen; 2 duplicate IDs |
| `SDS Personality Traits.xlsx` | Excel (XLSX) | 14.8 KB | 161 | 161 | 7 | `success_ classification_ high_low` (Binary 0/1) | 0 missing | Big 5 scores range 17–68 (not 1–5); Whitespace in headers; 9 duplicate IDs |
| `Data Description Doc.pdf` | PDF | N/A | N/A | N/A | N/A | N/A | File missing | **NOT VERIFIED FROM SOURCE DATA** (Absent from workspace root) |
| `Problem Context Brief, SAS VFL Demos, Guidelines Dos and Donts.pdf` | PDF | N/A | N/A | N/A | N/A | N/A | File missing | **NOT VERIFIED FROM SOURCE DATA** (Absent from workspace root) |

---

## 3. Detailed Dataset Profiles

### 3.1. Dataset 1: DataScience Jobs (`DataScience Jobs.csv`)

* **Filesystem Name**: `DataScience Jobs.csv` *(Note: No space between "Data" and "Science" in actual filename)*.
* **Storage Location**: `data/raw/DataScience Jobs.csv` (Preserved copy) and workspace root.
* **Row Count**: 1,602 records.
* **Column Count**: 8 attributes.
* **Missing Values**: Exactly 0 across all 8 columns.

#### Schema & Data Types
| Column Name | Inferred Type | Expected Business Meaning | Sample Values | Observations & Anomalies |
|---|---|---|---|---|
| `reference_no` | `int64` | Posting Reference Identifier | 7834, 7862, 5925 | 1,460 unique IDs; 142 duplicate entries. NOT a primary key. |
| `company_name` | `object` | Hiring Organization | TCS, Accenture, IBM | 642 unique companies. Top company postings: TCS (10), Deloitte (10). |
| `job_title` | `object` | Role Classification | Data Scientist, Data Analyst | Exactly 10 unique titles (Data Scientist, Business Analyst, etc.). |
| `min_experience`| `int64` | Minimum Required Years | 2, 3, 5, 0 | Min: 0 yrs, Max: 21 yrs, Mean: 2.80 yrs, Median: 2.0 yrs. |
| `avg_salary` | `object` | Average Annual Salary | `'7.8L'`, `'12.8L'` | String format with `'L'` suffix (Lakhs INR). Requires parsing. |
| `min_salary` | `object` | Minimum Advertised Salary | `'4.5L'`, `'5.8L'` | String format with `'L'` suffix (Lakhs INR). Requires parsing. |
| `max_salary` | `object` | Maximum Advertised Salary | `'16.0L'`, `'23.0L'` | String format with `'L'` suffix (Lakhs INR). Requires parsing. |
| `num_of_jobs` | `int64` | Job Opening Volume | 841, 501, 394 | Positively skewed. Min: 3, Median: 22, Mean: 58.06, Max: 4,200. |

---

### 3.2. Dataset 2: Analytics Jobs (`Analytics Jobs.csv`)

* **Filesystem Name**: `Analytics Jobs.csv`
* **Storage Location**: `data/raw/Analytics Jobs.csv` (Preserved copy) and workspace root.
* **Row Count**: 15,841 records.
* **Column Count**: 8 attributes.
* **Missing Values**:
  * `job_type`: 12,011 missing (75.82%)
  * `job_description`: 3,508 missing (22.14%)
  * `key_skills`: 1 missing (0.01%)
  * `s_no`, `experience`, `job_desig`, `location`, `salary`: 0 missing.

#### Schema & Data Types
| Column Name | Inferred Type | Expected Business Meaning | Sample Values | Observations & Anomalies |
|---|---|---|---|---|
| `s_no` | `int64` | Serial Index | 1, 2, 3 | 15,841 unique sequential indices (1 to 15,841). |
| `experience` | `object` | Experience Range Required | `'6-10 yrs'`, `'2-5 yrs'` | 128 distinct string formats. Requires regex extraction for min/max/mid. |
| `job_description`| `object` | Unstructured Job Text | Text description | 3,508 nulls. Free-form text requiring NLP/keyword extraction. |
| `job_desig` | `object` | Free-text Job Designation | `'Business Analyst'` | 10,097 unique strings. High noise (e.g. data entry, SEO, marketing roles). |
| `job_type` | `object` | Employment / Job Category | `'Analytics'`, NaN | 75.8% missing. Populated values are all casing variations of 'Analytics'. |
| `key_skills` | `object` | Comma-delimited Skills | `'IT Skills, Testing...'` | 1 missing value. Requires tokenization and standardized skill tagging. |
| `location` | `object` | Geographic Location | `'Bengaluru'`, `'Pune'` | 1,355 unique combinations, many multi-city strings (e.g. `'Bengaluru, Chennai'`). |
| `salary` | `object` | Categorical Salary Band | `'10to15'`, `'15to25'` | 6 discrete categorical bands in Lakhs INR. No continuous numbers. |

---

### 3.3. Dataset 3: Junior Data Scientist Skill Traits (`JDS Skill Traits.xlsx`)

* **Filesystem Name**: `JDS Skill Traits.xlsx`
* **Storage Location**: `data/raw/JDS Skill Traits.xlsx` (Preserved copy) and workspace root.
* **Spreadsheet Dimensions**: 171 rows in XML table, 7 columns.
* **Valid Analytical Sample**: 139 records (Rows 140–171 are 100% blank trailing cells).
* **Missing Values in Valid Sample**: Exactly 0 missing values across all features and target.

#### Schema & Summary Statistics (N = 139 Valid Records)
| Column Name | Type | Scale / Range | Mean ± Std | Median | Observations & Data Quality Notes |
|---|---|---|---|---|---|
| `id` | `int64` | 2007 – 4000 | 2958.5 ± 604.5 | 2963.0 | 137 unique IDs. 2 duplicates (`id` 2223, 3291). ID 3291 has conflicting target values! |
| `big_data_skills` | `float64` | 2.30 – 5.00 | 3.850 ± 0.847 | 3.80 | Rated on 1–5 scale (continuous decimal ratings). |
| `maths-stats_skills`| `float64` | 2.20 – 5.00 | 4.294 ± 0.844 | 4.60 | Header contains hyphen `-`. Negatively skewed towards higher scores. |
| `coding_skills` | `float64` | 2.20 – 5.00 | 4.268 ± 0.893 | 4.60 | Negatively skewed towards higher scores. |
| `ai_and_ml_skills` | `float64` | 2.20 – 5.00 | 4.566 ± 0.667 | 4.90 | Highest mean skill score. Substantial ceiling effect near 5.0. |
| `dashboard_and_storytelling_skills`| `float64` | 2.30 – 5.00 | 4.355 ± 0.933 | 5.00 | 50% of junior respondents scored 5.0. High ceiling effect. |
| `salary_hike_high_or_low` | `int64` | Binary {0, 1} | 0.525 ± 0.501 | 1.00 | **Target variable**: Class 1 = 73 (52.5%), Class 0 = 66 (47.5%). Balanced. |

---

### 3.4. Dataset 4: Senior Data Scientist Personality Traits (`SDS Personality Traits.xlsx`)

* **Filesystem Name**: `SDS Personality Traits.xlsx`
* **Storage Location**: `data/raw/SDS Personality Traits.xlsx` (Preserved copy) and workspace root.
* **Spreadsheet Dimensions**: 161 rows, 7 columns.
* **Valid Analytical Sample**: 161 records.
* **Missing Values**: Exactly 0 across all columns.

#### Schema & Summary Statistics (N = 161 Records)
| Column Name in File | Sanitized Name | Scale / Range | Mean ± Std | Median | Observations & Data Quality Notes |
|---|---|---|---|---|---|
| `id` | `id` | 8001 – 8979 | 8484.6 ± 280.4 | 8504.0 | 152 unique IDs. 9 duplicate IDs with differing trait scores and targets. |
| `neuroticism` | `neuroticism` | 17.0 – 68.0 | 36.19 ± 11.27 | 34.0 | Raw Big Five score scale (not 1–5 scale). Moderately normal. |
| `' extraversion'` | `extraversion` | 17.0 – 67.0 | 43.21 ± 12.14 | 45.0 | **Column header has leading space**. Raw score scale. |
| `openness_to_experience`| `openness_to_experience`| 18.0 – 65.0 | 41.33 ± 11.32 | 44.0 | Raw score scale. |
| `agreeableness` | `agreeableness` | 17.0 – 68.0 | 44.60 ± 11.29 | 46.0 | Raw score scale. |
| `conscientiousness` | `conscientiousness` | 18.0 – 66.0 | 45.21 ± 13.21 | 49.0 | Raw score scale. Wide dispersion. |
| `'success_ classification_ high_low'` | `success_classification_high_low`| Binary {0, 1} | 0.528 ± 0.501 | 1.00 | **Header contains internal spaces**. Class 1 = 85 (52.8%), Class 0 = 76 (47.2%). |

---

## 4. Empirical Discrepancy Analysis

The following discrepancies between the initial problem briefing / documentation assumptions and the physical data files were verified:

| Item | Problem Brief / Documentation Assumption | Empirical File Reality | Analytical Impact & Resolution Strategy |
|---|---|---|---|
| **Data Science Jobs Filename** | Expected `Data Science Jobs.csv` | Physical file is `DataScience Jobs.csv` (no space) | Resolved programmatically; preserve exact physical filename without renaming. |
| **PDF Documentation** | Expected `Data Description Doc.pdf` and `Problem Context Brief...pdf` | Files absent from workspace root | Documented as **NOT VERIFIED FROM SOURCE DATA**; context derived from brief. |
| **JDS Dataset Size** | Stated or implied ~172 records | Exactly 139 valid records; 32 blank trailing Excel rows | 32 null rows must be stripped during ingestion; analytical N = 139. |
| **JDS Column Naming** | Expected standard snake_case | Header contains hyphen: `maths-stats_skills` | Standardize to snake_case (`maths_stats_skills`) during preprocessing pipeline. |
| **SDS Trait Scales** | Implied standard Likert/normalized scale | Scores range between 17 and 68 | Represents raw psychometric inventory scores (e.g., IPIP Big Five); do not force into 1–5 range without justification. |
| **SDS Column Naming** | Expected clean snake_case | Leading space in `' extraversion'`, spaces in `'success_ classification_ high_low'` | Sanitize headers immediately in data loading layer. |
| **Row Identifier Integrity** | `id` and `reference_no` might be unique keys | Duplicate IDs found in DataScience Jobs (142), JDS (2), and SDS (9) | **Critical**: Identifiers are non-unique and must NOT be used as relational keys or modeling features. |
| **Analytics Jobs Salary** | Numerical salary figures | 6 discrete categorical bands (`'10to15'`, `'15to25'`, etc.) | Requires ordinal encoding and band-midpoint estimation rather than continuous regression. |
| **Analytics Jobs Job Type** | Structured categorical feature | 75.8% missing; populated values are solely casing variants of 'Analytics' | Low informational utility; document high missingness and treat as uninformative. |

---

## 5. Storage and Integrity Verification

All 4 raw source datasets have been duplicated into `data/raw/` to ensure absolute preservation. The original files in the project root remain 100% untouched and unmodified.
