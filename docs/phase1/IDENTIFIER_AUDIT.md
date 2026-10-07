# Primary Identifier & Cross-Dataset Key Audit (Phase 1)

## 1. Executive Summary

This document establishes the empirical integrity audit of all primary identifier variables across the four datasets. In strict accordance with Phase 1 principles and hackathon rules:
1. **Identifiers are NOT Predictors**: Row identifiers must never be included as analytical features in machine-learning models.
2. **Identifiers are NOT Relational Keys**: Cross-dataset merging based on integer identifiers is strictly prohibited due to semantic and population disconnects.

The machine-readable summary table is exported in [`outputs/tables/id_audit.csv`](file:///Users/anmolsharma/Desktop/DataScienceTool/outputs/tables/id_audit.csv).

---

## 2. Identifier Profiling Summary Table

| Dataset | Identifier Column | Storage Dtype | Total Records | Missing Count | Unique Count | Duplicate Count | Uniqueness Ratio | Min Value | Max Value | Semantic Meaning |
|---|---|---|---|---|---|---|---|---|---|---|
| **DataScience Jobs** | `reference_no` | `int64` | 1,602 | 0 | 1,460 | 142 | 0.9114 | 1012 | 8998 | Requisition posting reference number |
| **Analytics Jobs** | `s_no` | `int64` | 15,841 | 0 | 15,841 | 0 | 1.0000 | 1 | 15841 | Arbitrary sequential row index |
| **JDS Skill Traits** | `id` | `object` / `int64`| 171 (139 valid)| 32 (blank rows)| 137 | 2 | 0.9856 | 2007 | 4000 | Anonymized junior employee tag |
| **SDS Personality Traits**| `id` | `object` / `int64`| 161 | 0 | 152 | 9 | 0.9441 | 8001 | 8979 | Anonymized senior consultant tag |

---

## 3. Cross-Dataset Key Collision & Disconnection Audit

To definitively test whether any legitimate shared relational keys exist across datasets, a complete pairwise integer intersection was conducted:

### 3.1. Pairwise Key Overlap Matrix

```
                      [DataScience Jobs]  [Analytics Jobs]  [JDS Skills]  [SDS Traits]
                       (reference_no)         (s_no)            (id)          (id)
[DataScience Jobs]          1,460               N/A              21            33
[Analytics Jobs]             N/A               15,841            N/A           N/A
[JDS Skills]                  21                N/A              137            0
[SDS Traits]                  33                N/A               0            152
```

### 3.2. Detailed Analysis of Key Overlaps

1. **JDS vs SDS ID Disconnection ($N_{\text{overlap}} = 0$)**:
   * JDS `id` space: $[2007, 4000]$ ($N=137$ unique).
   * SDS `id` space: $[8001, 8979]$ ($N=152$ unique).
   * **Intersection**: Exactly **0 overlapping keys**. There is zero overlap between junior employees and senior consultants.
2. **JDS / SDS Collisions with `reference_no` (21 and 33 Overlaps)**:
   * 21 JDS employee IDs happen to match numerical `reference_no` values in `DataScience Jobs.csv`.
   * 33 SDS consultant IDs happen to match numerical `reference_no` values in `DataScience Jobs.csv`.
   * **Semantic Reality**: This represents pure integer collision between an internal HR employee number and an external job posting requisition ID. Joining them would map, for example, Junior Employee #2809 to an arbitrary job posting at *Wipro* or *Cognizant*, creating fabricated, nonsensical relationships.
3. **Analytics Jobs `s_no`**:
   * Represents a sequential index from 1 to 15,841. It contains no foreign-key relationship to any other dataset.

---

## 4. Methodological Conclusions & Phase 2 Directives

1. **Definitive Prohibition on Merging**: No row-level join or merge between any of the four datasets can be justified.
2. **Exclusion from Modeling**:
   * Drop `reference_no` from all market analyses.
   * Drop `s_no` from all analytics vacancy analyses.
   * Drop `id` from JDS classification pipelines (Phase 5).
   * Drop `id` from SDS classification pipelines (Phase 6).
3. **Preservation of Row Identity**: In the interim and processed datasets, preserve original row indices for auditing and traceability while quarantining identifier columns from feature sets.
