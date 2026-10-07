# Phase 2 Data Cleaning & Transformation Requirements (Phase 1 Deliverable)

## 1. Executive Summary & Governance Rules

This document establishes the formal, prioritized work specification for **Phase 2 — Data Cleaning & Transformation**. 

Every required transformation is justified by empirical evidence gathered during the Phase 1 audit. In strict accordance with project architecture:
1. **Raw Data Invariance**: All Phase 2 cleaning scripts must read from `data/raw/` in read-only mode and output cleaned datasets to `data/interim/` and `data/processed/`.
2. **Reversibility**: Every transformation must be implemented programmatically in Python modules under `src/preprocessing/` and `src/features/`.
3. **Traceability**: All row filtering or quarantine operations must log before-and-after row counts ($\Delta N$).

---

## 2. Ordered Phase 2 Cleaning Action Specifications

### Requirement 1: JDS Trailing Blank Row Removal
* **Dataset**: `JDS Skill Traits.xlsx`
* **Target Columns**: All 7 columns (Rows 140–171)
* **Empirical Evidence**: Exactly 32 rows contain `None` / `NaN` across all columns simultaneously.
* **Recommended Treatment**: Execute `df_jds = df_jds.dropna(how='all')` during initial ingestion.
* **Reason**: These rows are Excel formatting artifacts; removing them isolates the true analytical sample ($N = 139$).
* **Risk If Untreated**: Skews sample size calculations, breaks numerical conversions, and corrupts target proportions.
* **Human Approval Required?**: **NO** (Technical artifact removal; 0 valid data lost).

---

### Requirement 2: SDS Header Whitespace Sanitization
* **Dataset**: `SDS Personality Traits.xlsx`
* **Target Columns**: `' extraversion'`, `'success_ classification_ high_low'`
* **Empirical Evidence**: Header 3 has leading space `\x20`; Header 7 has internal spaces.
* **Recommended Treatment**: Rename via `df_sds.columns = [c.strip().replace(' ', '_').lower() for c in df_sds.columns]`. Resulting columns: `extraversion`, `success_classification_high_low`.
* **Reason**: Standardizes column names into valid Python/SQL identifiers.
* **Risk If Untreated**: Generates `KeyError` exceptions in downstream analysis and visualization code.
* **Human Approval Required?**: **NO** (Standard syntax hygiene).

---

### Requirement 3: JDS Header Hyphen Standardization
* **Dataset**: `JDS Skill Traits.xlsx`
* **Target Column**: `maths-stats_skills`
* **Empirical Evidence**: Contains a hyphen `-`.
* **Recommended Treatment**: Rename to `maths_stats_skills`.
* **Reason**: Hyphens represent subtraction operators in Python and statsmodels formula APIs.
* **Risk If Untreated**: Formula parsing errors in logistic regression (`statsmodels.formula.api.logit`).
* **Human Approval Required?**: **NO** (Standard syntax hygiene).

---

### Requirement 4: JDS Duplicate ID 3291 Label Conflict Resolution
* **Dataset**: `JDS Skill Traits.xlsx`
* **Target Column**: `id = 3291` (Row 3 vs Row 29)
* **Empirical Evidence**: Row 3 has `target = 0`; Row 29 has `target = 1`, while possessing almost identical skill vectors (`[4.0, 4.0, 4.5, 4.7, 5.0]` vs `[4.2, 4.5, 4.0, 4.9, 5.0]`).
* **Recommended Treatment**: In Phase 2, prepare two analytical subsets:
  * Subset A: Baseline sample ($N = 139$) retaining both records as distinct observations.
  * Subset B: Quarantined sample ($N = 137$) excluding `id = 3291` to evaluate model sensitivity to label noise.
* **Reason**: Contradictory outcome labels for identical feature vectors introduce severe decision boundary confusion.
* **Risk If Untreated**: Artificially depresses classifier accuracy and introduces model instability.
* **Human Approval Required?**: **YES** (Approval required to adopt Subset B for primary ML modeling).

