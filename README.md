# Evidence-Based Data Science Career-Readiness & Progression Framework

**SAS CU Hackathon Analytics Project — Round 2**  
*Lead Data Scientist & Analytics Architecture Team*  
**Current Status**: **Phase 0 (Complete)** | **Phase 1 (Complete)** | **Phase 2 (Complete)** | **Phase 3 (Complete)** | **Phase 4 (Complete)** | **Phase 5 (Complete)** | **Phase 6 — Ready to Start**

---

## 1. Project Overview & Hackathon Context

This project represents the complete analytical submission for the **SAS CU Hackathon**. The hackathon challenge investigates the data science talent ecosystem—spanning macro job-market postings, micro skill requirements, junior data scientist technical skill competencies, and senior customer-facing consultant personality traits.

The analysis is architected to address the official SAS Round 2 evaluation rubric (**100 Marks Total**):
* **Problem Definition / Analytics Objective**: 10 Marks
* **Approach Description**: 15 Marks
* **Data Exploration**: 25 Marks
* **Data Analysis (Statistical Modeling & Machine Learning)**: 30 Marks
* **Results and Conclusions**: 10 Marks
* **Business / Stakeholder Implications**: 10 Marks

The project delivers an end-to-end business analytics narrative culminating in a comprehensive Round 2 analytics report (~20–25 pages) and an executive presentation deck. The project strictly rejects cosmetic machine-learning optimization in favor of a cohesive, statistically validated, and stakeholder-actionable business story.

---

## 2. Central Problem Statement

> **"Data science career planning and talent development currently suffer from fragmented decision-making: job-market demand signals, early-career technical performance drivers, and senior-level behavioral success factors are analyzed in isolation. Consequently, aspiring professionals lack evidence-based guidance on how skill requirements evolve from entry to leadership, academic programs miss market-calibrated curriculum targets, and organizations face high attrition and leadership gaps. 
> 
> This project analyzes these complementary evidence sources together to identify market-aligned skills and observed success factors, translating them into an Evidence-Based Career-Readiness and Progression Framework that maps market requirements, compensation velocities, and professional success factors across career stages."**

---

## 3. The Multi-Lens Dataset Architecture

The project investigates four distinct, complementary datasets representing different observational units and populations across the data science talent lifecycle:

| Dataset | File Format | Verified Rows | Columns | Observational Unit | Core Analytical Role |
|---|---|---|---|---|---|
| **DataScience Jobs** | CSV (`DataScience Jobs.csv`) | 1,602 | 8 | Employer Job Requisitions | Macro market demand, role hierarchies, experience barriers, salary envelopes (Lakhs INR). |
| **Analytics Jobs** | CSV (`Analytics Jobs.csv`) | 15,841 | 8 | Individual Vacancies | Micro skill demand, geographic clusters, skill co-occurrence networks, categorical salary brackets. |
| **JDS Skill Traits** | Excel (`JDS Skill Traits.xlsx`) | 139 (valid) | 7 | Junior Data Scientists | Technical skill ratings (1–5 scale) associated with salary-hike classification (`salary_hike_high_or_low`). |
| **SDS Personality Traits**| Excel (`SDS Personality Traits.xlsx`)| 161 | 7 | Senior Data Scientists | Big Five personality traits (scores 17–68) associated with consulting success (`success_classification_high_low`). |

*Note: Documentation PDF files (`Data Description Doc.pdf` and `Problem Context Brief...pdf`) were absent from the workspace filesystem and are documented as **NOT VERIFIED FROM SOURCE DATA**.*

### Fundamental Principle: Analytical Integration Over Row-Level Merging
The four datasets represent distinct observational units (macro postings, micro vacancies, junior employees, senior consultants) with completely disconnected identifier domains (e.g., JDS IDs: $2007–4000$; SDS IDs: $8001–8979$; zero overlap). Row-level merging is **strictly prohibited**. The datasets are integrated conceptually through **Methodological Triangulation** and cross-evidence matrix mapping.

---

## 4. Formal Analytics Objectives

