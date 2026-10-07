# Master Analytical Methodology (Phase 0)

## 1. Overview and Standards Alignment

This document articulates the end-to-end analytical methodology governing the project. The architecture is engineered to satisfy the SAS CU Hackathon Round 2 evaluation structure (100 Marks Total):
* **Problem Definition / Analytics Objective**: 10 Marks
* **Approach Description**: 15 Marks
* **Data Exploration**: 25 Marks
* **Data Analysis (Statistics & ML)**: 30 Marks
* **Results and Conclusions**: 10 Marks
* **Business / Stakeholder Implications**: 10 Marks

The methodology follows a 15-stage disciplined pipeline maintaining strict segregation between raw data, cleaned artifacts, engineered features, statistical models, and strategic synthesis.

---

## 2. The 15-Stage Analytical Pipeline

```
[STAGE 1: Ingestion] ──────► [STAGE 2: Profiling] ──────► [STAGE 3: DQ Assessment]
                                                                  │
[STAGE 6: Feature Eng.] ◄─── [STAGE 5: Transform] ◄────── [STAGE 4: Cleaning]
        │
        ▼
[STAGE 7: EDA] ────────────► [STAGE 8: Statistics] ─────► [STAGE 9: Machine Learning]
                                                                  │
[STAGE 12: Synthesis] ◄───── [STAGE 11: Interpret] ◄───── [STAGE 10: Validation]
        │
        ▼
[STAGE 13: Business Recs] ──► [STAGE 14: Viz / Dash] ───► [STAGE 15: Final Report]
```

---

### Stage 1: Data Ingestion
* **Purpose**: Establish reproducible, read-only ingestion pipelines that load all raw source formats into memory without altering raw files on disk.
* **Expected Methods**:
  * Python ingestion scripts utilizing `pandas` and custom XML/openpyxl parsers.
  * Preservation checks: source files stored in `data/raw/` with read-only permissions where feasible.
  * Automated logging of raw record counts and byte hashes.
* **Expected Outputs**: Raw DataFrame instances loaded in memory; initial ingestion log.

### Stage 2: Data Profiling
* **Purpose**: Systematically inspect data dimensions, schema types, value ranges, uniqueness, and preliminary distributions.
* **Expected Methods**:
  * Automated column profiling (types, null counts, cardinalities, memory usage).
  * Extreme value screening and boundary checks.
* **Expected Outputs**: Automated data profile tables documented in Phase 1 audit notebooks.

### Stage 3: Data Quality Assessment
* **Purpose**: Rigorously audit the data for anomalies explicitly flagged in SAS guidance (mistyped values, trailing empty rows, header whitespace, duplicate keys, high missingness).
* **Expected Methods**:
  * Missing data pattern analysis (Missing Completely at Random - MCAR vs Missing at Random - MAR).
  * Duplicate identification (exact row vs primary identifier duplicates).
  * Syntax and string corruption audits (e.g., `' extraversion'`, `'success_ classification_ high_low'`).
* **Expected Outputs**: Formal Data Quality Report (`docs/phase1/DATA_QUALITY_REPORT.md`) with explicit remediation rules.

### Stage 4: Data Cleaning
* **Purpose**: Execute documented, transparent, and non-destructive cleaning transformations.
* **Expected Methods**:
  * Stripping 32 trailing empty rows from JDS.
  * Trimming column header whitespace and standardizing to snake_case.
  * Handling duplicate identifiers in JDS and SDS according to approved audit protocols.
  * Standardizing casing across categorical fields (e.g. normalizing `job_type` variants: `'analytics'`, `'ANALYTICS'`, `'Analytics'`).
* **Expected Outputs**: Cleaned intermediate datasets saved to `data/interim/`.

### Stage 5: Data Transformation
* **Purpose**: Convert unstructured strings, currency notations, and experience brackets into mathematically operable analytical variables.
* **Expected Methods**:
  * Salary parsing: Strip `'L'` suffix from `DataScience Jobs.csv` (`min_salary`, `avg_salary`, `max_salary`) and convert to `float64` (Lakhs INR).
  * Experience parsing: Regex extraction of `min_experience`, `max_experience`, and `midpoint_experience` from `Analytics Jobs.csv` string ranges (`'6-10 yrs'`).
  * Categorical ordering: Map `salary` brackets in `Analytics Jobs.csv` to ordinal integers ($1 = \text{0to3}, \dots, 6 = \text{25to50}$) and band midpoints.
* **Expected Outputs**: Transformed datasets ready for feature engineering in `data/interim/`.

### Stage 6: Feature Engineering
* **Purpose**: Derive domain-informed analytical features that enrich descriptive exploration and predictive modeling without introducing data leakage.
* **Expected Methods**:
  * `salary_spread`: Compute absolute spread (`max_salary - min_salary`) and relative spread (`spread / avg_salary`).
  * `skill_tokens`: Parse comma-delimited `key_skills` into binary one-hot indicators for top-50 market skills.
  * `location_cluster`: Consolidate 1,355 raw locations into primary tech metropolitan hubs (Bengaluru, Mumbai, Delhi-NCR, Pune, Hyderabad, Chennai, Tier-2/Other).
  * Psychometric standard scores: Compute z-scores for Big Five personality traits in SDS to enable standardized regression comparison.
* **Expected Outputs**: Processed analytical feature matrices saved to `data/processed/`.

