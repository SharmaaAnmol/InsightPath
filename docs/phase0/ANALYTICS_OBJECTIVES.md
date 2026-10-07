# Formal Analytics Objectives (Phase 0)

## 1. Overview of Analytics Objectives

To address the core problem statement systematically, the project defines five formal analytics objectives. Each objective maps directly to an underlying dataset, defines explicit input variables, designates defensible analytical methodologies, and articulates clear business relevance aligned with the SAS Round 2 evaluation structure.

---

## 2. Specification of Objectives

### Objective 1: Macro Data Science Job-Market & Compensation Architecture
* **Formal Objective**: Quantify the macroeconomic structure of data science job demand across leading hiring organizations, analyzing the distribution of roles, hiring volumes, required experience thresholds, and compensation envelopes.
* **Target Dataset**: `DataScience Jobs.csv` ($N = 1,602$)
* **Input Variables**:
  * `company_name` (Categorical, 642 unique firms)
  * `job_title` (Categorical, 10 standardized titles)
  * `min_experience` (Continuous / Integer, years)
  * `avg_salary`, `min_salary`, `max_salary` (Numeric parsed from Lakhs INR string format)
  * `num_of_jobs` (Continuous / Integer, opening volume)
* **Expected Analytical Methods**:
  * Robust univariate profiling (medians, IQR, trimming/Winsorization for extreme job counts).
  * Bivariate salary analysis across role categories and company tiers.
  * Experience-salary elasticity modeling (Ordinary Least Squares / robust linear regression).
  * Salary spread / dispersion analysis (`salary_spread = max_salary - min_salary`).
* **Expected Output**:
  * Comprehensive compensation benchmark tables by role and experience tier.
  * Market hiring concentration curves (top 10 vs long-tail employers).
  * Statistical quantification of experience premiums in annual compensation.
* **Business Relevance**: Establishes transparent compensation expectations for entry and mid-level roles, enabling job seekers and educators to benchmark market realities.

---

### Objective 2: Micro Analytics Skill Ecosystem, Geographic Clusters & Role Demand
* **Formal Objective**: Mine granular job postings to identify the high-demand technical skill co-occurrence network, map regional geographic demand hubs, categorize unstructured job designations, and analyze salary bracket distributions.
* **Target Dataset**: `Analytics Jobs.csv` ($N = 15,841$)
* **Input Variables**:
  * `key_skills` (Comma-delimited text list)
  * `location` (Geographic strings, multi-city listings)
  * `experience` (String ranges, e.g. `'5-10 yrs'`)
  * `salary` (6 discrete categorical brackets: `'0to3'`, `'3to6'`, `'6to10'`, `'10to15'`, `'15to25'`, `'25to50'`)
  * `job_desig` (Free-text titles, 10,097 unique values)
  * `job_description` (Unstructured natural language text, where available)
* **Expected Analytical Methods**:
  * Text tokenization and frequency profiling on `key_skills`.
  * Skill co-occurrence network analysis (Jaccard similarity / association rules).
  * Geographic hub normalization and regional demand share computation.
  * Experience parsing (regex extraction to derive `min_exp`, `max_exp`, `mid_exp`).
  * Chi-Square tests of independence between geographic hubs, skill clusters, and salary brackets.
* **Expected Output**:
  * Top-20 essential skills ranking across analytics sub-disciplines.
  * Geographic demand heatmap identifying primary tech centers (Bengaluru, NCR, Mumbai, etc.).
  * Empirical mapping connecting skill combinations to higher salary brackets (`15to25`, `25to50`).
* **Business Relevance**: Pinpoints the exact technical stack combinations required to unlock premium compensation tiers and reveals geographic hiring priorities.

---

### Objective 3: Junior Data Scientist Technical Competency & Hike Classification Modeling
* **Formal Objective**: Identify which specific technical skill dimensions are most strongly associated with high salary-hike classification among Junior Data Scientists, and evaluate the predictive capacity of interpretable classifiers.
* **Target Dataset**: `JDS Skill Traits.xlsx` ($N = 139$ valid records)
* **Input Variables**:
  * Predictors (1–5 scale): `big_data_skills`, `maths-stats_skills`, `coding_skills`, `ai_and_ml_skills`, `dashboard_and_storytelling_skills`
  * Target: `salary_hike_high_or_low` (Binary: 1 = High Hike, 0 = Low Hike)
