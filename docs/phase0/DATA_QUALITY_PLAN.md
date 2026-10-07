# Data Quality Assessment & Remediation Plan (Phase 0)

## 1. Principles of Data Quality Management

The SAS Hackathon guidelines explicitly emphasize that real-world datasets contain typographical errors, meaningless entries, inconsistent formatting, outliers, and structural anomalies. In this project:
1. **Zero Silent Corrections**: No data anomaly will be altered, removed, or imputed without explicit logging and justification.
2. **Preservation of Raw Inputs**: Raw data files remain strictly read-only; all corrections are executed through reproducible code pipelines outputting to `data/interim/`.
3. **Audit Trails**: Every data transformation must record row-count deltas ($\Delta N$) and summary distribution comparisons.

---

## 2. Empirical Data Quality Findings & Remediation Protocols

### 2.1. Missing Data Diagnostics & Treatment Plan

| Dataset | Column | Empirical Missingness | Root Cause / Mechanism | Planned Remediation Protocol |
|---|---|---|---|---|
| **JDS Skill Traits** | All 7 Columns | 32 rows (18.7%) | Trailing blank rows in Excel sheet (rows 140–171). | Strip trailing empty rows during ingestion where all features are null. Valid analytical $N = 139$. |
| **SDS Personality Traits**| All 7 Columns | 0 rows (0.0%) | None. Complete dataset. | No imputation required ($N = 161$). |
| **DataScience Jobs** | All 8 Columns | 0 rows (0.0%) | None. Complete dataset. | No imputation required ($N = 1,602$). |
| **Analytics Jobs** | `job_type` | 12,011 rows (75.82%) | Incomplete categorization by posting source. | Do not use for predictive modeling; document as uninformative due to $>75\%$ missingness. Populated values normalized. |
| **Analytics Jobs** | `job_description`| 3,508 rows (22.14%) | Omission by hiring employer. | Impute with empty string `""` for text mining; utilize `key_skills` as primary skill source (which has only 1 missing value). |
| **Analytics Jobs** | `key_skills` | 1 row (0.01%) | Random omission. | Retain posting; impute missing skill string as `"Not Specified"`. |

---

### 2.2. Duplicate Records and Identifier Collision Plan

| Dataset | Empirical Audit Finding | Nature of Anomaly | Planned Treatment Protocol |
|---|---|---|---|
| **DataScience Jobs** | 0 exact duplicate rows; 142 duplicate `reference_no` | `reference_no` is not unique across postings (e.g. 1024 shared by *Exl India* and *IHS Markit*). | Retain all 1,602 rows; treat each row as a distinct hiring requisition; document that `reference_no` is non-unique. |
| **Analytics Jobs** | 0 exact duplicate rows; 0 duplicate `s_no` | `s_no` is a perfectly unique sequential integer (1 to 15,841). | Retain all 15,841 rows as distinct job postings. |
| **JDS Skill Traits** | 0 exact duplicate rows; 2 duplicate `id`s (`id` 2223, 3291) | `id` 2223 has identical outcomes (0); `id` 3291 has conflicting target values (0 and 1). | In Phase 1 audit: inspect complete feature profiles of both rows. If identical features with conflicting labels, flag as label noise. Test sensitivity with and without conflicting duplicate. |
| **SDS Personality Traits**| 0 exact duplicate rows; 9 duplicate `id`s | Multiple rows share the same `id` but have different trait scores and target classifications. | Confirms `id` is an anonymized or non-unique subject tag, not a primary key. Treat rows as distinct observational evaluations; drop `id` from modeling. |

---

### 2.3. Syntactic, Whitespace & Typographical Quality Plan

