# Comprehensive Data Dictionary (Phase 1)

## 1. Overview and Standards

This data dictionary provides the complete metadata specification for all 30 attributes across the four datasets analyzed in the SAS CU Hackathon analytics project. 

In strict adherence to Phase 1 standards:
* Variable definitions reflect empirical properties observed during audit.
* Known data-quality flaws and required Phase 2 transformations are explicitly cataloged.

---

## 2. Dataset 1: Data Science Jobs (`DataScience Jobs.csv`)

### Population: Enterprise Employer Job Requisitions ($N = 1,602$)

| Column Name | Current Dtype | Semantic Role | Description | Missing (Count / %) | Unique Count | Example Values | Observed Range | Known Data Quality Issue | Phase 2 Action Required |
|---|---|---|---|---|---|---|---|---|---|
| `reference_no` | `int64` | Identifier / Requisition Key | Unique requisition identifier assigned by employer or recruiting portal. | 0 (0.0%) | 1,460 | `7834, 7862, 5925` | 1012 to 8998 | Non-unique (142 duplicates across different companies). | Exclude from modeling feature matrices; retain as row identifier. |
| `company_name` | `object` | Hiring Organization | Name of the hiring corporate entity. | 0 (0.0%) | 642 | `'TCS', 'Accenture', 'IBM'` | N/A | Minor whitespace variations in long tail. | Standardize via `.str.strip()`. |
| `job_title` | `object` | Role Classification | Standardized title of the advertised data role. | 0 (0.0%) | 10 | `'Data Scientist', 'Data Analyst'` | Exactly 10 titles | None. Structured taxonomy. | Retain as primary grouping factor for salary/experience benchmarks. |
| `min_experience`| `int64` | Experience Barrier | Minimum required years of professional experience. | 0 (0.0%) | 16 | `2, 3, 5, 0` | 0 to 21 years | Right-skewed tail (39 values $> 8.5$ years). | Retain continuous; bin into experience tiers (`[0-2]`, `[3-5]`, etc.). |
| `avg_salary` | `object` | Mean Compensation | Advertised average annual compensation in Lakhs INR. | 0 (0.0%) | 158 | `'7.8L', '12.8L', '13.4L'` | 1.4L to 82.0L | Stored as string with `'L'` suffix. | Parse string: strip `'L'`, cast to `float64`. |
| `min_salary` | `object` | Minimum Compensation | Lower bound of advertised annual compensation in Lakhs INR. | 0 (0.0%) | 124 | `'4.5L', '5.8L', '5.3L'` | 0.2L to 55.0L | Stored as string with `'L'` suffix. | Parse string: strip `'L'`, cast to `float64`. |
| `max_salary` | `object` | Maximum Compensation | Upper bound of advertised annual compensation in Lakhs INR. | 0 (0.0%) | 164 | `'16.0L', '23.0L', '25.0L'` | 2.0L to 102.0L | Stored as string with `'L'` suffix. | Parse string: strip `'L'`, cast to `float64`; derive `salary_spread`. |
| `num_of_jobs` | `int64` | Requisition Volume | Total number of vacancies advertised in the requisition. | 0 (0.0%) | 134 | `841, 501, 394` | 3 to 4,200 | Severe right skewness (164 outliers; max 4,200). | Retain raw; compute $\log_{10}(\text{num\_of\_jobs})$ for sensitivity. |

---

## 3. Dataset 2: Analytics Jobs (`Analytics Jobs.csv`)

### Population: Individual Analytics Job Postings ($N = 15,841$)

| Column Name | Current Dtype | Semantic Role | Description | Missing (Count / %) | Unique Count | Example Values | Observed Range | Known Data Quality Issue | Phase 2 Action Required |
|---|---|---|---|---|---|---|---|---|---|
| `s_no` | `int64` | Serial Index | Arbitrary sequential record index from scraper. | 0 (0.0%) | 15,841 | `1, 2, 3` | 1 to 15841 | None. Perfect sequence. | Retain as index; exclude from feature matrices. |
| `experience` | `object` | Experience Range | Required experience interval string. | 0 (0.0%) | 128 | `'6-10 yrs', '2-5 yrs'` | 128 formats | Unstructured string intervals. | Regex extract `min_exp`, `max_exp`, `midpoint_exp`. |
| `job_description`| `object`| Job Text Snippet | Short promotional teaser snippet for the job. | 3,508 (22.1%)| 7,859 | `'Looking for data...'` | 13 to 109 chars | Truncated snippet text; 22.1% missing. | Impute `""`; use `key_skills` as primary skill source. |
| `job_desig` | `object` | Job Designation | Free-text job title as posted by employer. | 0 (0.0%) | 10,097 | `'Business Analyst'` | N/A | Extreme cardinality; domain noise. | Keyword dictionary mapping to 5 core analytical role families. |
| `job_type` | `object` | Job Family Flag | Category flag (predominantly 'Analytics'). | 12,011 (75.8%)| 5 | `'Analytics', 'analytics'`| 5 casing variants| 75.8% missing; 5 casing variants of 1 word. | Standardize casing; exclude from ML models due to $>75\%$ nulls. |
| `key_skills` | `object` | Skill Inventory | Comma-delimited list of required candidate skills. | 1 (0.006%) | 11,155 | `'IT Skills, Python, SQL'` | 1 to 12 tokens | Inconsistent casing across tokens; 1 null. | Tokenize, fold casing, and extract multi-hot indicators. |
| `location` | `object` | Employment Location| Advertised hiring office city or cities. | 0 (0.0%) | 1,355 | `'Bengaluru', 'Mumbai'` | N/A | Multi-city comma-separated strings. | Parse into primary metro hub indicators (Bengaluru, NCR, etc.). |
| `salary` | `object` | Salary Bracket | Discrete annual salary bracket in Lakhs INR. | 0 (0.0%) | 6 | `'10to15', '15to25'` | 6 discrete bands | Discrete categorical intervals. | Create ordinal factor ($1 \dots 6$) and interval midpoints. |

