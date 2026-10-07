# Master Analytical Flow & Project Narrative Architecture (Phase 0)

## 1. Executive Overview

This document formalizes the complete narrative and analytical flow of the SAS CU Hackathon project. The sequence ensures that every phase builds upon the empirical findings of preceding phases, maintaining absolute continuity from initial problem definition to final jury defense.

---

## 2. Master Analytical Flow Diagram

```
================================================================================
                              BUSINESS PROBLEM
             (The Talent Disconnect in Data Science Careers)
================================================================================
                                       │
                                       ▼
                              DATA UNDERSTANDING
         (Empirical Inspection of 4 Multi-Lens Datasets & Documents)
================================================================================
                                       │
                                       ▼
                                 DATA QUALITY
       (Auditing 32 Blank Rows, Header Spaces, Duplicate Keys, Skew)
================================================================================
                                       │
                                       ▼
                               DATA PREPARATION
          (Parsing Lakhs 'L', Experience Regex, Metric Harmonization)
================================================================================
                                       │
                                       ▼
                         EXPLORATORY DATA ANALYSIS (EDA)
         (Purpose-Driven Univariate, Bivariate, Multivariate Visuals)
================================================================================
                                       │
                                       ▼
                             JOB MARKET ANALYSIS
        (Macro Demand: Roles, Experience Barriers, Enterprise Hiring)
================================================================================
                                       │
                                       ▼
                            SKILL DEMAND ANALYSIS
        (Micro Demand: Skill Frequencies, Co-occurrences, Metro Hubs)
================================================================================
                                       │
                                       ▼
                            JUNIOR SKILL ANALYSIS
      (Competency Distributions, Parametric & Non-Parametric Testing)
================================================================================
                                       │
                                       ▼
                              JUNIOR ML MODELING
     (Interpretable Classifiers: Logistic, CART, Random Forest, CV=25)
================================================================================
                                       │
                                       ▼
                          SENIOR PERSONALITY ANALYSIS
      (Big Five Distributions, Success Differentiation, Effect Sizes)
================================================================================
                                       │
                                       ▼
                              SENIOR ML MODELING
     (Predicting Consulting Success, Regularized Classifiers, CV=25)
================================================================================
                                       │
                                       ▼
                             MODEL INTERPRETATION
       (Odds Ratios, Decision Tree Rules, Permutation Importance)
================================================================================
                                       │
                                       ▼
                            CROSS-DATASET SYNTHESIS
    (Evidence Triangulation: Market × Junior Hike × Senior Success)
================================================================================
                                       │
                                       ▼
                           CAREER-READINESS FRAMEWORK
   (The 4-Quadrant Talent Matrix & Lifecycle Competency Roadmap)
================================================================================
                                       │
                                       ▼
                             BUSINESS IMPLICATIONS
  (Action Blueprints: Students, Universities, Mentors, Employers)
================================================================================
                                       │
                                       ▼
                           ROUND 2 WRITTEN REPORT
             (20–25 Page Document Aligned with 100-Mark Rubric)
================================================================================
                                       │
                                       ▼
                           PRESENTATION & SLIDE DECK
               (Executive Infographics & Visual Data Narrative)
================================================================================
                                       │
                                       ▼
                                JURY DEFENSE & Q&A
           (Defending Methodology, Non-Merge Rationale, Ethics)
================================================================================
```

---

## 3. Narrative Architecture & Stage Details

### Step 1: Business Problem Definition
* **Narrative Focus**: Frame the central industry paradox: why do individuals with technical qualifications fail to achieve long-term career success, and why do organizations face senior talent shortages?
* **Core Artifact**: `docs/phase0/PROBLEM_STATEMENT.md`

### Step 2: Data Understanding
* **Narrative Focus**: Introduce the four complementary datasets as multi-perspective lenses illuminating distinct stages of the career lifecycle rather than isolated files.
* **Core Artifact**: `docs/phase0/DATASET_INVENTORY.md` & `docs/phase0/DATASET_ROLE_MAP.md`

### Step 3: Data Quality Assessment
* **Narrative Focus**: Demonstrate meticulous data stewardship by transparently auditing trailing blank rows, header corruptions, non-unique IDs, and missingness.
* **Core Artifact**: `docs/phase0/DATA_QUALITY_PLAN.md` & `docs/phase1/DATA_QUALITY_REPORT.md`

