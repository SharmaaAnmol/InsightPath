# Formal Research Questions (Phase 0)

## 1. Overview and Design Principles

The research questions (RQs) establish the empirical scope of the project. Each question is designed to be:
1. **Answerable**: Directly measurable from the verified fields in the four supplied datasets.
2. **Defensible**: Grounded in statistical inference or data mining rather than subjective assumption.
3. **Actionable**: Capable of producing concrete business, educational, or professional development insights.

---

## 2. Research Questions Specification

### RQ1: Market Demand by Role and Organization
* **Question**: Which Data Science job roles and hiring organizations exhibit the highest observed volume of job openings in the macro market data?
* **Dataset**: `DataScience Jobs.csv` ($N = 1,602$)
* **Key Variables**: `job_title`, `company_name`, `num_of_jobs`
* **Analytical Measurement**:
  * Aggregate job opening volume ($\sum \text{num\_of\_jobs}$) and requisition frequency across the 10 standardized job titles.
  * Employer hiring concentration index (Top-10 employers by total openings; distribution of openings across enterprise tiers).
* **Expected Analytical Insight**: Identifies whether market demand is concentrated in pure Data Scientist roles or heavily distributed across engineering and analyst specializations.

---

### RQ2: Experience-to-Compensation Elasticity
* **Question**: How does required minimum experience relate to advertised compensation levels (minimum, average, and maximum salary) in the Data Science job market?
* **Dataset**: `DataScience Jobs.csv` ($N = 1,602$)
* **Key Variables**: `min_experience`, `avg_salary`, `min_salary`, `max_salary` (parsed to numeric Lakhs INR), `salary_spread`
* **Analytical Measurement**:
  * Pearson ($r$) and Spearman ($\rho$) correlation coefficients between `min_experience` and `avg_salary`.
  * Linear and polynomial regression slopes estimating average salary progression per additional year of required experience ($\Delta \text{Salary} / \Delta \text{Experience}$).
  * Salary dispersion analysis across junior (0–2 yrs), mid (3–6 yrs), and senior (7+ yrs) tiers.
* **Expected Analytical Insight**: Quantifies the empirical "experience premium" and reveals whether entry-level compensation is tightly compressed versus senior compensation spreads.

---

### RQ3: Regional Geographic Distribution of Analytics Demand
* **Question**: Which metropolitan centers and geographic clusters demonstrate the highest observed hiring volume and demand concentration in the analytics job market?
* **Dataset**: `Analytics Jobs.csv` ($N = 15,841$)
* **Key Variables**: `location`, `s_no` (posting count)
* **Analytical Measurement**:
  * Geographic string parsing and standardization of multi-city strings (e.g. `'Bengaluru, Chennai'`).
  * Relative frequency and cumulative share of postings across top metro hubs (Bengaluru, Mumbai, NCR/Gurgaon/Noida, Pune, Hyderabad, Chennai).
* **Expected Analytical Insight**: Maps the geographic talent landscape, revealing primary employment centers and decentralized/remote hiring patterns.

---

### RQ4: Frequency and Landscape of Technical Skills in Postings
* **Question**: Which specific technical skills, programming languages, and analytical tools appear most frequently within analytics job postings?
* **Dataset**: `Analytics Jobs.csv` ($N = 15,841$)
* **Key Variables**: `key_skills`, `job_description`
* **Analytical Measurement**:
  * Text tokenization, n-gram extraction, and frequency ranking across parsed `key_skills`.
  * Categorization into skill domains: Core Languages (Python, R, SQL), Big Data / Cloud (Hadoop, Spark, AWS, Azure), BI / Visualization (Tableau, PowerBI, Excel), and Modeling / ML.
* **Expected Analytical Insight**: Delivers an empirical skill inventory of the baseline versus specialized tools demanded by hiring managers.

---

### RQ5: Skill-to-Salary Tier Associations
* **Question**: Which individual technical skills or multi-skill combinations are statistically associated with higher observed salary brackets (`15to25`, `25to50` Lakhs)?
* **Dataset**: `Analytics Jobs.csv` ($N = 15,841$)
* **Key Variables**: `key_skills` (parsed binary indicators), `salary` (6 discrete brackets)
* **Analytical Measurement**:
  * Cross-tabulation and Chi-Square ($\chi^2$) tests of independence between high-frequency skills and salary brackets.
  * Cramér's $V$ effect sizes for skill-salary associations.
  * Relative Risk / Odds Ratio of premium salary classification (`\ge 15` Lakhs) given presence of specific skills (e.g., Python + Cloud vs Excel alone).