| Dataset | Field / Location | Observed Flaw | Correction Standard |
|---|---|---|---|
| **SDS Personality Traits** | Column Headers | Leading space in `' extraversion'`; multiple spaces in `'success_ classification_ high_low'` | Standardize during loading: `.strip()`, `.replace(' ', '_')`, `.lower()`. Result: `extraversion`, `success_classification_high_low`. |
| **JDS Skill Traits** | Column Headers | Hyphen in `maths-stats_skills` | Standardize to valid Python identifier: `maths_stats_skills`. |
| **Analytics Jobs** | `job_type` | Inconsistent casing: `'Analytics'`, `'analytics'`, `'ANALYTICS'`, `'analytic'`, `'Analytic'` | Standardize via `.str.strip().str.title()` to `'Analytics'`. |
| **Analytics Jobs** | `location` | Mixed capitalization, whitespace, and multi-city strings (e.g. `'Bengaluru, Chennai '`) | Standardize casing and strip leading/trailing whitespace; parse multi-city strings into primary hub indicators. |
| **Analytics Jobs** | `job_desig` | Extreme variability (10,097 unique strings) with non-analytics noise | Tokenize and categorize into standardized analytical role families (Data Scientist, BI Analyst, Data Engineer, Non-Analytics/Other). |

---

### 2.4. Value Format Parsing & Type Conversion

| Dataset | Field | Current String Format | Conversion Protocol | Target Numerical Variable |
|---|---|---|---|---|
| **DataScience Jobs** | `avg_salary`, `min_salary`, `max_salary` | String with `'L'` suffix (e.g. `'7.8L'`) | Strip `'L'` / `'l'`, convert to `float64` | Continuous salary in Lakhs INR. |
| **Analytics Jobs** | `experience` | String ranges (e.g. `'6-10 yrs'`, `'2-5 yrs'`) | Regex pattern `r'(\d+)\s*-\s*(\d+)'` to extract bounds | `min_experience`, `max_experience`, `midpoint_experience`. |
| **Analytics Jobs** | `salary` | 6 discrete string brackets (`'0to3'`, `'3to6'`, etc.) | Map to ordered integer factor ($1 \dots 6$) and interval midpoint (e.g. `'10to15'` $\rightarrow 12.5$) | Ordinal salary rank and numerical proxy. |

---

### 2.5. Outlier Detection and Extreme Value Strategy

* **DataScience Jobs `num_of_jobs`**:
  * *Audit Finding*: Min = 3, Median = 22, Mean = 58.06, Max = 4,200. The maximum of 4,200 is an extreme outlier representing bulk mega-recruitment drives (e.g., mass campus hiring by IT services giants).
  * *Treatment*: Do not blindly delete; report raw statistics alongside log-transformed ($\log_{10}(\text{num\_of\_jobs})$) or median/IQR metrics.
* **DataScience Jobs `min_experience`**:
  * *Audit Finding*: Ranges from 0 to 21 years. Values $> 15$ years are rare enterprise architect positions.
  * *Treatment*: Retain for macro profiling; segment into experience tiers: Junior (0–2 yrs), Mid (3–6 yrs), Senior (7–10 yrs), Executive/Architect (11+ yrs).
* **JDS & SDS Score Ranges**:
  * *Audit Finding*: All JDS skill scores lie strictly within the valid 1.0–5.0 scale (observed 2.2 to 5.0). All SDS scores lie strictly within 17.0–68.0.
  * *Treatment*: Verify absence of out-of-bound ratings ($< 1$ or $> 5$ in JDS; $< 0$ or $> 100$ in SDS).

---

### 2.6. Target Distribution & Leakage Safeguards

* **Target Balance**:
  * JDS `salary_hike_high_or_low`: 73 positive (52.5%), 66 negative (47.5%).
  * SDS `success_classification_high_low`: 85 positive (52.8%), 76 negative (47.2%).
  * *Assessment*: Both target variables exhibit near-perfect class balance (~53:47). No synthetic oversampling (SMOTE) is required or justified.
* **Data & Target Leakage Safeguards**:
  * Ensure `id` and `reference_no` are completely excluded from predictive modeling pipelines.
  * Ensure all feature scaling and transformations are fitted strictly on training folds within cross-validation, never on the full dataset before splitting.
