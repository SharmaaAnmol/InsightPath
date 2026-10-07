# Detailed Dataset Audit: Analytics Jobs (Phase 1)

## 1. Executive Summary

This document establishes the dedicated column-by-column audit for `Analytics Jobs.csv` ($N = 15,841$). In strict compliance with Phase 1 Rule 1 and Rule 2, **no raw values have been modified, imputed, or cleaned**.

The dataset represents granular individual job postings across India's technology ecosystem. It features high dimensionality, substantial missingness in `job_type` (75.82%), text snippets in `job_description` (22.14% missing), discrete categorical salary bands, and high free-text variability in designations and locations.

---

## 2. Comprehensive Attribute Audit

### 2.1. `s_no` (Serial Posting Index)
* **Raw Type**: `int64`
* **Range**: $1$ to $15,841$
* **Completeness**: 15,841 non-null (100.0%)
* **Uniqueness**: 15,841 unique values (uniqueness ratio = $1.0000$)
* **Data Quality Finding**: Perfect sequential index with zero missing values or duplicate rows.
* **Phase 2 Directive**: Drop from analytical feature sets; retain purely as row index.

### 2.2. `experience` (Experience Requirement Interval)
* **Raw Type**: `object` (string)
* **Completeness**: 15,841 non-null (100.0%)
* **Cardinality**: 128 distinct interval formats
* **Top Observed Formats**:
  * `'5-10 yrs'`: 1,010 ($6.38\%$)
  * `'2-5 yrs'`: 964 ($6.09\%$)
  * `'3-8 yrs'`: 750 ($4.73\%$)
  * `'2-7 yrs'`: 665 ($4.20\%$)
  * `'3-5 yrs'`: 545 ($3.44\%$)
  * `'4-9 yrs'`: 527 ($3.33\%$)
* **Data Quality Finding**: All 15,841 records follow hyphenated year patterns (`'X-Y yrs'`).
* **Phase 2 Directive**: Apply regex `r'(\d+)\s*-\s*(\d+)'` to derive `min_experience`, `max_experience`, and `midpoint_experience`.

### 2.3. `job_description` (Unstructured Posting Text)
* **Raw Type**: `object` (text)
* **Completeness**: 12,333 non-null; **3,508 missing** ($22.14\%$)
* **Text Length Distribution (Populated Sample)**:
  * Character Length: Min = 13, Q1 = 98, Median = 104, Q3 = 106, Max = 109, Mean = 100.9 chars.
  * Word Count: Min = 2, Median = 15 words, Max = 27 words, Mean = 15.2 words.
* **Critical Finding**: Populated descriptions are **short teaser snippets** (truncated at ~109 characters) rather than complete enterprise job descriptions.
* **Phase 2 Directive**: Impute missing values with `""`. Rely on `key_skills` as the primary technical skill signal.

### 2.4. `job_desig` (Free-Text Job Designation)
* **Raw Type**: `object` (string)
* **Completeness**: 15,841 non-null (100.0%)
* **Cardinality**: 10,097 unique free-text designations
* **Top Designations**:
  * Business Analyst: 108 ($0.68\%$)
  * Data Scientist: 64 ($0.40\%$)
  * Data Analyst: 50 ($0.32\%$)
  * Digital Marketing Manager: 45 ($0.28\%$)
  * Home Base Job/ Data Entry/online Work...: 45 ($0.28\%$)
* **Data Quality Finding**: Heavy presence of peripheral and non-analytics roles originating from broad job-board scraping.
* **Phase 2 Directive**: Build keyword classification dictionary to map titles into standardized families: Data Scientist, Data Analyst, Business Analyst, Data Engineer, BI Developer, and Non-Analytics/Other.

### 2.5. `job_type` (Job Family Categorization)
* **Raw Type**: `object` (string)
* **Completeness**: 3,830 non-null; **12,011 missing** ($75.82\%$)
* **Distribution of Populated Entries**:
  * `'Analytics'`: 2,971 ($77.57\%$)
  * `'analytics'`: 746 ($19.48\%$)
  * `'ANALYTICS'`: 64 ($1.67\%$)
  * `'analytic'`: 30 ($0.78\%$)
  * `'Analytic'`: 19 ($0.50\%$)
* **Data Quality Finding**: Single category ("Analytics") disguised across 5 casing variations; zero alternative categories.
* **Phase 2 Directive**: Standardize populated casing to `'Analytics'`. Due to $>75\%$ missingness and zero variance, **exclude from predictive modeling**.

### 2.6. `key_skills` (Comma-Delimited Technical Skills)
* **Raw Type**: `object` (text)
* **Completeness**: 15,840 non-null; **1 missing record** ($0.006\%$)
* **Token Characteristics**:
  * String Length: Min = 2, Median = 70 chars, Max = 78 chars, Mean = 67.6 chars.
  * Delimited Tokens per Posting: Min = 1, Median = 5 skills, Max = 12 skills, Mean = 5.0 skills.
* **Data Quality Finding**: High quality, dense technical signal with comma delimiters.
* **Phase 2 Directive**: Tokenize, strip whitespace, fold casing, and extract multi-hot indicators for top 50 market skills. Impute the 1 missing record as `"Not Specified"`.

### 2.7. `location` (Geographic Employment Hubs)
* **Raw Type**: `object` (string)
* **Completeness**: 15,841 non-null (100.0%)
* **Cardinality**: 1,355 unique location strings
* **Top Metropolitan Centers**:
  * Bengaluru: 3,333 ($21.04\%$)
  * Mumbai: 1,992 ($12.58\%$)
  * Gurgaon: 1,313 ($8.29\%$)
  * Pune: 945 ($5.97\%$)
  * Hyderabad: 878 ($5.54\%$)
  * Chennai: 786 ($4.96\%$)
  * Delhi NCR: 593 ($3.74\%$)
* **Data Quality Finding**: ~14% of records contain multi-city strings (e.g. `'Bengaluru, Chennai'`).
* **Phase 2 Directive**: Parse primary location indicators into 7 standardized metro clusters: Bengaluru, Mumbai, NCR (Delhi/Gurgaon/Noida), Pune, Hyderabad, Chennai, and Other/Tier-2.

### 2.8. `salary` (Advertised Salary Bracket)
* **Raw Type**: `object` (discrete categorical intervals)
* **Completeness**: 15,841 non-null (100.0%)
* **Discrete Category Breakdown**:
  * `'10to15'`: 3,608 ($22.78\%$)
  * `'15to25'`: 3,281 ($20.71\%$)
  * `'6to10'`: 2,876 ($18.15\%$)
  * `'0to3'`: 2,592 ($16.36\%$)
  * `'3to6'`: 2,239 ($14.13\%$)
  * `'25to50'`: 1,245 ($7.86\%$)
* **Data Quality Finding**: Perfectly complete discrete ordinal intervals denominated in Lakhs INR.
* **Phase 2 Directive**: Create ordinal factor `salary_rank` ($1 \dots 6$), numerical midpoint `salary_midpoint` ($[1.5, 4.5, 8.0, 12.5, 20.0, 37.5]$), and high-salary binary flag `is_high_salary` ($\ge 15\text{L}$).