* **Expected Analytical Insight**: Disentangles commodity skills from high-premium technical combinations that command top-tier compensation.

---

### RQ6: Junior Data Scientist Skill Outcomes & Hike Differentiation
* **Question**: Which technical skill dimensions (Big Data, Math/Stats, Coding, AI/ML, Dashboarding) exhibit the strongest statistically significant association with high salary-hike classification among Junior Data Scientists?
* **Dataset**: `JDS Skill Traits.xlsx` ($N = 139$ valid cases)
* **Key Variables**: `big_data_skills`, `maths-stats_skills`, `coding_skills`, `ai_and_ml_skills`, `dashboard_and_storytelling_skills`, `salary_hike_high_or_low`
* **Analytical Measurement**:
  * Two-group comparative tests (Independent t-tests / Mann–Whitney U tests) comparing High-Hike ($N=73$) vs Low-Hike ($N=66$) cohorts across all 5 skill dimensions.
  * Standardized mean difference effect sizes (Cohen's $d$, Cliff's $\delta$).
  * Multiple logistic regression coefficients ($\beta$), Odds Ratios ($\exp(\beta)$), and 95% confidence intervals.
* **Expected Analytical Insight**: Distinguishes "hygiene/baseline skills" (high average scores across all juniors, low hike differentiation) from "catalyst skills" (statistically driving above-average salary hikes).

---

### RQ7: Senior Data Scientist Personality Trait Associations with Success
* **Question**: Which Big Five personality dimensions (Neuroticism, Extraversion, Openness, Agreeableness, Conscientiousness) demonstrate statistically distinguishable distributions and associations with observed high-success classification among Senior, customer-facing Data Scientists?
* **Dataset**: `SDS Personality Traits.xlsx` ($N = 161$ cases)
* **Key Variables**: `neuroticism`, `extraversion`, `openness_to_experience`, `agreeableness`, `conscientiousness`, `success_classification_high_low`
* **Analytical Measurement**:
  * Two-group distributional comparisons (High Success $N=85$ vs Low Success $N=76$).
  * Parametric / non-parametric two-sample tests with False Discovery Rate (Benjamini-Hochberg) adjustment for multiple testing.
  * Logistic regression odds ratios ($\text{OR}$) with profile-likelihood confidence intervals.
* **Expected Analytical Insight**: Identifies behavioral traits that act as positive correlates (e.g., conscientiousness, emotional stability) or risk factors in client-facing analytics leadership.

---

### RQ8: Predictive Utility and Model Interpretability for Career Classifications
* **Question**: Can interpretable supervised machine-learning models reliably predict junior salary-hike classification and senior consulting success classification from their respective feature profiles, and what are the dominant explanatory features?
* **Datasets**: `JDS Skill Traits.xlsx` ($N = 139$) and `SDS Personality Traits.xlsx` ($N = 161$)
* **Key Variables**: Respective feature sets and binary targets.
* **Analytical Measurement**:
  * Model evaluation via Stratified Cross-Validation reporting Accuracy, Precision, Recall, F1-Score, and ROC-AUC.
  * Comparison across Logistic Regression, Decision Tree, and Random Forest baselines.
  * Global and local feature interpretability via logistic odds ratios, tree decision paths, and permutation feature importance.
* **Expected Analytical Insight**: Establishes whether career classifications can be modeled stably without overfitting on small samples ($N \approx 140 - 160$) while isolating feature contributions clearly.

---

### RQ9: Multi-Source Synthesis into a Career-Readiness Framework
* **Question**: How can empirical insights from external market demand (RQ1–RQ5), junior technical advancement (RQ6), and senior behavioral consulting success (RQ7–RQ8) be synthesized into an operational, evidence-based Career-Readiness and Progression Framework?
* **Datasets**: Synthesis across all 4 datasets
* **Analytical Measurement**:
  * Cross-mapping skill demand frequencies against junior hike effect sizes.
  * Mapping the competency transition from early-career technical execution to senior customer-facing consulting.
  * Developing actionable guidance matrices for students, academic institutions, and enterprise talent teams.
* **Expected Analytical Insight**: Delivers the capstone strategic deliverable required for the SAS Hackathon Round 2 report and presentation.
