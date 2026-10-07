# Feature Engineering & Processed Data Dictionary

**Project**: InsightPath — SAS CU Hackathon Round 2 Analytics  
**Document**: `docs/phase2/FEATURE_METADATA.md`  
**Phase**: Phase 2 — Data Cleaning & Transformation  
**Governing Standard**: Comprehensive Feature Governance & Auditability  

---

## 1. Overview of Processed Analytical Datasets

Phase 2 generates 4 clean interim files in `data/interim/` and 5 analytical production files in `data/processed/`:

| Dataset Identifier | Physical Path | Row Count ($N$) | Column Count ($P$) | Primary Analytical Purpose |
| :--- | :--- | :---: | :---: | :--- |
| **`jds_processed`** | `data/processed/jds_processed.csv` | 139 | 7 | Junior Data Scientist Skill Modeling (Baseline) |
| **`jds_sensitivity`** | `data/processed/jds_sensitivity_3291_removed.csv` | 137 | 7 | JDS Sensitivity Benchmark (ID 3291 Excluded) |
| **`sds_processed`** | `data/processed/sds_processed.csv` | 161 | 7 | Senior Data Scientist Psychometric Modeling |
| **`data_science_jobs_processed`** | `data/processed/data_science_jobs_processed.csv` | 1,602 | 14 | Compensation Spread & Hiring Volume Analytics |
| **`analytics_jobs_processed`** | `data/processed/analytics_jobs_processed.csv` | 15,841 | 72 | Skill Demand, Location, & Wage Bracket Analytics |

---

## 2. Dataset 1: Junior Data Scientist Skill Traits (`jds_processed.csv`)

### Population & Scope
- **Rows**: 139 (Filtered from 171 raw rows by eliminating 32 trailing Excel blanks; zero populated rows dropped).
- **Columns**: 7 (All non-null).

| Variable Name | Raw Source Column | Data Type | Physical Range / Scale | Missing Count | Modeling Role | Description & Derivation |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| `id` | `id` | `int64` | $[3111, 3362]$ | 0 | **Excluded** | Unique candidate identifier. Preserved for linkage; excluded from predictive models. |
| `big_data_skills` | `big_data_skills` | `float64` | $[1.0, 5.0]$ | 0 | Continuous Feature | Candidate proficiency rating in Big Data technologies (Hadoop, Spark, Distributed Systems). |
| `maths_stats_skills` | `maths-stats_skills` | `float64` | $[1.0, 5.0]$ | 0 | Continuous Feature | Proficiency rating in Mathematics & Statistics. Renamed from hyphenated header. |
| `coding_skills` | `coding_skills` | `float64` | $[1.0, 5.0]$ | 0 | Continuous Feature | Proficiency rating in Programming & Software Development (Python, R, Algorithms). |
| `ai_and_ml_skills` | `ai_and_ml_skills` | `float64` | $[1.0, 5.0]$ | 0 | Continuous Feature | Proficiency rating in Machine Learning, Deep Learning, and AI methodologies. |
| `dashboard_and_storytelling_skills` | `dashboard_and_storytelling_skills` | `float64` | $[1.0, 5.0]$ | 0 | Continuous Feature | Proficiency rating in BI dashboards, Data Visualization, and Executive Communication. |
| `salary_hike_high_or_low` | `salary_hike_high_or_low` | `int64` | $\{0, 1\}$ | 0 | **Target Variable** | Binary career advancement indicator: `1` = High Salary Hike ($n=73$), `0` = Low Salary Hike ($n=66$). |

---

## 3. Dataset 2: Senior Data Scientist Personality Traits (`sds_processed.csv`)

### Population & Scope
- **Rows**: 161 (100% of raw records preserved; 9 duplicated subject IDs retained for observational validity).
- **Columns**: 7 (All non-null).

