# SDS Duplicate ID Handling & Cross-Validation Safeguards

**Project**: InsightPath — SAS CU Hackathon Round 2 Analytics  
**Document**: `docs/phase2/SDS_DUPLICATE_HANDLING.md`  
**Phase**: Phase 2 — Data Cleaning & Transformation  
**Governing Standard**: Psychometric Integrity & Leakage Prevention  

---

## 1. Executive Summary & Empirical Finding

In `SDS Personality Traits.xlsx` ($N = 161$), the Phase 1 audit (`docs/phase1/DUPLICATE_AUDIT.md`, `docs/phase1/IDENTIFIER_AUDIT.md`) identified **9 duplicated subject IDs** comprising **18 total rows** ($11.18\%$ of the dataset).

A granular forensic comparison across all 7 variables revealed that unlike the JDS duplicate anomaly, **all 9 duplicate pairs in SDS are 100% complete duplicates across every single attribute**:
- Identical `neuroticism`
- Identical `extraversion`
- Identical `openness_to_experience`
- Identical `agreeableness`
- Identical `conscientiousness`
- Identical `success_classification_high_low`

---

## 2. Granular Inventory of SDS Duplicate Pairs

| Duplicate ID | First Row Index | Second Row Index | Trait Vector $[\text{N}, \text{E}, \text{O}, \text{A}, \text{C}]$ | Target Classification |
| :---: | :---: | :---: | :---: | :---: |
| **`3120`** | Row 4 | Row 105 | $[34.0, 48.0, 42.0, 45.0, 52.0]$ | `1` (High Success) |
| **`3145`** | Row 12 | Row 112 | $[42.0, 39.0, 35.0, 38.0, 46.0]$ | `0` (Low Success) |
| **`3178`** | Row 24 | Row 119 | $[28.0, 54.0, 48.0, 49.0, 58.0]$ | `1` (High Success) |
| **`3201`** | Row 38 | Row 126 | $[45.0, 33.0, 31.0, 34.0, 40.0]$ | `0` (Low Success) |
| **`3234`** | Row 52 | Row 133 | $[31.0, 50.0, 44.0, 46.0, 54.0]$ | `1` (High Success) |
| **`3258`** | Row 67 | Row 141 | $[39.0, 42.0, 38.0, 41.0, 48.0]$ | `1` (High Success) |
| **`3289`** | Row 79 | Row 148 | $[47.0, 31.0, 29.0, 32.0, 38.0]$ | `0` (Low Success) |
| **`3312`** | Row 91 | Row 154 | $[26.0, 56.0, 50.0, 51.0, 60.0]$ | `1` (High Success) |
| **`3340`** | Row 101 | Row 159 | $[36.0, 45.0, 40.0, 43.0, 50.0]$ | `1` (High Success) |

### Key Observations
1. **Target Distribution Among Duplicates**:
   - $6$ duplicate pairs belong to Class 1 (High Success).
   - $3$ duplicate pairs belong to Class 0 (Low Success).
   - The ratio among duplicates ($66.7\%$ Class 1) is slightly higher than the overall dataset base rate ($52.80\%$, 85 Class 1 / 76 Class 0).
2. **Zero Intersubject Variance**:
   Unlike JDS Subject ID 3291, there are **no contradictory labels**. The duplicates are deterministic clones.

---

## 3. Methodological Rationale for Preservation in Phase 2

Under Phase 2 Governance Rules (Rule 1 & Rule 4), we do not arbitrarily delete rows from the official hackathon submission dataset:
1. **Preserving Population Size**: Retaining all $N = 161$ records preserves the official benchmark row count.
2. **Observational Weighting**: In survey methodology, repeated entries can reflect stratified oversampling or multi-rater panel evaluations.
3. **Traceability**: Deleting 9 rows silently would distort the official descriptive statistics expected by hackathon evaluators.

Therefore, `sds_processed.csv` retains all 161 rows intact.

---

## 4. Critical Data Leakage Safeguards for Phase 6 (Modeling)

While retaining identical rows in descriptive analysis is safe, **random K-Fold cross-validation on datasets with cloned rows produces severe data leakage**. If Row 4 and Row 105 (both representing Subject 3120) are randomly assigned to different folds, the model will be trained on Row 4 and evaluated on its exact twin in Row 105, artificially inflating evaluation metrics (AUC, accuracy, log-loss).

To prevent this data leakage, the following modeling protocols are pre-registered for Phase 6:

### Safeguard A: Grouped Cross-Validation (`GroupKFold`)
- All cross-validation splits must group by the identifier column `id`.
- This ensures that both instances of any duplicated subject ID are strictly held within the same fold (either entirely in the training fold or entirely in the validation fold), completely eliminating cross-fold memorization leakage:
  $$\text{Fold}(i) = \text{Fold}(j) \quad \forall \; i, j \; \text{where} \; \text{id}_i = \text{id}_j$$

### Safeguard B: Deduplicated Sensitivity Modeling
- In Phase 6, we will evaluate a deduplicated sensitivity dataset ($N = 152$) where duplicate IDs are aggregated or pruned to a single instance.
- We will verify that trait importance weights ($\beta_{\text{conscientiousness}}$, $\beta_{\text{neuroticism}}$) remain statistically equivalent between $N=161$ (Grouped CV) and $N=152$ (Standard Stratified CV).
