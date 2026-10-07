# Categorical Variable Profiling & Text Inconsistency Audit (Phase 1)

## 1. Executive Summary

This document establishes the categorical variable profiling across all raw datasets. In strict accordance with Phase 1 Rule 2, **no categories have been normalized, re-coded, stripped of whitespace, or case-folded**. 

The audit systematically screened for:
1. High cardinality and rare categories
2. Whitespace anomalies (leading/trailing spaces)
3. Casing inconsistencies (e.g., `'Analytics'` vs `'analytics'`)
4. Free-text noise and non-standard categories.

The machine-readable summary table is exported in [`outputs/tables/categorical_profile.csv`](file:///Users/anmolsharma/Desktop/DataScienceTool/outputs/tables/categorical_profile.csv).

---

## 2. Categorical Profiling Summary Table

| Dataset | Column Name | Total Valid | Unique Categories | Whitespace Anomaly | Casing Inconsistency | Most Frequent Value | Top Value Frequency | Top Value % |
|---|---|---|---|---|---|---|---|---|
| **DataScience Jobs** | `company_name` | 1,602 | 642 | True | False | TCS | 10 | 0.62% |
| **DataScience Jobs** | `job_title` | 1,602 | 10 | False | False | Data Scientist | 188 | 11.74% |
| **Analytics Jobs** | `experience` | 15,841 | 128 | True | False | `'5-10 yrs'` | 1,010 | 6.38% |
| **Analytics Jobs** | `job_description`| 12,333 | 7,859 | True | False | Short descriptions | 45 | 0.36% |
| **Analytics Jobs** | `job_desig` | 15,841 | 10,097 | True | True | Business Analyst | 108 | 0.68% |
| **Analytics Jobs** | `job_type` | 3,830 | 5 | False | **True** | Analytics | 2,971 | 77.57% |
| **Analytics Jobs** | `key_skills` | 15,840 | 11,155 | True | True | Delimited lists | 45 | 0.28% |
| **Analytics Jobs** | `location` | 15,841 | 1,355 | True | False | Bengaluru | 3,333 | 21.04% |
| **Analytics Jobs** | `salary` | 15,841 | 6 | False | False | `'10to15'` | 3,608 | 22.78% |

---

## 3. Detailed Categorical Profiles by Dataset

### 3.1. Data Science Jobs: Standardized Titles & Enterprise Distribution
* **`job_title` (10 Standardized Titles)**:
  * Highly structured role taxonomy. Exactly 10 titles:
    1. Data Scientist ($N=188, 11.74\%$)
    2. Business Analyst ($N=188, 11.74\%$)
    3. Data Engineer ($N=188, 11.74\%$)
    4. Data Analyst ($N=187, 11.67\%$)
    5. Senior Business Analyst ($N=187, 11.67\%$)
    6. Senior Data Analyst ($N=187, 11.67\%$)
    7. Senior Data Scientist ($N=185, 11.55\%$)
    8. Senior Data Engineer ($N=183, 11.42\%$)
    9. Machine Learning Engineer ($N=59, 3.68\%$)
    10. Data Architect ($N=50, 3.12\%$)
  * *Audit Finding*: Perfectly consistent casing; 0 trailing whitespace anomalies.
* **`company_name` (642 Employers)**:
  * Top posting employers: TCS (10), Deloitte (10), UST (10), Mindtree (10), DXC Technology (10).
  * 642 unique firms across 1,602 postings confirms an extensive enterprise hiring sample.

---

### 3.2. Analytics Jobs: High Cardinality, Casing & Domain Noise
* **`job_type` (The Casing Collision)**:
  * Out of 3,830 populated records, there are 5 distinct values representing the exact same word:
    1. `'Analytics'` ($N = 2,971, 77.57\%$)
    2. `'analytics'` ($N = 746, 19.48\%$)
    3. `'ANALYTICS'` ($N = 64, 1.67\%$)
    4. `'analytic'` ($N = 30, 0.78\%$)
    5. `'Analytic'` ($N = 19, 0.50\%$)
  * *Phase 2 Action*: Standardize all variations via `.str.lower().str.strip()` to `'analytics'`.
* **`salary` (6 Discrete Categorical Brackets)**:
  * Complete coverage across all 15,841 postings (0 missing values):
    1. `'10to15'` ($N = 3,608, 22.78\%$) — Median bracket
    2. `'15to25'` ($N = 3,281, 20.71\%$) — High bracket
    3. `'6to10'` ($N = 2,876, 18.15\%$) — Mid-market
    4. `'0to3'` ($N = 2,592, 16.36\%$) — Entry-level
    5. `'3to6'` ($N = 2,239, 14.13\%$) — Early-tenure
    6. `'25to50'` ($N = 1,245, 7.86\%$) — Executive / Lead bracket
  * *Phase 2 Action*: Map to an ordered categorical factor $[1, 2, 3, 4, 5, 6]$ and assign interval midpoints $[1.5, 4.5, 8.0, 12.5, 20.0, 37.5]$.
* **`location` (Geographic Clusters & Multi-City Listings)**:
  * 1,355 unique location strings. Top metro hubs:
    1. Bengaluru ($N = 3,333, 21.04\%$)
    2. Mumbai ($N = 1,992, 12.58\%$)
    3. Gurgaon ($N = 1,313, 8.29\%$)
    4. Pune ($N = 945, 5.97\%$)
    5. Hyderabad ($N = 878, 5.54\%$)
    6. Chennai ($N = 786, 4.96\%$)
    7. Delhi NCR ($N = 593, 3.74\%$)
    8. Noida ($N = 403, 2.54\%$)
  * *Anomaly*: Multi-city strings (e.g. `'Bengaluru, Chennai'`, `'Delhi NCR, Gurgaon'`) represent ~14% of listings.
  * *Phase 2 Action*: Parse primary metro hub indicators.
* **`job_desig` (Domain Noise & High Cardinality)**:
  * 10,097 unique strings across 15,841 postings.
  * Includes core analytics roles: Business Analyst (108), Data Scientist (64), Data Analyst (50).
  * Also includes non-analytics noise from scraped job feeds: Digital Marketing Manager (45), "Home Base Job/ Data Entry/online Work/part Time Work/freelancer work" (45), SEO Executive (29).
  * *Phase 2 Action*: Implement keyword classification rules to categorize into Core Analytics vs Peripheral/Non-Analytics.
