# Phase 3 — Purpose-Driven EDA Execution Report

**Project**: InsightPath — SAS CU Hackathon Round 2 Analytics  
**Document**: `docs/phase3/PHASE_3_EXECUTION_REPORT.md`  
**Phase**: Phase 3 — Purpose-Driven Exploratory Data Analysis  
**Status**: COMPLETE  
**Execution Timestamp**: 2026-10-07T16:38:00Z  

---

## 1. Executive Summary

Phase 3 ("Purpose-Driven Exploratory Data Analysis") has executed to completion in full compliance with the pre-registered analytical plan (`docs/phase0/EDA_PLAN.md`), the 9 research questions (`docs/phase0/RESEARCH_QUESTIONS.md`), and the governance safeguards established in Phase 2.

All descriptive statistics, group comparisons, skill differentials, and model-readiness screenings were performed exclusively against the **Phase 2 processed analytical datasets**. Raw datasets remain cryptographically invariant. The analysis generated **15 publication-grade figures** (saved in both high-resolution PNG and scalable vector SVG formats) and **13 comprehensive analytical tables** in `outputs/tables/phase3/`.

### Phase Boundary Affirmations
* **Phase 4 Statistical Hypothesis Testing was NOT performed**: All $p$-values and test statistics reported in Phase 3 are exploratory diagnostics; formal parametric/non-parametric tests, family-wise error adjustments, and pre-registered hypothesis decisions (H1–H6) are strictly deferred to Phase 4.
* **Phase 5 & Phase 6 Predictive Machine Learning was NOT performed**: No classifiers (Logistic Regression, Decision Trees, Random Forests, XGBoost) were trained, cross-validated, or hyperparameter-tuned.

---

## 2. Input Datasets Analyzed

All inputs loaded from `data/processed/`:

| Dataset Identifier | Physical File Path | Verified Rows ($N$) | Verified Columns ($P$) | Integrity Status |
| :--- | :--- | :---: | :---: | :---: |
| **DataScience Jobs** | `data/processed/data_science_jobs_processed.csv` | 1,602 | 14 | PASS (100% complete) |
| **Analytics Jobs** | `data/processed/analytics_jobs_processed.csv` | 15,841 | 72 | PASS (100% complete) |
| **JDS Skill Traits (Baseline)** | `data/processed/jds_processed.csv` | 139 | 7 | PASS (100% complete) |
| **JDS Skill Traits (Sensitivity)**| `data/processed/jds_sensitivity_3291_removed.csv` | 137 | 7 | PASS (ID 3291 excluded) |
| **SDS Personality Traits** | `data/processed/sds_processed.csv` | 161 | 7 | PASS (100% complete) |

---

## 3. Deliverables Inventory

### Python Source Modules
- `src/visualization/style.py`: Standardized publication theme, typography, color palettes, and dual PNG/SVG exporter.
- `src/visualization/figure_generators.py`: Generator functions for all 15 publication figures with complete annotations.
- `src/analysis/eda_summary.py`: Analytical calculation engine producing all 13 summary and diagnostic tables.
- `src/analysis/run_phase3.py`: Master automated pipeline script and validation engine.

### Generated Figures (`outputs/figures/phase3/`)
All 15 figures generated in both PNG (300 DPI) and SVG formats (30 files total):
1. `fig01_missingness_matrix.png` & `.svg` (283.6 KB / 125.1 KB)
2. `fig02_id_multiplicity_diagnostic.png` & `.svg` (261.2 KB / 120.4 KB)
3. `fig03_role_demand_volume.png` & `.svg` (246.5 KB / 117.2 KB)
4. `fig04_employer_hiring_concentration.png` & `.svg` (315.3 KB / 118.5 KB)
5. `fig05_role_compensation_envelopes.png` & `.svg` (238.8 KB / 104.2 KB)
6. `fig06_compensation_dispersion.png` & `.svg` (579.2 KB / 323.4 KB)
7. `fig07_experience_salary_curve.png` & `.svg` (423.6 KB / 329.1 KB)
8. `fig08_career_experience_tiers.png` & `.svg` (189.0 KB / 91.3 KB)
9. `fig09_top_skills_demand.png` & `.svg` (345.4 KB / 135.2 KB)
10. `fig10_geographic_salary_alignment.png` & `.svg` (170.4 KB / 99.1 KB)
11. `fig11_skill_cooccurrence_matrix.png` & `.svg` (444.0 KB / 206.3 KB)
12. `fig12_jds_competency_profiles.png` & `.svg` (186.8 KB / 100.2 KB)
13. `fig13_jds_hike_differentiation.png` & `.svg` (176.4 KB / 103.4 KB)
14. `fig14_sds_personality_profiles.png` & `.svg` (188.6 KB / 104.1 KB)
15. `fig15_sds_trait_correlation_matrix.png` & `.svg` (188.3 KB / 93.2 KB)