* **Expected Analytical Methods**:
  * Two-sample comparative testing (Student's t-test / Mann–Whitney U test depending on normality).
  * Effect size quantification (Cohen's $d$, Cliff's $\delta$, Rank-Biserial correlation).
  * Multicollinearity diagnostic (Variance Inflation Factor - VIF).
  * Interpretable Classification: Binary Logistic Regression (Odds Ratios, Wald tests), Decision Tree Classifier, Random Forest (with Repeated Stratified K-Fold CV).
  * Feature importance ranking (Coefficients, Permutation Importance, Gini Importance).
* **Expected Output**:
  * Statistically validated ranking of technical skills by their association with salary hikes.
  * Calibrated classification models reporting Accuracy, Precision, Recall, F1, and ROC-AUC.
  * Identification of "baseline threshold skills" vs "high-impact differentiating skills".
* **Business Relevance**: Informs early-career professionals which skill investments yield the greatest tangible career advancement and guides corporate training programs.

---

### Objective 4: Senior Data Scientist Behavioral Dynamics & Consulting Success Profiling
* **Formal Objective**: Investigate the relationship between Big Five personality trait dimensions and observed high/low success classifications among Senior, customer-facing Data Scientists, evaluating behavioral differentiation at the leadership level.
* **Target Dataset**: `SDS Personality Traits.xlsx` ($N = 161$ records)
* **Input Variables**:
  * Predictors (Continuous psychometric scores, 17–68): `neuroticism`, `extraversion`, `openness_to_experience`, `agreeableness`, `conscientiousness`
  * Target: `success_classification_high_low` (Binary: 1 = High Success, 0 = Low Success)
* **Expected Analytical Methods**:
  * Normality assessment (Shapiro-Wilk) and distribution profiling across success classes.
  * Two-sample inferential testing (Independent t-tests / Mann–Whitney U tests with FDR correction).
  * Effect size computation (Cohen's $d$, Common Language Effect Size).
  * Binary Logistic Regression to estimate trait odds ratios and independent marginal effects.
  * Tree-based modeling (Decision Tree, Random Forest) evaluated via Repeated Stratified K-Fold CV.
  * Model interpretability (Odds ratios with 95% CIs, Decision rules).
* **Expected Output**:
  * Empirical behavioral profile differentiating successful from struggling senior practitioners.
  * Odds ratios revealing which traits act as enablers or risk factors in client-facing environments.
  * Rigorous documentation of model performance and stability boundaries on $N=161$.
* **Business Relevance**: Provides an evidence base for leadership development, soft-skill coaching, and executive mentoring in customer-interfacing analytical roles.

---

### Objective 5: Cross-Evidence Synthesis & Career-Readiness Framework Construction
* **Formal Objective**: Synthesize the empirical findings from market demand (Objectives 1 & 2), junior technical competencies (Objective 3), and senior behavioral traits (Objective 4) into a cohesive, evidence-based Career-Readiness & Progression Framework.
* **Target Datasets**: Synthesis across all 4 datasets
* **Input Variables**: Synthesized empirical findings, effect sizes, skill frequencies, salary brackets, and trait odds ratios.
* **Expected Analytical Methods**:
  * Multi-dimensional matrix mapping (Market Demand $\times$ Technical Hike Impact $\times$ Senior Leadership Influence).
  * Gap analysis comparing market skill demands with junior curriculum priorities.
  * Stage-gate career progression mapping (Entry $\rightarrow$ Mid-Level $\rightarrow$ Senior Consulting).
* **Expected Output**:
  * The "Data Science Career-Readiness Matrix" (actionable 3-tier blueprint).
  * Targeted stakeholder recommendation roadmaps (Students, Universities, Employers).
  * Comprehensive Round 2 Hackathon Analytics Report and Presentation Artifacts.
* **Business Relevance**: Translates isolated statistical models into high-value strategic decision frameworks for individuals and organizations.