* **Objective 1 (Macro Market Demand)**: Quantify the macroeconomic structure of data science job demand across 642 hiring organizations, 10 standardized roles, experience thresholds, and compensation envelopes.
* **Objective 2 (Micro Skill Ecosystem)**: Mine 15,841 job postings to extract high-frequency skills, geographic talent clusters (Bengaluru, NCR, Mumbai), and skill combinations commanding premium compensation ($\ge 15\text{L}$).
* **Objective 3 (Junior Competency Modeling)**: Identify which technical skill dimensions (Big Data, Math/Stats, Coding, AI/ML, Dashboarding) are statistically associated with high salary-hike classification among Junior Data Scientists ($N = 139$).
* **Objective 4 (Senior Behavioral Profiling)**: Analyze how Big Five personality dimensions associate with high/low success classification among Senior, customer-facing Data Scientists ($N = 161$).
* **Objective 5 (Integrated Career Framework)**: Synthesize empirical findings across market demand, junior execution, and senior leadership into a cohesive, evidence-based Career-Readiness & Progression Framework.

---

## 5. Research Questions (RQ1 – RQ9)

* **RQ1**: Which Data Science job roles and companies show the highest observed job demand?
* **RQ2**: How does required experience relate to salary in the available job-market data?
* **RQ3**: Which locations demonstrate the greatest observed analytics-job demand?
* **RQ4**: Which technical skills appear most frequently in Analytics job postings?
* **RQ5**: Which skills or skill combinations are associated with higher observed salary levels?
* **RQ6**: Which technical skill dimensions are associated with high salary-hike classification among Junior Data Scientists?
* **RQ7**: Which personality dimensions are associated with high success classification among Senior Data Scientists?
* **RQ8**: Can interpretable classification models predict observed junior salary-hike and senior success classifications?
* **RQ9**: How can market demand and observed success-factor evidence be synthesized into an operational career-readiness framework?

---

## 6. Pre-Registered Hypotheses (H1 – H6)

* **H1**: Higher technical skill scores are positively associated with high salary-hike classification among Junior Data Scientists (tested via Mann–Whitney U / t-tests with Benjamini-Hochberg FDR).
* **H2**: Different technical skill dimensions have unequal, independent associations with salary-hike classification in a multivariable logistic model.
* **H3**: Big Five personality dimensions show statistically distinguishable distributions between high-success and low-success Senior Data Scientists.
* **H4**: Conscientiousness and Extraversion are positively associated, and Neuroticism negatively associated, with senior consulting success.
* **H5**: Required minimum experience is positively correlated with average advertised salary in macro market data.
* **H6**: High-tier salary bracket representation is statistically dependent on geographic tech hub and specialized technical skills.

---

## 7. Machine Learning & Statistical Strategy

* **Small-Sample Discipline**: With valid samples of $N = 139$ (JDS) and $N = 161$ (SDS), modeling enforces strict parsimony to prevent overfitting.
* **Candidate Classifiers**:
  1. Regularized Logistic Regression (L1/L2) — Primary parametric, odds-ratio interpretable model.
  2. Decision Tree Classifier (CART, max depth $\le 3$) — Rule-based transparent decision logic.
  3. Random Forest Classifier (100 trees, constrained depth) — Non-linear ensemble benchmark.
* **Validation Standard**: **Repeated Stratified K-Fold Cross-Validation** (5 Folds $\times$ 5 Repeats = 25 splits) embedded within leakage-free `scikit-learn` Pipelines.
* **Interpretability Architecture**: Adjusted Odds Ratios with 95% CIs, transparent decision tree paths, and permutation feature importance.
* **Ethical Guardrails**: Strictly non-deterministic interpretation of personality traits; personality models serve as mentoring/coaching diagnostics, never automated hiring gates.

---

## 8. Master Analytical Flow

```
BUSINESS PROBLEM ──► DATA UNDERSTANDING ──► DATA QUALITY ──► DATA PREPARATION
        │
        ▼
       EDA ────────► JOB MARKET ANALYSIS ─► SKILL DEMAND ANALYSIS
        │
        ▼
JUNIOR ANALYSIS ───► JUNIOR ML MODEL ─────► SENIOR ANALYSIS ──► SENIOR ML MODEL
        │
        ▼
MODEL INTERPRET ───► CROSS-DATA SYNTHESIS ─► CAREER MATRIX ───► BUSINESS RECS
        │
        ▼
ROUND 2 REPORT ────► PRESENTATION DECK ───► JURY DEFENSE & Q&A
```