### Step 4: Data Preparation & Transformation
* **Narrative Focus**: Convert raw text and currency markers into rigorous mathematical features while strictly guarding against data leakage and preserving raw data.
* **Core Artifact**: `docs/phase0/FEATURE_ENGINEERING_PLAN.md`

### Step 5: Exploratory Data Analysis (EDA)
* **Narrative Focus**: Unveil the empirical topography of the data through purpose-driven visualizations that directly answer research questions RQ1–RQ9.
* **Core Artifact**: `docs/phase0/EDA_PLAN.md` & `outputs/figures/`

### Step 6: Job Market Demand Analysis
* **Narrative Focus**: Dissect the macro hiring landscape (`DataScience Jobs.csv`), quantifying the volume of openings across roles, enterprise hiring concentration, and experience premiums.
* **Core Findings**: Identifies baseline salary envelopes and required entry experience across roles.

### Step 7: Granular Skill Demand Analysis
* **Narrative Focus**: Mine the micro vacancy ecosystem (`Analytics Jobs.csv`) to isolate high-frequency skills, geographic hiring hubs (Bengaluru, NCR), and high-paying skill bundles ($\ge 15\text{L}$).
* **Core Findings**: Delivers the empirical skill inventory that employers actively purchase.

### Step 8: Junior Technical Skill Analysis
* **Narrative Focus**: Transition from external market demand to internal employee outcomes (`JDS Skill Traits.xlsx`), testing which technical skills differentiate high salary-hike recipients.
* **Core Findings**: Identifies "threshold skills" (AI/ML) vs "differentiating catalysts" (Big Data, Storytelling).

### Step 9: Junior ML Modeling & Validation
* **Narrative Focus**: Build regularized, interpretable classification models under Repeated Stratified K-Fold CV (25 splits) to predict salary-hike classification reliably on small samples ($N = 139$).
* **Core Findings**: Validates model stability, out-of-fold generalization, and absence of overfitting.

### Step 10: Senior Personality Analysis
* **Narrative Focus**: Pivot to the leadership level (`SDS Personality Traits.xlsx`), investigating how Big Five personality traits differentiate high-performing customer-facing senior data scientists.
* **Core Findings**: Tests hypotheses on Conscientiousness, Emotional Stability, and Extraversion in client consulting.

### Step 11: Senior ML Modeling & Validation
* **Narrative Focus**: Train and validate interpretable classifiers to assess whether psychometric profiles predict consulting success classification on $N = 161$.
* **Core Findings**: Establishes predictive boundaries and extracts odds ratios with 95% confidence intervals.

### Step 12: Model Interpretation & Explainability
* **Narrative Focus**: Extract actionable decision trees, parameter odds ratios, and permutation feature importance rankings, cleanly separating prediction from explanation.
* **Core Findings**: Provides transparent rules and factor rankings for mentoring and coaching.

### Step 13: Cross-Dataset Analytical Synthesis
* **Narrative Focus**: Synthesize the empirical findings across all datasets without row-level merging, mapping external market demand against internal career drivers.
* **Core Findings**: Resolves the multi-lens disconnect identified in Step 1.

### Step 14: Career-Readiness & Progression Framework
* **Narrative Focus**: Deliver the capstone strategic model: the 4-Quadrant Talent Matrix mapping skills from Entry Gates to Senior Consulting Accelerators.
* **Core Deliverable**: The unified Career-Readiness Framework.

### Step 15: Business & Stakeholder Implications
* **Narrative Focus**: Translate statistical findings into concrete, high-impact blueprints for students, higher education, career mentors, and enterprise HR leaders.
* **Core Deliverable**: Stakeholder Action Blueprints.

### Step 16: Final Report Construction
* **Narrative Focus**: Author the comprehensive 20–25 page Round 2 analytics report structured strictly according to the SAS 100-mark evaluation rubric.
* **Core Deliverable**: `outputs/reports/ROUND_2_FINAL_REPORT.md`

### Step 17: Executive Presentation & Visual Assets
* **Narrative Focus**: Package the project into an executive presentation deck featuring high-resolution figures, summary infographics, and narrative slides.
* **Core Deliverable**: Round 2 Presentation Deck.

### Step 18: Jury Defense Preparation & Q&A
* **Narrative Focus**: Prepare rigorous defense rationale for jury questions: why datasets were not merged, how small-sample overfitting was prevented, ethical boundaries on personality traits, and non-causal interpretation standards.
* **Core Deliverable**: Jury Q&A Defense Brief.
