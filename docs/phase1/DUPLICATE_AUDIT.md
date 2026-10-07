# Duplicate Records & Identifier Multiplicity Audit (Phase 1)

## 1. Executive Summary

This document presents the duplicate record and identifier multiplicity audit across all four raw datasets. In strict compliance with Phase 1 Rule 3, **no duplicate rows or duplicate keys have been deleted or modified**.

The audit differentiates between two distinct structural phenomena:
1. **Exact Row Duplicates**: Identical data across all columns simultaneously.
2. **Identifier Multiplicity (Key Duplicates)**: Records sharing the same identifier value but possessing distinct attribute values or conflicting outcome labels.

The machine-readable summary table is exported in [`outputs/tables/duplicate_profile.csv`](file:///Users/anmolsharma/Desktop/DataScienceTool/outputs/tables/duplicate_profile.csv).

---

## 2. Duplicate Audit Summary Table

| Dataset | Total Records | Exact Duplicate Rows | Exact Duplicate % | Primary ID Column | Unique IDs | Duplicate ID Count | ID Uniqueness Ratio |
|---|---|---|---|---|---|---|---|
| **DataScience Jobs** | 1,602 | 0 | 0.00% | `reference_no` | 1,460 | 142 | 0.9114 |
| **Analytics Jobs** | 15,841 | 0 | 0.00% | `s_no` | 15,841 | 0 | 1.0000 |
| **JDS Skill Traits** | 171 (139 valid) | 0 | 0.00% | `id` | 137 | 2 | 0.9856 |
| **SDS Personality Traits**| 161 | 0 | 0.00% | `id` | 152 | 9 | 0.9441 |

*Empirical Finding*: There are **zero exact full-row duplicates** across all four datasets. However, significant identifier collisions and non-uniqueness exist in `DataScience Jobs.csv`, `JDS Skill Traits.xlsx`, and `SDS Personality Traits.xlsx`.

---

## 3. Deep-Dive Audit of Identifier Multiplicity

### 3.1. Data Science Jobs: The `reference_no` Multiplicity (142 Duplicates)
* **Empirical Audit**: 142 records share a `reference_no` with another record in the dataset.
* **Structural Finding**: Identical `reference_no` values are assigned to **entirely different companies and job titles**:
  * `reference_no = 1024`: Assigned to *Exl India* (max salary 8.6L, 147 jobs) AND *IHS Markit* (max salary 18.5L, 28 jobs).
  * `reference_no = 1048`: Assigned to *InfoStretch* (max salary 23.0L) AND *Happiest Minds Technologies* (max salary 26.0L).
  * `reference_no = 1093`: Assigned to *WNS* (max salary 8.0L) AND *Shell* (max salary 27.0L).
* **Root Cause**: `reference_no` is not a relational primary key nor an internal company ID. It represents an external posting reference code reused across recruiting sources or scraped batches.
* **Analytical Treatment**: Retain all 1,602 rows as distinct hiring requisitions. Under no circumstances should `reference_no` be used as a primary key or as an analytical feature.

---

### 3.2. JDS Skill Traits: The Conflicting Target Anomaly (2 Duplicate IDs)
* **Empirical Audit**: 2 IDs appear more than once in the 139 valid records: `id = 2223` and `id = 3291`.

#### Feature and Label Inspection for Duplicate JDS IDs
| Row Index | ID | Big Data | Math/Stats | Coding | AI/ML | Storytelling | Target (`salary_hike_high_or_low`) | Audit Assessment |
|---|---|---|---|---|---|---|---|---|
| **Row 58** | `2223` | 3.5 | 4.8 | 4.5 | 4.8 | 5.0 | **0** | Consistent target label (0). |
| **Row 101** | `2223` | 4.0 | 5.0 | 5.0 | 5.0 | 5.0 | **0** | Distinct skill scores; same target (0). |
| **Row 3** | `3291` | 4.0 | 4.0 | 4.5 | 4.7 | 5.0 | **0** | **CONFLICTING TARGET** |
| **Row 29** | `3291` | 4.2 | 4.5 | 4.0 | 4.9 | 5.0 | **1** | **CONFLICTING TARGET** |

* **Critical Anomaly**: `id = 3291` appears twice with **conflicting outcome classifications** (Row 3 has `target = 0`; Row 29 has `target = 1`), despite having very similar skill ratings.
* **Implications**:
  * Confirms that `id` is an anonymized tag or non-unique identifier.
  * In Phase 5 ML modeling, retaining conflicting labels for nearly identical feature vectors introduces label noise.
* **Phase 2 Recommended Action**: Document the label conflict. In Phase 2, evaluate sensitivity: test model training both with both instances retained (as distinct observations) and with `id = 3291` quarantined/excluded ($N = 137$).

---

### 3.3. SDS Personality Traits: Subject Identifier Multiplicity (9 Duplicate IDs)
* **Empirical Audit**: 9 IDs appear twice in the 161 records: `8065`, `8198`, `8228`, `8301`, `8303`, `8367`, `8562`, `8656`, `8951`.

#### Sample Inspection of Duplicate SDS IDs
| Row Index | ID | Neuroticism | Extraversion | Openness | Agreeableness | Conscientiousness | Target (`success`) | Audit Assessment |
|---|---|---|---|---|---|---|---|---|
| **Row 35** | `8065` | 17 | 37 | 32 | 39 | 44 | **0** | Different scores & target |
| **Row 133** | `8065` | 36 | 45 | 47 | 45 | 51 | **1** | Different scores & target |
| **Row 16** | `8198` | 31 | 51 | 42 | 48 | 31 | **0** | Different scores & target |
| **Row 86** | `8198` | 41 | 38 | 48 | 51 | 59 | **1** | Different scores & target |
| **Row 31** | `8228` | 26 | 50 | 44 | 49 | 35 | **0** | Different scores; same target (0) |
| **Row 58** | `8228` | 44 | 48 | 32 | 47 | 27 | **0** | Different scores; same target (0) |

* **Structural Finding**: Rows sharing the same `id` possess **completely different psychometric trait scores**. For example, ID 8065 has Neuroticism = 17 in row 35, but Neuroticism = 36 in row 133.
* **Root Cause**: Identifiers were generated by a hashing or anonymization algorithm that suffered key collisions, or they represent repeated multi-rater evaluations of the same subject.
* **Phase 2 Recommended Action**: Treat each of the 161 rows as a distinct observational record; explicitly drop `id` from all modeling matrices.