---

### Requirement 5: Data Science Jobs Currency Parsing & Spread Feature
* **Dataset**: `DataScience Jobs.csv`
* **Target Columns**: `avg_salary`, `min_salary`, `max_salary`
* **Empirical Evidence**: 1,602 rows formatted as text strings with `'L'` suffix (e.g. `'7.8L'`).
* **Recommended Treatment**: Strip `'L'` and whitespace; convert to `float64` (Lakhs INR). Derive `salary_spread = max_salary - min_salary` and `salary_spread_ratio = salary_spread / avg_salary`.
* **Reason**: Converts text into continuous mathematical variables for regression and ANOVA.
* **Risk If Untreated**: Mathematical analysis and salary modeling cannot execute.
* **Human Approval Required?**: **NO** (Standard data type correction).

---

### Requirement 6: Analytics Jobs Experience Interval Parsing
* **Dataset**: `Analytics Jobs.csv`
* **Target Column**: `experience`
* **Empirical Evidence**: 15,841 rows formatted as string intervals (e.g. `'6-10 yrs'`, `'2-5 yrs'`).
* **Recommended Treatment**: Apply regex `r'(\d+)\s*-\s*(\d+)'` to extract `min_experience` (lower integer), `max_experience` (upper integer), and `midpoint_experience = (min_exp + max_exp) / 2.0`.
* **Reason**: Creates numeric continuous experience metrics for elasticity and correlation modeling.
* **Risk If Untreated**: Inability to quantitatively evaluate experience requirements.
* **Human Approval Required?**: **NO** (Standard feature engineering).

---

### Requirement 7: Analytics Jobs Salary Bracket Transformation
* **Dataset**: `Analytics Jobs.csv`
* **Target Column**: `salary`
* **Empirical Evidence**: 15,841 rows stored as 6 discrete text brackets (`'0to3'`, `'3to6'`, `'6to10'`, `'10to15'`, `'15to25'`, `'25to50'`).
* **Recommended Treatment**:
  * Create ordered categorical factor `salary_rank` $\in \{1, 2, 3, 4, 5, 6\}$.
  * Assign numerical midpoint approximation `salary_midpoint` $\in [1.5, 4.5, 8.0, 12.5, 20.0, 37.5]$ Lakhs INR.
  * Create binary high-salary benchmark flag `is_high_salary = 1` if salary $\in \{\text{'15to25'}, \text{'25to50'}\}$, else $0$.
* **Reason**: Enables both non-parametric rank correlation and logistic odds ratio modeling.
* **Risk If Untreated**: Constrains salary analysis to purely nominal frequency tables.
* **Human Approval Required?**: **NO** (Standard domain transformation).

---

### Requirement 8: Analytics Jobs `job_type` Missingness & Normalization
* **Dataset**: `Analytics Jobs.csv`
* **Target Column**: `job_type`
* **Empirical Evidence**: 12,011 missing values ($75.82\%$); 3,830 populated entries represent 5 casing variants of "Analytics".
* **Recommended Treatment**: Standardize populated entries to `'Analytics'` and impute missing records as `'Unspecified'`. **Exclude from all predictive modeling**.
* **Reason**: A variable with $>75\%$ missingness and zero variance across populated records provides no predictive discrimination.
* **Risk If Untreated**: Biases models or forces dropping 76% of valid job postings.
* **Human Approval Required?**: **YES** (Approval to exclude `job_type` from statistical modeling).

---

### Requirement 9: Analytics Jobs `job_description` Imputation
* **Dataset**: `Analytics Jobs.csv`
* **Target Column**: `job_description`
* **Empirical Evidence**: 3,508 missing values ($22.14\%$); populated entries are short teaser snippets ($\le 109$ chars).
* **Recommended Treatment**: Impute missing values with empty string `""`. Establish `key_skills` as primary skill source.
* **Reason**: Prevents vectorization errors in text mining scripts without dropping valid postings.
* **Risk If Untreated**: Dropping 3,508 records loses $22\%$ of the dataset.
* **Human Approval Required?**: **NO** (Standard text imputation practice).