---

## 4. Dataset 3: Junior Data Scientist Skill Traits (`JDS Skill Traits.xlsx`)

### Population: Junior Data Scientists ($N = 139$ Valid Cases; 32 Blank Trailing Rows)

| Column Name | Current Dtype | Semantic Role | Description | Missing (Count / %) | Unique Count | Example Values | Observed Range | Known Data Quality Issue | Phase 2 Action Required |
|---|---|---|---|---|---|---|---|---|---|
| `id` | `object` | Employee Identifier | Anonymized junior employee evaluation ID. | 32 (18.7%) | 137 | `'2809', '2231'` | 2007 to 4000 | 32 trailing blank rows; 2 duplicate IDs (ID 3291 has conflicting targets). | Strip blank rows; test model sensitivity with ID 3291 excluded. Drop ID from ML. |
| `big_data_skills` | `object` | Technical Competency | Evaluation rating in Big Data technologies (1–5 scale). | 32 (18.7%) | 28 | `'3.6', '4', '4.5'` | 2.30 to 5.00 | None in valid sample. | Strip blank rows; cast to `float64`. |
| `maths-stats_skills`| `object`| Technical Competency | Evaluation rating in Mathematics & Statistics (1–5 scale). | 32 (18.7%) | 27 | `'4', '3.8', '5'` | 2.20 to 5.00 | Hyphen in header name. | Rename to `maths_stats_skills`; cast to `float64`. |
| `coding_skills` | `object` | Technical Competency | Evaluation rating in Programming & Software Coding (1–5 scale). | 32 (18.7%) | 22 | `'4.5', '5', '3.3'` | 2.20 to 5.00 | 44.6% ceiling compression at 5.0. | Strip blank rows; cast to `float64`. |
| `ai_and_ml_skills` | `object` | Technical Competency | Evaluation rating in AI & Machine Learning (1–5 scale). | 32 (18.7%) | 22 | `'4.8', '4.4', '5'` | 2.20 to 5.00 | 48.9% ceiling compression; 18 Tukey low outliers. | Strip blank rows; cast to `float64`. |
| `dashboard_and_storytelling_skills`| `object`| Technical Competency | Evaluation rating in BI Dashboards & Storytelling (1–5 scale). | 32 (18.7%) | 21 | `'5', '4.5', '3.7'` | 2.30 to 5.00 | 58.3% ceiling compression at 5.0 (median 5.00). | Strip blank rows; cast to `float64`. |
| `salary_hike_high_or_low` | `object` | Progression Target | Binary classification of salary hike increment: 1=High, 0=Low. | 32 (18.7%) | 2 | `'1', '0'` | Binary {0, 1} | Conflicting target label for duplicate ID 3291. | Cast to `int64`; test sensitivity with ID 3291 quarantined. |

---

## 5. Dataset 4: Senior Data Scientist Personality Traits (`SDS Personality Traits.xlsx`)

### Population: Senior Customer-Facing Data Scientists ($N = 161$)

| Column Name (Raw) | Current Dtype | Semantic Role | Description | Missing (Count / %) | Unique Count | Example Values | Observed Range | Known Data Quality Issue | Phase 2 Action Required |
|---|---|---|---|---|---|---|---|---|---|
| `'id'` | `object` | Subject Identifier | Anonymized senior consultant identifier. | 0 (0.0%) | 152 | `'8120', '8951'` | 8001 to 8979 | 9 duplicate IDs with differing trait scores and targets. | Treat rows as distinct evaluations; drop ID from modeling. |
| `'neuroticism'` | `object` | Big Five Dimension | Raw psychometric score for Neuroticism (Emotional Stability). | 0 (0.0%) | 39 | `'33', '50', '38'` | 17.0 to 68.0 | None. Raw psychometric scale. | Cast to `float64`; compute standardized Z-score in CV. |
| `' extraversion'` | `object` | Big Five Dimension | Raw psychometric score for Extraversion / Social Engagement. | 0 (0.0%) | 43 | `'34', '45', '55'` | 17.0 to 67.0 | Leading whitespace in column header. | Sanitize header to `extraversion`; cast to `float64`. |
| `'openness_to_experience'`| `object`| Big Five Dimension | Raw psychometric score for Openness to Experience / Intellect. | 0 (0.0%) | 40 | `'39', '44', '32'` | 18.0 to 65.0 | None. Raw psychometric scale. | Cast to `float64`; compute standardized Z-score in CV. |
| `'agreeableness'` | `object` | Big Five Dimension | Raw psychometric score for Agreeableness / Cooperation. | 0 (0.0%) | 42 | `'45', '39', '51'` | 17.0 to 68.0 | 5 low outliers (scores 17–20). | Cast to `float64`; retain all outliers. |
| `'conscientiousness'` | `object`| Big Five Dimension | Raw psychometric score for Conscientiousness / Diligence. | 0 (0.0%) | 43 | `'51', '39', '49'` | 18.0 to 66.0 | None. Wide dispersion (std = 13.2). | Cast to `float64`; compute standardized Z-score in CV. |
| `'success_ classification_ high_low'`| `object`| Consulting Target | Binary classification of client consulting success: 1=High, 0=Low. | 0 (0.0%) | 2 | `'1', '0'` | Binary {0, 1} | Internal whitespace in column header. | Sanitize header to `success_classification_high_low`; cast to `int64`. |