### Stage 7: Exploratory Data Analysis (EDA)
* **Purpose**: Uncover empirical patterns, test distributional assumptions, and generate visual evidence addressing the research questions.
* **Expected Methods**:
  * Univariate analysis: Histograms, kernel density estimates, boxplots, and violin plots.
  * Bivariate analysis: Experience-to-salary scatter plots, role-wise salary boxplots, skill frequency bar plots.
  * Multivariate analysis: Correlation heatmaps (Pearson, Spearman), pairplots across skill and personality dimensions.
* **Expected Outputs**: Curated, publication-quality figures saved to `outputs/figures/`; narrative analytical logs in `notebooks/03_eda/`.

### Stage 8: Statistical Analysis & Hypothesis Testing
* **Purpose**: Subject the defined hypotheses (H1–H6) to formal statistical testing, evaluating both statistical significance ($p$-values) and practical significance (effect sizes).
* **Expected Methods**:
  * Normality testing (Shapiro-Wilk) and variance homogeneity testing (Levene's test).
  * Two-sample comparative testing: Independent t-tests (parametric) and Mann–Whitney U tests (non-parametric).
  * Multiple testing correction: Benjamini-Hochberg False Discovery Rate (FDR).
  * Effect size computation: Cohen's $d$, Cliff's $\delta$, Rank-Biserial correlation, Cramér's $V$, Odds Ratios.
  * Categorical independence: Pearson $\chi^2$ tests with standardized adjusted residuals.
* **Expected Outputs**: Comprehensive statistical summary tables saved to `outputs/tables/`; formal hypothesis acceptance/rejection logs.

### Stage 9: Supervised Machine Learning
* **Purpose**: Train interpretable classification models to predict binary career outcomes (`salary_hike_high_or_low` in JDS; `success_classification_high_low` in SDS) while strictly guarding against overfitting on modest sample sizes ($N \approx 140 - 160$).
* **Expected Methods**:
  * Candidate Models:
    1. L1/L2 Regularized Logistic Regression (Parametric / Highly Interpretable)
    2. Decision Tree Classifier (Non-linear / Rule-based)
    3. Random Forest Classifier (Ensemble / Non-linear Benchmark)
  * Resampling: Repeated Stratified K-Fold Cross-Validation (5 Folds $\times$ 5 Repeats) to guarantee stability.
* **Expected Outputs**: Model artifacts saved to `outputs/models/`; cross-validation metric logs.

### Stage 10: Model Validation & Diagnostics
* **Purpose**: Conduct rigorous multi-metric performance evaluations ensuring balanced trade-offs between precision, recall, and discrimination ability.
* **Expected Methods**:
  * Evaluation Metrics: Out-of-fold Accuracy, Precision, Recall, F1-Score, ROC-AUC, and Confusion Matrices.
  * Learning curves and validation curves to diagnose underfitting vs overfitting.
  * Permutation testing against a dummy/null classifier baseline.
* **Expected Outputs**: Cross-validated metric comparison tables and ROC/PR curves in `outputs/figures/`.

### Stage 11: Model Interpretation & Explainability
* **Purpose**: Extract transparent, human-understandable insights explaining *why* models make specific predictions and which features drive career outcomes.
* **Expected Methods**:
  * Logistic Regression: Parameter estimates ($\beta$), Adjusted Odds Ratios ($\exp(\beta)$), and 95% profile likelihood confidence intervals.
  * Decision Trees: Visualization of explicit decision rules and tree splits.
  * Random Forests: Permutation feature importance and Mean Decrease in Impurity (MDI).
* **Expected Outputs**: Feature importance plots and odds ratio forest plots saved to `outputs/figures/`.

### Stage 12: Cross-Dataset Synthesis
* **Purpose**: Triangulate findings across external market demand, junior technical differentiation, and senior consulting success without row-level merging.
* **Expected Methods**:
  * 3-Dimensional Talent Matrix mapping: Market Frequency $\times$ Junior Hike Effect Size $\times$ Senior Trait Influence.
  * Identification of curriculum gaps between university training and employer demands.
* **Expected Outputs**: Master Cross-Dataset Synthesis document (`docs/final/CROSS_DATASET_SYNTHESIS.md`).

### Stage 13: Business & Policy Recommendations
* **Purpose**: Translate empirical findings into actionable, tailored strategies for each identified stakeholder group.
* **Expected Methods**:
  * Stakeholder impact mapping: Students, Higher Education Institutions, Corporate Mentorship Programs, Talent Acquisition Teams.
  * Explicit ethical guardrails against algorithmic hiring or deterministic personality profiling.
* **Expected Outputs**: Stakeholder Recommendation Roadmap document.

### Stage 14: Data Visualizations & Executive Dashboards
* **Purpose**: Create polished, high-impact visualizations and executive artifacts that visually convey the business narrative for Round 2 presentation.
* **Expected Methods**:
  * Matplotlib / Seaborn styled visualization suites adhering to consistent design systems.
  * Executive summary infographic slides and presentation visual assets.
* **Expected Outputs**: High-resolution figures in `outputs/figures/`.

### Stage 15: Final Report & Presentation Deliverables
* **Purpose**: Synthesize all code, outputs, and documentation into the formal 20–25 page Round 2 Hackathon Report and presentation deck.
* **Expected Methods**:
  * Structuring exactly to the SAS 100-mark evaluation sections.
  * Peer review and reproducibility verification from an end-to-end execution script.
* **Expected Outputs**: Final Report Markdown/PDF in `outputs/reports/` and slide deck assets.
