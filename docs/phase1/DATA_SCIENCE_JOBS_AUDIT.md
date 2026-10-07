# Detailed Dataset Audit: Data Science Jobs (Phase 1)

## 1. Executive Summary

This document establishes the dedicated column-by-column audit for `DataScience Jobs.csv` ($N = 1,602$). In strict compliance with Phase 1 Rule 1 and Rule 2, **no raw values have been converted, cleaned, or modified**.

The dataset represents macro-level employer hiring requisitions across 642 hiring organizations. Overall completeness is **100.0%** across all 8 fields, but formatting anomalies (string notation for currency) and identifier multiplicity require explicit remediation planning for Phase 2.

---

## 2. Comprehensive Attribute Audit

### 2.1. `reference_no` (Requisition Reference Code)
* **Raw Type**: `int64`
* **Range**: $1,012$ to $8,998$
* **Completeness**: 1,602 non-null (100.0%)
* **Cardinality**: 1,460 unique values (142 duplicate occurrences; uniqueness ratio = $0.9114$)
* **Data Quality Finding**: The identical `reference_no` appears across multiple competing companies (e.g. `1024` shared by *Exl India* and *IHS Markit*). 
* **Phase 2 Directive**: **Do NOT treat as a primary key or relational merge key**. Retain each row as an independent hiring requisition. Drop from analytical modeling.

### 2.2. `company_name` (Hiring Organization)
* **Raw Type**: `object` (string)
* **Completeness**: 1,602 non-null (100.0%)
* **Cardinality**: 642 unique companies
* **Top Employers by Posting Count**:
  * TCS: 10 postings
  * Deloitte: 10 postings
  * UST: 10 postings
  * DXC Technology: 10 postings
  * Mindtree: 10 postings
  * Accenture: 9 postings
  * IBM: 8 postings
* **Data Quality Finding**: Generally clean text, with minor casing/whitespace variations in the long tail.
* **Phase 2 Directive**: Standardize via `.str.strip()`.

### 2.3. `job_title` (Role Classification)
* **Raw Type**: `object` (string)
* **Completeness**: 1,602 non-null (100.0%)
* **Cardinality**: Exactly 10 standardized titles:
  1. Data Scientist: 188 ($11.74\%$)
  2. Business Analyst: 188 ($11.74\%$)
  3. Data Engineer: 188 ($11.74\%$)
  4. Data Analyst: 187 ($11.67\%$)
  5. Senior Business Analyst: 187 ($11.67\%$)
  6. Senior Data Analyst: 187 ($11.67\%$)
  7. Senior Data Scientist: 185 ($11.55\%$)
  8. Senior Data Engineer: 183 ($11.42\%$)
  9. Machine Learning Engineer: 59 ($3.68\%$)
  10. Data Architect: 50 ($3.12\%$)
* **Data Quality Finding**: Highly structured taxonomy; 0 typos or capitalization inconsistencies.
* **Phase 2 Directive**: Preserve as core categorical grouping factor for salary and experience benchmarks.

### 2.4. `min_experience` (Required Experience Barrier)
* **Raw Type**: `int64` (years)
* **Completeness**: 1,602 non-null (100.0%)
* **Statistical Distribution**:
  * Min: $0$ years (entry level)
  * Q1: $1.0$ years
  * Median: $2.0$ years
  * Mean: $2.80$ years
  * Q3: $4.0$ years
  * Max: $21.0$ years (Principal Architect roles)
* **Data Quality Finding**: 0 negative values; 0 impossible values. 39 records ($2.43\%$) exceed the upper Tukey bound ($8.5$ years).
* **Phase 2 Directive**: Retain continuous integer years; bin into experience tiers: Entry (`0-2`), Mid (`3-5`), Senior (`6-9`), Lead (`10+`).

### 2.5. `avg_salary`, `min_salary`, `max_salary` (Advertised Compensation)
* **Raw Type**: `object` (strings with `'L'` suffix, e.g. `'7.8L'`, `'4.5L'`, `'16.0L'`)
* **Completeness**: 1,602 non-null across all three columns (100.0%)
* **Currency Standard**: Indian Lakhs (INR, where $1\text{ Lakh} = 100,000\text{ INR}$).
* **Empirical Range Analysis**:
  * `min_salary`: $0.2\text{L}$ to $55.0\text{L}$ (Median $\approx 4.5\text{L}$)
  * `avg_salary`: $1.4\text{L}$ to $82.0\text{L}$ (Median $\approx 9.7\text{L}$)
  * `max_salary`: $2.0\text{L}$ to $102.0\text{L}$ (Median $\approx 18.0\text{L}$)
* **Mathematical Consistency Audit**:
  * Tested condition: $\text{min\_salary} \le \text{avg\_salary} \le \text{max\_salary}$
  * **Result**: **0 violations across all 1,602 rows** (100% mathematically valid ordering).
* **Data Quality Finding**: Stored as text strings with `'L'`.
* **Phase 2 Directive**: Develop parser: strip `'L'`, cast to `float64`, derive `salary_spread = max_salary - min_salary`.

### 2.6. `num_of_jobs` (Advertised Opening Volume)
* **Raw Type**: `int64`
* **Completeness**: 1,602 non-null (100.0%)
* **Statistical Distribution**:
  * Min: $3$
  * Q1: $9.25$
  * Median: $22.0$
  * Mean: $58.06$
  * Q3: $47.0$
  * Max: $4,200.0$
  * Skewness: $+12.83$ (severe positive skewness)
* **Data Quality Finding**: 164 records ($10.24\%$) exceed the Tukey upper bound ($103.6$ jobs), peaking at 4,200 openings.
* **Context**: Represents mega-campus recruitment drives by Indian IT service providers.
* **Phase 2 Directive**: Retain all records; engineer $\log_{10}(\text{num\_of\_jobs})$ for regression sensitivity.
