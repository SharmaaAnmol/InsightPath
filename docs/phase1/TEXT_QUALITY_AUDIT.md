# Text Data Quality & String Format Audit (Phase 1)

## 1. Executive Summary

This document establishes the text and unstructured string data quality audit across all textual attributes in the raw datasets. In strict compliance with Phase 1 Rule 2, **no strings have been stripped, normalized, lowercased, or tokenized**.

The audit screened text fields for:
1. Leading and trailing whitespace anomalies
2. Inconsistent capitalization (case sensitivity issues)
3. Length boundaries (abnormally short or truncated strings)
4. Delimiter integrity and repeated punctuation
5. Unstructured noise and HTML/encoding artifacts.

---

## 2. Text Attribute Diagnostics Summary Table

| Dataset | Field Name | Populated Records | Null Records | Unique Strings | Length Range (Chars) | Whitespace Issues | Casing Issues | Primary Structural Flaw |
|---|---|---|---|---|---|---|---|---|
| **Analytics Jobs** | `job_description` | 12,333 | 3,508 | 7,859 | 13 – 109 | True | False | Truncated snippet text; 22.1% missing |
| **Analytics Jobs** | `key_skills` | 15,840 | 1 | 11,155 | 2 – 78 | True | **True** | Mixed casing across skill tokens |
| **Analytics Jobs** | `job_desig` | 15,841 | 0 | 10,097 | 2 – 186 | True | **True** | High cardinality; domain noise |
| **Analytics Jobs** | `location` | 15,841 | 0 | 1,355 | 3 – 122 | True | False | Multi-city comma-separated strings |
| **DataScience Jobs** | `company_name` | 1,602 | 0 | 642 | 2 – 58 | True | False | Minor whitespace in long tail |
| **DataScience Jobs** | `job_title` | 1,602 | 0 | 10 | 12 – 25 | **False** | **False** | Clean standardized taxonomy |
| **SDS Personality** | Column Headers | 7 | 0 | 7 | 2 – 35 | **True** | **True** | Leading and internal whitespace |
| **JDS Skill Traits** | Column Headers | 7 | 0 | 7 | 2 – 33 | False | False | Hyphen in `maths-stats_skills` |

---

## 3. In-Depth Text Field Audits

### 3.1. `Analytics Jobs.csv`: `job_description`
* **Audit Finding**: Character lengths range strictly from 13 to 109 characters (Median = 104; Mean = 100.9). Word counts range from 2 to 27 words (Median = 15).
* **Structural Reality**: The text is **not** a full job description. It consists of short introductory teaser snippets scraped from portal search cards (e.g., *"Looking for senior data scientist with 5 years experience in machine learning..."*).
* **Implications**: While unsuitable for deep document embedding or dense topic modeling, it can support keyword verification to complement `key_skills`.

### 3.2. `Analytics Jobs.csv`: `key_skills`
* **Audit Finding**: Comma-delimited skill lists with an average of 5.0 tokens per posting (Min = 1, Max = 12).
* **Observed String Inconsistencies**:
  * **Casing Variability**: The identical skill appears with varied capitalization across postings:
    * `'Python'` vs `'python'` vs `'PYTHON'`
    * `'Machine Learning'` vs `'machine learning'` vs `'Machine learning'`
    * `'Sql'` vs `'SQL'` vs `'sql'`
  * **Punctuation & Whitespace**: Spurious spaces around commas (`'Python , SQL , Tableau'`).
  * **Single Missing Value**: Row 10,482 has `NaN`.
* **Phase 2 Directive**: Build a regex/string tokenizer that splits on commas, trims whitespace, casts to lowercase, and extracts standardized multi-hot binary indicators for top market skills.

### 3.3. `Analytics Jobs.csv`: `job_desig`
* **Audit Finding**: 10,097 distinct values across 15,841 rows.
* **Observed Inconsistencies**:
  * Punctuation noise: Slashes, hyphens, and ellipses (`'Data Scientist / ML Engineer...'`).
  * Non-Analytics Noise: Job listings for data entry, telecalling, SEO, and digital marketing mixed into analytics feeds.
* **Phase 2 Directive**: Design a regex role-mapping dictionary to extract 5 core analytical families: Data Scientist, Data Analyst, Business Analyst, Data Engineer, and BI Developer.

### 3.4. `Analytics Jobs.csv`: `location`
* **Audit Finding**: 1,355 unique strings.
* **Observed Multi-City Patterns**:
  * Postings listing multiple acceptable offices separated by commas: `'Bengaluru, Chennai'`, `'Delhi NCR, Gurgaon'`, `'Pune, Mumbai, Bengaluru'`.
* **Phase 2 Directive**: Extract primary metro hub flags without dropping secondary locations.

### 3.5. Header Syntax Anomalies in SDS and JDS
* **SDS Personality Traits**:
  * Header 3: `' extraversion'` (contains leading ASCII space `\x20`).
  * Header 7: `'success_ classification_ high_low'` (contains internal spaces).
* **JDS Skill Traits**:
  * Header 3: `maths-stats_skills` (contains hyphen `-`, which is an invalid identifier in Python and SQL syntax).
* **Phase 2 Directive**: Standardize headers to snake_case during initial DataFrame loading.