| Variable Name | Raw Source Column | Data Type | Physical Range / Scale | Missing Count | Modeling Role | Description & Derivation |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| `id` | `id` | `int64` | $[3111, 3362]$ | 0 | **Excluded** | Candidate identifier. Grouping key for `GroupKFold` cross-validation; excluded from modeling. |
| `neuroticism` | `neuroticism` | `float64` | $[17.0, 68.0]$ | 0 | Continuous Feature | Big Five Neuroticism psychometric score. Measured on raw survey scale. |
| `extraversion` | ` extraversion` | `float64` | $[17.0, 68.0]$ | 0 | Continuous Feature | Big Five Extraversion psychometric score. Sanitized leading whitespace. |
| `openness_to_experience` | `openness_to_experience` | `float64` | $[17.0, 68.0]$ | 0 | Continuous Feature | Big Five Openness to Experience psychometric score. Raw survey scale. |
| `agreeableness` | `agreeableness` | `float64` | $[17.0, 68.0]$ | 0 | Continuous Feature | Big Five Agreeableness psychometric score. Raw survey scale. |
| `conscientiousness` | `conscientiousness` | `float64` | $[17.0, 68.0]$ | 0 | Continuous Feature | Big Five Conscientiousness psychometric score. Raw survey scale. |
| `success_classification_high_low` | `success_ classification_ high_low` | `int64` | $\{0, 1\}$ | 0 | **Target Variable** | Senior DS leadership outcome: `1` = High Success ($n=85$), `0` = Low Success ($n=76$). |

---

## 4. Dataset 3: Data Science Jobs (`data_science_jobs_processed.csv`)

### Population & Scope
- **Rows**: 1,602 (100% preserved; no outliers pruned).
- **Columns**: 14 (8 raw attributes preserved + 6 derived numeric variables).

| Variable Name | Raw / Derived | Data Type | Range / Domain | Missing | Modeling Role | Derivation / Analytical Definition |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| `reference_no` | Raw | `int64` | $[1011, 2612]$ | 0 | **Excluded** | Arbitrary sequential identifier. Excluded from models. |
| `company_name` | Cleaned Raw | `object` | 1,029 unique | 0 | Categorical | Employer name. Whitespace trimmed (`.str.strip()`). |
| `job_title` | Raw | `object` | 10 unique titles | 0 | Categorical | Standardized role title (e.g., Data Scientist, Data Engineer). |
| `min_experience` | Raw | `int64` | $[1, 10]$ years | 0 | Continuous | Minimum professional experience required in years. |
| `avg_salary` | Raw | `object` | Text with `'L'` | 0 | Raw Backup | Preserved verbatim raw string (e.g. `'10.5L'`). |
| `min_salary` | Raw | `object` | Text with `'L'` | 0 | Raw Backup | Preserved verbatim raw string. |
| `max_salary` | Raw | `object` | Text with `'L'` | 0 | Raw Backup | Preserved verbatim raw string. |
| `num_of_jobs` | Raw | `int64` | $[1, 82]$ jobs | 0 | Count | Number of open positions posted. Extreme right skew. |
| `min_salary_lakh` | Derived | `float64` | $[1.5, 30.0]$ | 0 | Continuous | Parsed numeric minimum salary in Lakhs INR. |
| `avg_salary_lakh` | Derived | `float64` | $[2.5, 45.0]$ | 0 | Continuous | Parsed numeric average salary in Lakhs INR. |
| `max_salary_lakh` | Derived | `float64` | $[3.5, 60.0]$ | 0 | Continuous | Parsed numeric maximum salary in Lakhs INR. |
| `salary_spread_lakh` | Derived | `float64` | $[0.0, 30.0]$ | 0 | Continuous | Absolute salary bargaining spread: $\text{max} - \text{min}$. |
| `salary_spread_ratio` | Derived | `float64` | $[0.0, 2.5]$ | 0 | Continuous | Relative salary flexibility: $(\text{max} - \text{min}) / \text{avg}$. |
| `log10_num_of_jobs` | Derived | `float64` | $[0.30, 1.92]$ | 0 | Continuous | $\log_{10}(1 + \text{num\_of\_jobs})$ for skew normalization. |

---

## 5. Dataset 4: Analytics Jobs (`analytics_jobs_processed.csv`)

### Population & Scope
- **Rows**: 15,841 (100% preserved).
- **Columns**: 72 (8 raw + 14 core derived + 50 binary skill indicators).