### Generated Analytical Tables (`outputs/tables/phase3/`)
All 13 analytical tables exported:
1. `phase3_descriptive_summary.csv` (25 records)
2. `phase3_role_demand.csv` (10 records)
3. `phase3_company_demand.csv` (25 records)
4. `phase3_salary_summary.csv` (14 records)
5. `phase3_experience_summary.csv` (2 records)
6. `phase3_location_summary.csv` (7 records)
7. `phase3_skill_frequency.csv` (50 records)
8. `phase3_skill_salary_comparison.csv` (30 records)
9. `phase3_jds_summary.csv` (5 records)
10. `phase3_sds_summary.csv` (5 records)
11. `phase3_correlation_summary.csv` (30 records)
12. `phase3_diagnostic_summary.csv` (12 records)
13. `phase3_rq_figure_map.csv` (9 records)

### Reproducible Notebook & Test Suite
- `notebooks/03_eda/03_eda.ipynb`: 27-cell executable walkthrough.
- `tests/test_phase3_eda.py`: 9 unit and integration tests (100% passing).

---

## 4. Post-EDA Validation Checks & Results

The validation suite in `run_phase3.py` and `tests/test_phase3_eda.py` evaluated:

| Category | Check Description | Criterion | Result |
| :--- | :--- | :--- | :---: |
| **Data Integrity** | Processed Dataset Row Counts | DS=1602, AJ=15841, JDS=139, SDS=161 | **PASS** |
| | Target Domain Integrity | Binary $\{0, 1\}$ in JDS, SDS, Analytics | **PASS** |
| | Numeric Field Integrity | Salaries, experience, skills, traits valid | **PASS** |
| **Table Integrity** | Table Existence & Size | All 13 tables $> 50$ bytes | **PASS** |
| | Reconciled Population Totals | Reconciles to 15,841 and 1,602 | **PASS** |
| **Figure Integrity**| Figure Existence (PNG & SVG) | Exactly 15 PNG and 15 SVG files present | **PASS** |
| | File Size & Completeness | PNG $> 5$ KB, SVG $> 1$ KB (zero blank plots)| **PASS** |
| **RQ Coverage** | Exhaustive Mapping | RQ1–RQ9 all covered with findings & limits | **PASS** |
| **Leakage Audit** | Zero ID Usage in Features | `id`, `reference_no`, `s_no` excluded | **PASS** |
| | Zero Target Autocorrelation | `salary_rank`/`midpoint` barred from predictors | **PASS** |
| | Zero Cross-Dataset Row Joins | 4 distinct cohorts preserved independently | **PASS** |

---

## 5. Material Anomalies & Analytical Caveats Documented

1. **JDS Subject ID 3291 Contradiction**:
   Identical skill vectors between Row 3 (target=0) and Row 29 (target=1). Maintained dual-dataset strategy (Baseline $N=139$, Sensitivity $N=137$); verified that effect sizes remain stable ($\Delta d < 0.02$).
2. **SDS Duplicate Subject ID Pairs**:
   18 rows represent 9 duplicate ID pairs with identical trait scores and targets. Documented as observational replications; `GroupKFold` cross-validation pre-registered as mandatory for Phase 6.
3. **Analytics Jobs Scraping Heterogeneity**:
   $84.65\%$ ($13,410 / 15,841$) of postings belong to `Non-Analytics / Other` due to scraper keywords. Core data roles ($2,431$ postings) must be segmented during skill-premium modeling.
4. **DataScience Jobs Hiring Volume Skewness**:
   `num_of_jobs` exhibits positive skewness of $+7.82$ (max $= 82$). Must be modeled on logarithmic scale (`log10_num_of_jobs`).
