# Phase 1 Execution Plan & Technical Handoff (Phase 0 Deliverable)

## 1. Phase 1 Objective & Scope

* **Phase Title**: **Phase 1 — Data Audit, Profiling & Comprehensive Quality Assessment**
* **Primary Objective**: Perform the exhaustive, programmatic data audit and generate formal data quality artifacts for all four datasets. Phase 1 establishes the benchmark empirical truth before any data cleaning transformations or modeling pipelines are executed.
* **Non-Goals / Scope Boundaries**:
  * Do NOT perform destructive data cleaning or row deletions in place.
  * Do NOT train machine learning models.
  * Do NOT calculate final inferential statistics or hypothesis conclusions.
  * Focus exclusively on audit, profiling, structural verification, and generating baseline reports.

---

## 2. Phase 1 Work Breakdown Structure (WBS)

```
[TASK 1.1: Environment & File Verification]
                   │
                   ▼
[TASK 1.2: Programmatic Data Profiling Engine]
                   │
                   ▼
[TASK 1.3: Deep Column-Level Profiling (4 Datasets)]
  ├─ 1.3A: DataScience Jobs.csv (1,602 rows)
  ├─ 1.3B: Analytics Jobs.csv (15,841 rows)
  ├─ 1.3C: JDS Skill Traits.xlsx (171 rows / 139 valid)
  └─ 1.3D: SDS Personality Traits.xlsx (161 rows)
                   │
                   ▼
[TASK 1.4: Cross-Dataset Key & Collision Audit]
                   │
                   ▼
[TASK 1.5: Data Quality Deliverables & Artifact Generation]
  ├─ Deliverable A: docs/phase1/DATA_QUALITY_REPORT.md
  ├─ Deliverable B: docs/phase1/DATA_DICTIONARY.md
  └─ Deliverable C: notebooks/01_data_audit/01_initial_data_audit.ipynb
```

---

## 3. Detailed Specifications by Task

### Task 1.1: Environment & Ingestion Setup
* Set up reproducible data loading scripts in `src/data/loader.py` that read raw files from `data/raw/` in read-only mode.
* Implement robust XML/openpyxl Excel parsing to handle the trailing blank rows in `JDS Skill Traits.xlsx` without crashing.

### Task 1.2: Programmatic Data Profiling Engine
* Develop an automated profiling function in `src/utils/profiler.py` that computes for every column across all datasets:
  * Inferred vs storage data type
  * Total count, non-null count, null count, null percentage
  * Distinct / unique value count and uniqueness ratio
  * Leading/trailing whitespace presence
  * Casing inconsistencies (e.g. mixed upper/lower case in categorical fields)
  * Five-number summary (Min, Q1, Median, Q3, Max), Mean, Std, Skewness, Kurtosis for numeric fields
  * Top-5 most frequent values with absolute counts and percentages for categorical fields.

### Task 1.3: Detailed Dataset Profiling Protocols

#### 1.3A: Profiling `DataScience Jobs.csv` ($N = 1,602$)
* Profile `reference_no`: Document exact distribution of the 142 duplicate values; confirm whether duplicate reference numbers belong to identical or different companies.
* Profile `company_name`: Compute exact cardinality (642 companies), identify top-20 employers, and screen for spelling variations (e.g. "TCS" vs "Tata Consultancy Services").
* Profile `job_title`: Confirm exact distribution of the 10 standardized titles.
* Profile `min_experience`: Compute distribution, IQR, and identify values $> 10$ years.
* Profile `avg_salary`, `min_salary`, `max_salary`: Parse string `'L'` suffix; inspect distribution in Lakhs; compute `salary_spread` (`max - min`) and flag any instances where `min_salary > max_salary` or `avg_salary` falls outside `[min_salary, max_salary]`.
* Profile `num_of_jobs`: Audit positive skewness, compute percentiles (50th, 90th, 99th), and assess impact of bulk hiring records ($> 1,000$ openings).

