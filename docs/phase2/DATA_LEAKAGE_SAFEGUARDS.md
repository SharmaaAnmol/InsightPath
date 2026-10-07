# Data Leakage Prevention & Methodological Safeguards

**Project**: InsightPath — SAS CU Hackathon Round 2 Analytics  
**Document**: `docs/phase2/DATA_LEAKAGE_SAFEGUARDS.md`  
**Phase**: Phase 2 — Data Cleaning & Transformation  
**Governing Standard**: ML Best Practices, Zero Information Leakage, Cross-Validation Purity  

---

## 1. Executive Statement on Leakage Architecture

Data leakage occurs when information from outside the training dataset (such as the target variable, test partition, future states, or global sample statistics) inadvertently contaminates the model development pipeline. In competitive hackathons, models exhibiting artificially inflated test accuracy due to subtle data leakage invariably fail upon external validation.

Phase 2 establishes strict **architectural boundaries** to guarantee that data transformations performed during data preparation do not induce leakage into downstream statistical analysis (Phases 3–4) or predictive machine learning (Phases 5–6).

---

## 2. Six Primary Leakage Vectors & Implemented Safeguards

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          LEAKAGE VECTORS & SAFEGUARDS                       │
├───────────────────────────────┬─────────────────────────────────────────────┤
│ 1. Cohort Boundary Violation  │ Strict separation; zero cross-dataset joins │
│ 2. Global Distribution Leak   │ Preserved raw scale; no global Z-scaling    │
│ 3. Duplicate Clone Memorization│ GroupKFold grouped by subject ID in SDS     │
│ 4. ID Memorization            │ Explicit configuration feature exclusions   │
│ 5. Target Autocorrelation     │ Exclude salary rank/midpoint when modeling  │
│ 6. High-Missingness Distortion│ Descriptive tagging; excluded from X matrix │
└───────────────────────────────┴─────────────────────────────────────────────┘
```

---

### Safeguard 1: Strict Preservation of Cohort Independence
- **Risk**: Merging candidate-level survey data (`JDS`, `SDS`) with macro labor postings (`Analytics Jobs`, `DataScience Jobs`) at the record level.
- **Empirical Reality**: The four datasets represent fundamentally distinct observation units:
  - `JDS`: 139 individual junior candidates evaluated on 5 technical skill scales.
  - `SDS`: 161 individual senior candidates evaluated on Big Five personality traits.
  - `DataScience Jobs`: 1,602 firm-level job openings with numerical salary ranges.
  - `Analytics Jobs`: 15,841 web-scraped job listings with text skills and salary brackets.
- **Enforcement**: Phase 2 **strictly prohibits merging** datasets into a unified mega-table. Each dataset is cleaned and stored in its own dedicated interim and processed files. Harmonization across datasets occurs purely at the synthesized aggregate level in Phase 7.

---

### Safeguard 2: Zero Global Parameter Estimation (Fold Purity)
- **Risk**: Applying Z-score standardization ($\mu, \sigma$) or Min-Max scaling ($x_{\min}, x_{\max}$) across the full dataset prior to train/test splitting leaks validation distribution properties into training weights.
- **Enforcement**:
  - `jds_processed.csv` retains raw skill ratings on their natural $[1.0, 5.0]$ scale.
  - `sds_processed.csv` retains raw psychometric scores on their natural $[17.0, 68.0]$ scale.
  - In Phases 5 and 6, any normalization or standardization must be instantiated inside `sklearn.pipeline.Pipeline` objects and fitted **strictly within training folds** during cross-validation:
    $$\hat{\mu}_{\text{train}} = \frac{1}{N_{\text{train}}} \sum_{i \in \text{train}} x_i, \quad \hat{\sigma}_{\text{train}} = \sqrt{\frac{1}{N_{\text{train}}-1} \sum_{i \in \text{train}} (x_i - \hat{\mu}_{\text{train}})^2}$$

---

### Safeguard 3: Grouped Cross-Validation on Replicated Identifiers (SDS)
- **Risk**: `SDS Personality Traits` contains 9 duplicate IDs across 18 rows. Random K-fold splitting would distribute twin records across training and validation folds, enabling the model to "memorize" the identity vector and achieve falsely elevated test performance.
- **Enforcement**:
  - In Phase 6, cross-validation must be executed via `GroupKFold(n_splits=5)` grouping on the `id` column.
  - This mathematically guarantees that both records for any duplicated subject reside in the same fold.

---

### Safeguard 4: Explicit Identifier Exclusion Enforcement
- **Risk**: Decision trees or regularized linear models using arbitrary sequence IDs (`reference_no`, `s_no`, `id`) as predictive features.
- **Enforcement**:
  - A formal configuration file `config/feature_exclusions.yaml` is deployed and pre-registered.
  - The model training scripts in Phases 5 and 6 will programmatically ingest this exclusion list to strip identifier columns prior to building feature design matrices $\mathbf{X}$.

---

### Safeguard 5: Target Autocorrelation & Circularity Prevention
- **Risk**: In `Analytics Jobs`, `salary` was converted into `salary_rank` (1–6), `salary_midpoint` (1.5–37.5L), and `is_high_salary` ($\ge 15\text{L}$). If predicting `is_high_salary` in Phase 4 or 7, including `salary_rank` or `salary_midpoint` as predictors would constitute direct mathematical target leakage ($100\%$ accuracy via circular identity).
- **Enforcement**:
  - `salary_rank`, `salary_midpoint`, and `is_high_salary` are explicitly designated as alternative representations of the dependent outcome variable $\mathbf{y}$.
  - Any model predicting high salary probability will restrict feature matrix $\mathbf{X}$ strictly to:
    $$\mathbf{X} = [\text{experience features}, \text{location clusters}, \text{role families}, \text{skill indicators}]$$

---

### Safeguard 6: Descriptive-Only Tagging for High-Missingness Attributes
- **Risk**: `job_type` in `Analytics Jobs` is $75.82\%$ missing ($12,011$ nulls). Using this variable in predictive modeling would either force dropping three-quarters of the dataset or introduce severe imputation artifacts.
- **Enforcement**:
  - `job_type_clean` is tagged as **Descriptive Only** in `config/feature_exclusions.yaml`.
  - It is retained for descriptive macro reporting but completely excluded from predictive model estimation.