---

### Requirement 10: Analytics Jobs `key_skills` Tokenization & Multi-Hot Encoding
* **Dataset**: `Analytics Jobs.csv`
* **Target Column**: `key_skills`
* **Empirical Evidence**: 15,840 populated rows of comma-delimited skills; 1 missing record.
* **Recommended Treatment**: Impute the 1 missing record as `"Not Specified"`. Build a string tokenizer to split on commas, strip whitespace, fold casing to lowercase, and extract binary multi-hot indicator features for the top 50 in-demand skills (Python, SQL, R, Tableau, PowerBI, Spark, AWS, Machine Learning, etc.).
* **Reason**: Enables granular skill frequency ranking, co-occurrence network analysis, and salary association tests.
* **Risk If Untreated**: Skills remain locked in unsearchable comma-separated text strings.
* **Human Approval Required?**: **NO** (Core analytical methodology).

---

### Requirement 11: Analytics Jobs Location Clustering
* **Dataset**: `Analytics Jobs.csv`
* **Target Column**: `location`
* **Empirical Evidence**: 1,355 unique strings with frequent multi-city entries (`'Bengaluru, Chennai'`).
* **Recommended Treatment**: Parse primary metro indicators into 7 standardized macro clusters: Bengaluru, Mumbai, NCR (Delhi/Gurgaon/Noida), Pune, Hyderabad, Chennai, and Other/Tier-2.
* **Reason**: Reduces extreme cardinality while preserving core geographic hiring patterns.
* **Risk If Untreated**: Geographic analysis fragmented across 1,355 sparse categories.
* **Human Approval Required?**: **NO** (Standard categorical aggregation).

---

### Requirement 12: Analytics Jobs Designation Role Family Grouping
* **Dataset**: `Analytics Jobs.csv`
* **Target Column**: `job_desig`
* **Empirical Evidence**: 10,097 unique free-text strings with significant non-analytics scraping noise.
* **Recommended Treatment**: Apply regex dictionary mapping to classify postings into: Data Scientist, Data Analyst, Business Analyst, Data Engineer, BI Developer, and Non-Analytics/Other.
* **Reason**: Harmonizes role titles with the standardized taxonomy of `DataScience Jobs.csv`.
* **Risk If Untreated**: Inability to compare role trends between macro and micro datasets.
* **Human Approval Required?**: **NO** (Standard text classification).

---

### Requirement 13: Data Science Jobs Extreme Skewness Management
* **Dataset**: `DataScience Jobs.csv`
* **Target Column**: `num_of_jobs`
* **Empirical Evidence**: Positive skewness of $+12.83$ with 164 high outliers peaking at 4,200 openings.
* **Recommended Treatment**: Retain all 1,602 records. Engineer $\log_{10}(\text{num\_of\_jobs})$ feature to stabilize variance in regression models.
* **Reason**: Deleting records would discard genuine enterprise hiring volume signals.
* **Risk If Untreated**: Outliers exert extreme leverage on OLS regression slopes.
* **Human Approval Required?**: **NO** (Standard econometric transformation).

---

### Requirement 14: Identifier Quarantine & Leakage Safeguard
* **Dataset**: All 4 Datasets
* **Target Columns**: `reference_no`, `s_no`, `id`
* **Empirical Evidence**: Identifier multiplicity, non-uniqueness, and cross-dataset key collisions.
* **Recommended Treatment**: Strictly exclude identifier columns from all predictive feature matrices. Retain row indices for audit logging only.
* **Reason**: Identifiers carry no domain signal and create spurious overfitting.
* **Risk If Untreated**: Catastrophic data leakage and invalid models.
* **Human Approval Required?**: **NO** (Core machine learning principle).
