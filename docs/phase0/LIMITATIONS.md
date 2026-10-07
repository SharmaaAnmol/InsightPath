# Analytical Limitations & Boundary Conditions (Phase 0)

## 1. Context and Methodological Humility

Scientific rigor requires explicit articulation of data constraints, analytical boundaries, and methodological assumptions. Documenting limitations does not weaken the project; it establishes credibility and demonstrates mature analytics judgment to the SAS evaluation jury.

---

## 2. Key Limitations of the Study

### 2.1. Observational Cross-Sectional Nature (No Causal Inference)
* **Limitation**: All four datasets represent cross-sectional observational snapshots collected during a specific timeframe (~2024–2025).
* **Implication**:
  * Cross-sectional data cannot establish temporal precedence or causal mechanisms.
  * We cannot claim that increasing an individual's skill score by 1.0 *causes* a higher salary hike, nor that altering a personality trait *causes* consulting success.
  * Omitted variable bias (e.g. employee educational pedigree, previous company brand, manager rating style, individual project assignment difficulty) cannot be controlled.
* **Analytical Treatment**: Use strictly associational framing ("is associated with", "corresponds to higher odds of") across all reports and presentations.

---

### 2.2. Sample Size Boundaries in Employee Datasets ($N \approx 140 - 160$)
* **Limitation**: The junior dataset contains only $N = 139$ valid observations; the senior dataset contains $N = 161$ observations.
* **Implication**:
  * Small sample sizes limit statistical power to detect subtle non-linear interactions or high-order interaction effects.
  * Risk of model overfitting is heightened if complex, high-capacity models (deep trees, gradient boosting) are unconstrained.
  * Parameter estimates and odds ratios have wider confidence intervals.
* **Analytical Treatment**: Prioritize parsimonious, regularized models (Logistic Regression, shallow Decision Trees); evaluate performance using Repeated Stratified K-Fold Cross-Validation (25 splits) rather than single train/test splits.

---

### 2.3. Geographic and Economic Scope (India Tech Ecosystem Concentration)
* **Limitation**: Salary figures in `DataScience Jobs.csv` and `Analytics Jobs.csv` are denominated in Indian Lakhs (INR), and locations represent major Indian technology corridors (Bengaluru, Mumbai, Delhi-NCR, Pune, Hyderabad, Chennai).
* **Implication**:
  * Findings reflect the dynamics of the Indian technology and offshoring analytics ecosystem.
  * Generalizing salary thresholds, experience elasticities, and role structures directly to North American or European markets without adjustment is invalid.
* **Analytical Treatment**: Explicitly bound all macroeconomic findings to the Indian technology labor market.

---

### 2.4. Job Posting Signal vs. Actual Hiring Practices
* **Limitation**: Job postings (`DataScience Jobs.csv`, `Analytics Jobs.csv`) reflect advertised employer *intent* rather than finalized employment contracts.
* **Implication**:
  * Postings often list aspirational or "wishlist" skill sets that exceed actual hiring requirements.
  * Salary ranges listed in job ads represent budgeted brackets rather than negotiated compensation.
  * 75.8% missingness in `job_type` and free-text noise in `job_desig` (10,097 unique strings) in Analytics Jobs require aggressive heuristic categorization.
* **Analytical Treatment**: Treat job-market insights as employer demand signals and hiring intent benchmarks rather than census hiring data.

---

### 2.5. Self-Reported / Evaluator Subjectivity in Psychometric & Skill Ratings
* **Limitation**: Skill ratings in JDS (1.0–5.0) and personality scores in SDS (17–68) are derived from standardized subjective assessments or manager appraisals.
* **Implication**:
  * Potential evaluator leniency / halo effect (reflected in ceiling compression on JDS `ai_and_ml_skills` where median = 4.90).
  * SDS scores reflect Big Five inventory responses that may be subject to social desirability bias in corporate settings.
* **Analytical Treatment**: Audit distributions for ceiling and floor effects; report non-parametric statistics alongside parametric metrics.

---

### 2.6. Binary Coarsening of Career Outcomes
* **Limitation**: The target variables (`salary_hike_high_or_low` and `success_classification_high_low`) are binary classifications (0 vs 1).
* **Implication**:
  * Continuous career growth and consulting performance are compressed into binary thresholds, discarding granular performance variance (e.g. difference between a 15% hike and a 40% hike).
* **Analytical Treatment**: Acknowledge that models predict probability of crossing a categorical threshold rather than continuous career trajectory.

---

### 2.7. Absence of Physical Documentation PDFs in Workspace
* **Limitation**: The original files `Data Description Doc.pdf` and `Problem Context Brief, SAS VFL Demos, Guidelines Dos and Donts.pdf` were not present in the workspace filesystem.
* **Implication**:
  * Contextual nuances, official variable definitions, or specific SAS VFL demo notes beyond the provided prompt brief could not be independently cross-verified from the PDF documents.
* **Analytical Treatment**: Documented explicitly as **NOT VERIFIED FROM SOURCE DATA**; analytical execution relies strictly on the physical data files and the hackathon brief provided in the prompt.
