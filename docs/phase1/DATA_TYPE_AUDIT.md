# Data Type Profile & Semantic Audit (Phase 1)

## 1. Executive Summary

This document details the data type profile across all 30 variables in the four raw datasets. In strict adherence to Phase 1 Rule 2, **no data types have been converted in place**. Storing variables in incompatible or non-standard formats (such as numerical currency stored as string notations or ordinal brackets stored as text) represents an empirical data quality finding to be remediated in Phase 2.

The complete machine-readable profile is exported in [`outputs/tables/data_type_profile.csv`](file:///Users/anmolsharma/Desktop/DataScienceTool/outputs/tables/data_type_profile.csv).

---

## 2. Dataset-by-Dataset Data Type Profiles

### 2.1. Dataset 1: Data Science Jobs (`DataScience Jobs.csv`)

| Column Name | Raw Storage Dtype | Inferred Semantic Role | True Semantic Type | Unique Count | Unique % | Example Raw Values | Phase 1 Finding & Phase 2 Action |
|---|---|---|---|---|---|---|---|
| `reference_no` | `int64` | Identifier / Requisition ID | Categorical / Key | 1,460 | 91.14% | `[7834, 7862, 5925]` | 142 duplicate values. Do NOT treat as primary key or ML feature. |
| `company_name` | `object` | Hiring Organization | Categorical / Text | 642 | 40.07% | `['TCS', 'Accenture', 'IBM']` | Clean text, casing variations present across long tail. |
| `job_title` | `object` | Role Classification | Categorical | 10 | 0.62% | `['Data Scientist', 'Business Analyst']` | Exactly 10 standardized titles. |
| `min_experience`| `int64` | Experience Barrier | Numeric (Years) | 16 | 1.00% | `[2, 3, 5]` | Integer years (0 to 21). Valid numeric type. |
| `avg_salary` | `object` | Mean Compensation | Continuous Numeric (Lakhs INR) | 158 | 9.86% | `['7.8L', '12.8L', '13.4L']` | **Mismatch**: Stored as string with `'L'`. Phase 2: parse to `float64`. |
| `min_salary` | `object` | Minimum Compensation | Continuous Numeric (Lakhs INR) | 124 | 7.74% | `['4.5L', '5.8L', '5.3L']` | **Mismatch**: Stored as string with `'L'`. Phase 2: parse to `float64`. |
| `max_salary` | `object` | Maximum Compensation | Continuous Numeric (Lakhs INR) | 164 | 10.24% | `['16.0L', '23.0L', '25.0L']`| **Mismatch**: Stored as string with `'L'`. Phase 2: parse to `float64`. |
| `num_of_jobs` | `int64` | Requisition Volume | Numeric (Count) | 134 | 8.36% | `[841, 501, 394]` | Severe right skewness (max 4,200). Valid integer type. |

---

### 2.2. Dataset 2: Analytics Jobs (`Analytics Jobs.csv`)

| Column Name | Raw Storage Dtype | Inferred Semantic Role | True Semantic Type | Unique Count | Unique % | Example Raw Values | Phase 1 Finding & Phase 2 Action |
|---|---|---|---|---|---|---|---|
| `s_no` | `int64` | Serial Index | Integer Key | 15,841 | 100.0% | `[1, 2, 3]` | Perfectly monotonic sequence (1 to 15,841). Drop from ML. |
| `experience` | `object` | Experience Requirement | Text Range | 128 | 0.81% | `['6-10 yrs', '8-12 yrs', '3-8 yrs']`| **Mismatch**: Text intervals. Phase 2: regex extract `min_exp`, `max_exp`. |
| `job_description`| `object` | Job Posting Description | Unstructured Text / NLP | 7,859 | 49.61% | `['Text description...']` | 3,508 nulls. High cardinality free text. Phase 2: impute `""`. |
| `job_desig` | `object` | Advertised Designation | Free-text Categorical | 10,097 | 63.74% | `['Business Analyst', 'Data Scientist']`| High cardinality & noise (data entry, SEO). Phase 2: role grouping. |
| `job_type` | `object` | Job Family Flag | Binary Categorical | 5 | 0.03% | `['Analytics', 'analytics', 'ANALYTICS']`| **Mismatch**: 75.8% missing. Populated values casing variants. Phase 2: standardize casing. |
| `key_skills` | `object` | Skill Inventory | Text / Delimited | 11,155 | 70.42% | `['IT Skills, Testing...']` | Comma-delimited list. Phase 2: tokenize & multi-hot encode. |
| `location` | `object` | Geographic Hiring Location | Categorical / Multi-city | 1,355 | 8.55% | `['Bengaluru, Chennai', 'Bengaluru']` | Multi-city strings present. Phase 2: map to primary metro hubs. |
| `salary` | `object` | Advertised Compensation | Categorical (Ordinal Band) | 6 | 0.04% | `['6to10', '10to15', '0to3']` | **Mismatch**: 6 discrete string brackets. Phase 2: ordinal encode & midpoints. |

---

### 2.3. Dataset 3: Junior Data Scientist Skill Traits (`JDS Skill Traits.xlsx`)

*Note: Raw XML parsing loads cell strings into memory before type casting. In the valid $N=139$ subset, all skill scores are continuous decimal numbers on a 1.0–5.0 scale.*

| Column Name | Raw Storage Dtype | Inferred Semantic Role | True Semantic Type | Unique Count (Valid) | Example Raw Values | Phase 1 Finding & Phase 2 Action |
|---|---|---|---|---|---|---|
| `id` | `object` | Employee Identifier | Categorical Key | 137 | `['2809', '2231']` | 32 trailing null rows. 2 duplicate IDs. Exclude from ML. |
| `big_data_skills` | `object` | Technical Competency | Continuous (1–5 Scale) | 28 | `['3.6', '4', '4.5']` | Decimal ratings. Phase 2: cast to `float64`. |
| `maths-stats_skills`| `object`| Technical Competency | Continuous (1–5 Scale) | 27 | `['4', '3.8', '5']` | Header has hyphen. Phase 2: rename to `maths_stats_skills`, cast to `float64`. |
| `coding_skills` | `object` | Technical Competency | Continuous (1–5 Scale) | 22 | `['4.5', '5', '3.3']` | Decimal ratings. Phase 2: cast to `float64`. |
| `ai_and_ml_skills` | `object` | Technical Competency | Continuous (1–5 Scale) | 22 | `['4.8', '4.4', '5']` | Ceiling effect (median 4.90). Phase 2: cast to `float64`. |
| `dashboard_and_storytelling_skills`| `object`| Technical Competency | Continuous (1–5 Scale) | 21 | `['5', '4.5', '3.7']` | Ceiling effect (median 5.00). Phase 2: cast to `float64`. |
| `salary_hike_high_or_low` | `object` | Career Progression Target | Binary Indicator {0, 1} | 2 | `['1', '0']` | Binary target (73 vs 66). Phase 2: cast to `int64`. |

---

### 2.4. Dataset 4: Senior Data Scientist Personality Traits (`SDS Personality Traits.xlsx`)

| Column Name (Raw) | Raw Storage Dtype | Inferred Semantic Role | True Semantic Type | Unique Count | Example Raw Values | Phase 1 Finding & Phase 2 Action |
|---|---|---|---|---|---|---|
| `'id'` | `object` | Subject Identifier | Categorical Key | 152 | `['8120', '8951']` | 9 duplicate IDs. Exclude from modeling. |
| `'neuroticism'` | `object` | Big Five Dimension | Continuous (17–68 Scale) | 39 | `['33', '50', '38']` | Raw psychometric score. Phase 2: cast to `float64`. |
| `' extraversion'` | `object` | Big Five Dimension | Continuous (17–68 Scale) | 43 | `['34', '45', '55']` | **Leading whitespace** in header. Phase 2: sanitize name & cast to `float64`. |
| `'openness_to_experience'`| `object`| Big Five Dimension | Continuous (18–65 Scale) | 40 | `['39', '44', '32']` | Raw psychometric score. Phase 2: cast to `float64`. |
| `'agreeableness'` | `object` | Big Five Dimension | Continuous (17–68 Scale) | 42 | `['45', '39', '51']` | Raw psychometric score. Phase 2: cast to `float64`. |
| `'conscientiousness'` | `object`| Big Five Dimension | Continuous (18–66 Scale) | 43 | `['51', '39', '49']` | Raw psychometric score. Phase 2: cast to `float64`. |
| `'success_ classification_ high_low'`| `object`| Consulting Success Target | Binary Indicator {0, 1} | 2 | `['1', '0']` | **Internal whitespace** in header. Phase 2: sanitize name & cast to `int64`. |