---

## 9. Project Directory Structure

```
DataScienceTool/
├── data/
│   ├── raw/                  # Read-only copies of source datasets
│   ├── interim/              # Transformed & cleaned datasets
│   ├── processed/            # Feature-engineered modeling matrices
│   └── external/             # Supplementary reference data
├── notebooks/
│   ├── 01_data_audit/        # Phase 1: Ingestion & audit notebooks
│   ├── 02_data_cleaning/     # Phase 2: Reproducible cleaning pipelines
│   ├── 03_eda/               # Phase 3: Purpose-driven exploratory analysis
│   ├── 04_statistical_analysis/ # Phase 4: Formal hypothesis testing
│   ├── 05_jds_modeling/      # Phase 5: Junior skill classification
│   ├── 06_sds_modeling/      # Phase 6: Senior personality classification
│   └── 07_integrated_analysis/ # Phase 7: Cross-dataset triangulation
├── src/
│   ├── data/                 # Raw ingestion scripts
│   ├── preprocessing/        # Cleaning & text normalization modules
│   ├── features/             # Feature engineering pipelines
│   ├── analysis/             # Statistical testing & correlation modules
│   ├── modeling/             # Scikit-learn pipelines & cross-validation
│   ├── visualization/        # Standardized plotting & styling engine
│   └── utils/                # Profiling helpers & metric calculators
├── outputs/
│   ├── figures/              # Publication-quality charts & plots
│   ├── tables/               # Formatted CSV/Markdown statistical tables
│   ├── models/               # Serialized model pipelines & weights
│   └── reports/              # Phase deliverables & final Round 2 report
├── docs/
│   ├── phase0/               # Complete Phase 0 analytical foundation
│   ├── phase1/ ... phase9/   # Execution documentation by phase
│   └── final/                # Executive summaries & jury brief
├── config/                   # Configuration YAML files (paths, seeds)
├── tests/                    # Pytest test suite for pipelines
├── requirements.txt          # Python dependencies
├── README.md                 # Master project documentation
└── PROJECT_STATUS.md         # Phase-by-phase execution tracker
```

---

## 10. Reproducibility & Environment Setup

### Prerequisites
* Python 3.10+ (Tested on Python 3.13 macOS environment)

### Installation
```bash
# Clone or navigate to the project directory
cd /Users/anmolsharma/Desktop/DataScienceTool

# Install required dependencies
pip install -r requirements.txt
```

### Reproducibility Standards
* Random Seed: Pinned across all random operations (`seed = 42`).
* Zero Raw In-Place Modifications: Raw files in root and `data/raw/` remain untouched.
* Pipelines: All transformations wrapped in automated, programmatic scripts.

---

## 11. Current Phase & Future Roadmap

* **Phase 0 — Analytical Foundation**: **COMPLETE** (19 foundation documents, architecture, dataset inventory).
* **Phase 1 — Data Audit & Quality Profiling**: **COMPLETE** (13 audit tables, 14 audit docs, quality scorecard, unit tests).
* **Phase 2 — Data Cleaning & Transformation**: **COMPLETE** (4 interim, 5 processed analytical datasets, feature engineering, 14 tests).
* **Phase 3 — Purpose-Driven Exploratory Data Analysis**: **COMPLETE** (15 publication figures, 13 summary tables, EDA report, 9 tests, notebook).
* **Phase 4 — Statistical Analysis & Hypothesis Testing**: **COMPLETE** (26 tables, 7 figures, decision matrix, 2 reports, 12 tests, notebook).
* **Phase 5 — JDS Skill Modeling & Interpretability**: **COMPLETE** (7 pipelines, 25 CV splits, 24 tables, 10 figures, serialized model, 2 reports).
* **Phase 6 — SDS Personality Modeling & Interpretability**: **READY TO START** (SDS classification pipelines, CV evaluation, odds ratios).
* **Phase 7 — Cross-Dataset Synthesis**: Scheduled next.
* **Phase 8 — Career-Readiness Framework & Business Blueprint**: Scheduled next.
* **Phase 9 — Round 2 Report & Presentation Assembly**: Scheduled next.