#### 1.3B: Profiling `Analytics Jobs.csv` ($N = 15,841$)
* Profile `s_no`: Verify strict monotonicity and uniqueness across all 15,841 rows.
* Profile `experience`: Profile all 128 distinct string patterns; build regex extraction validator for `min_exp` and `max_exp`; identify irregular formats (e.g. `'0 yrs'`, `'Fresher'`, `'15+ yrs'`).
* Profile `job_description`: Document exact missingness (3,508 nulls; 22.14%); compute character length and word count distributions for populated records.
* Profile `job_desig`: Audit the 10,097 unique free-text strings; design keyword filtering dictionary to classify into core analytics role families vs non-analytics noise.
* Profile `job_type`: Formally document 75.82% missingness (12,011 nulls); catalog the 5 casing variants of "Analytics" (`'Analytics'`, `'analytics'`, `'ANALYTICS'`, `'analytic'`, `'Analytic'`).
* Profile `key_skills`: Profile delimiter patterns (comma vs semicolon vs pipe); tokenize all skill strings; generate full frequency rank of top-100 skills; audit the single missing record.
* Profile `location`: Audit 1,355 unique strings; isolate multi-city entries; design canonical mapping to primary metro hubs (Bengaluru, Mumbai, Delhi-NCR, Pune, Hyderabad, Chennai).
* Profile `salary`: Document exact counts across the 6 discrete categorical bands (`0to3`, `3to6`, `6to10`, `10to15`, `15to25`, `25to50`); verify 0 missing values.

#### 1.3C: Profiling `JDS Skill Traits.xlsx` ($N = 171$ sheet rows, 139 valid records)
* Blank Row Isolation: Formally confirm rows 140–171 are 100% null across all 7 columns; log removal protocol.
* Profile `id`: Audit the 2 duplicate IDs (`id` 2223, 3291); inspect whether `id` 3291 (which has targets 0 and 1) has identical or distinct skill ratings.
* Profile 5 Skill Dimensions: Compute descriptive statistics (Mean, Median, Std, Skewness, Min, Max); inspect ceiling compression at 5.0 (especially `ai_and_ml_skills` and `dashboard_and_storytelling_skills`); run Shapiro-Wilk normality tests.
* Profile `salary_hike_high_or_low`: Confirm exact class frequencies (73 vs 66); verify binary encoding integrity $\in \{0, 1\}$.

#### 1.3D: Profiling `SDS Personality Traits.xlsx` ($N = 161$ records)
* Header Sanitization: Document leading space in `' extraversion'` and internal spaces in `'success_ classification_ high_low'`.
* Profile `id`: Catalog all 9 duplicate ID occurrences; confirm trait variances across identical IDs.
* Profile Big Five Personality Dimensions: Verify score boundaries ($[17, 68]$); compute distribution metrics; run Shapiro-Wilk tests and screen for outliers ($> 3 \sigma$).
* Profile `success_classification_high_low`: Confirm exact class frequencies (85 vs 76); verify binary encoding integrity $\in \{0, 1\}$.

---

## 4. Phase 1 Required Output Deliverables

Upon completion of Phase 1, the following deliverables must be generated and committed:

1. **`docs/phase1/DATA_QUALITY_REPORT.md`**: Comprehensive markdown report documenting all empirical anomalies, missingness tables, duplicate key breakdowns, and approved cleaning rules.
2. **`docs/phase1/DATA_DICTIONARY.md`**: Complete metadata catalog defining every variable, business meaning, raw type, parsed type, valid range, and observed statistics across all 4 datasets.
3. **`notebooks/01_data_audit/01_initial_data_audit.ipynb`**: Fully executed, reproducible Jupyter notebook containing all profiling code, diagnostic tables, and visual verification plots.
4. **Handoff Decision Gate**: Formal sign-off on cleaning rules before triggering Phase 2 (Data Cleaning & Preparation).