### Core Attributes & Feature Engineering
| Variable Name | Raw / Derived | Data Type | Range / Domain | Missing | Modeling Role | Description & Transformation |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| `s_no` | Raw | `int64` | $[1, 15841]$ | 0 | **Excluded** | Sequence row ID. Excluded from models. |
| `experience` | Raw | `object` | 128 intervals | 0 | Raw Backup | Verbatim experience string (e.g. `'5-10 yrs'`). |
| `job_description` | Raw | `object` | Text snippets | 3,508 | Raw Backup | Verbatim short text teaser snippet. |
| `job_desig` | Raw | `object` | 10,097 titles | 0 | Raw Backup | Verbatim raw job designation. |
| `job_type` | Raw | `object` | Text | 12,011 | Raw Backup | Verbatim job type string. |
| `key_skills` | Raw | `object` | Text | 1 | Raw Backup | Verbatim comma/pipe separated skill string. |
| `location` | Raw | `object` | 1,355 strings | 35 | Raw Backup | Verbatim location string. |
| `salary` | Raw | `object` | 6 brackets | 0 | Raw Backup | Verbatim discrete salary bracket text. |
| `min_experience` | Derived | `float64` | $[0.0, 25.0]$ | 0 | Continuous | Lower bound of experience interval in years. |
| `max_experience` | Derived | `float64` | $[0.0, 30.0]$ | 0 | Continuous | Upper bound of experience interval in years. |
| `midpoint_experience` | Derived | `float64` | $[0.0, 27.5]$ | 0 | Continuous | Interval midpoint: $(\text{min} + \text{max}) / 2$. |
| `salary_rank` | Derived | `int64` | $[1, 6]$ | 0 | Ordinal | Monotonic salary grade: 1='0to3', 2='3to6', 3='6to10', 4='10to15', 5='15to25', 6='25to50'. |
| `salary_midpoint` | Derived | `float64` | $[1.5, 37.5]$ | 0 | Continuous | Interval midpoint approximation in Lakhs INR: 1.5, 4.5, 8.0, 12.5, 20.0, 37.5. |
| `is_high_salary` | Derived | `int64` | $\{0, 1\}$ | 0 | Binary Target | Upper bracket indicator: `1` if $\ge 15\text{L}$ (ranks 5 and 6), `0` otherwise. |
| `job_type_clean` | Derived | `object` | 2 categories | 0 | Descriptive Only | 'Analytics' ($n=3,830$) vs 'Unspecified' ($n=12,011$). Excluded from models. |
| `job_description_clean` | Derived | `object` | String | 0 | Text | Whitespace trimmed; missing imputed with `""`. |
| `job_description_char_count` | Derived | `int64` | $[0, 109]$ | 0 | Metadata | Character count of snippet (median = 88 chars). |
| `job_description_word_count` | Derived | `int64` | $[0, 25]$ | 0 | Metadata | Word count of snippet (median = 15 words). |
| `key_skills_clean` | Derived | `object` | String | 0 | Text | Missing imputed as 'Not Specified'; trimmed. |
| `location_clean` | Derived | `object` | String | 0 | Intermediate | Lowercased, stripped, punctuation cleaned. |
| `location_cluster` | Derived | `object` | 7 clusters | 0 | Categorical | Bengaluru, NCR, Mumbai, Pune, Hyderabad, Chennai, Other/Tier-2. |
| `job_role_family` | Derived | `object` | 6 families | 0 | Categorical | Data Scientist, Data Analyst, Business Analyst, Data Engineer, BI Developer, Non-Analytics/Other. |

### Top-50 Multi-Hot Skill Indicators (`skill_*`)
Columns 23 to 72 contain deterministic binary indicators ($0$ = absent, $1$ = present) derived from the empirical vocabulary profile:
`skill_sql`, `skill_analytics`, `skill_python`, `skill_finance`, `skill_java`, `skill_r`, `skill_excel`, `skill_machine_learning`, `skill_business_analysis`, `skill_tableau`, `skill_accounting`, `skill_data_analysis`, `skill_banking`, `skill_communication_skills`, `skill_sas`, `skill_c`, `skill_oracle`, `skill_javascript`, `skill_management`, `skill_spark`, `skill_power_bi`, `skill_aws`, `skill_data_mining`, `skill_big_data`, `skill_consulting`, `skill_hadoop`, `skill_scala`, `skill_reporting`, `skill_hive`, `skill_data_science`, `skill_financial_analysis`, `skill_auditing`, `skill_csharp`, `skill_cpp`, `skill_taxation`, `skill_linux`, `skill_deep_learning`, `skill_qlikview`, `skill_git`, `skill_nlp`, `skill_etl`, `skill_nosql`, `skill_html`, `skill_agile`, `skill_dotnet`, `skill_tableau_software`, `skill_market_research`, `skill_sap`, `skill_vba`, `skill_risk_management`.
