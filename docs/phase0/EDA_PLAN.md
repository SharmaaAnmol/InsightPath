# Exploratory Data Analysis (EDA) Plan (Phase 0)

## 1. Principles of Purpose-Driven EDA

In accordance with the SAS Hackathon standards:
1. **Hypothesis-Linked Visualizations**: No chart will be produced merely for aesthetic filler. Every visualization must answer a concrete analytical question linked to research questions RQ1–RQ9.
2. **Dual-Lens Perspectives**: Visualizations must communicate both central tendencies (medians, means) and dispersion/variance (IQR, confidence bands, distributions).
3. **Publication-Ready Standardization**: All figures will share a unified visual design system (consistent palette, labeled axes with measurement units, data labels, and descriptive captions).

---

## 2. Structured EDA Chart Catalogue

### Section A: Data Quality & Structural Diagnostics
* **Figure 1: Missing Data & Completeness Matrix**
  * *Analytical Question*: What is the pattern and extent of missingness across `Analytics Jobs.csv` and `JDS Skill Traits.xlsx`?
  * *Variables*: All columns from `Analytics Jobs.csv` and `JDS Skill Traits.xlsx`.
  * *Visualization*: Horizontal Missingness Percentage Bar Chart with annotation of the 32 blank trailing rows in JDS and 75.8% missingness in `job_type`.
  * *Expected Interpretation*: Visually documents data sanitization steps and justifies exclusion/imputation choices.
* **Figure 2: Primary Key Multiplicity & Collision Diagnostic**
  * *Analytical Question*: How frequently do duplicate identifiers occur within datasets, and do identifier ranges intersect between junior and senior cohorts?
  * *Variables*: `reference_no` (DataScience Jobs), `id` (JDS), `id` (SDS).
  * *Visualization*: Overlapping ID Range Interval Plot and frequency distribution of duplicate keys.
  * *Expected Interpretation*: Visually demonstrates the separation of JDS ($2007–4000$) and SDS ($8001–8979$) ID domains, reinforcing why row-level joining is invalid.

---

### Section B & E: Macro Job-Market & Enterprise Hiring Analysis (DataScience Jobs)
* **Figure 3: Role Demand & Enterprise Opening Volume Distribution**
  * *Analytical Question*: Which of the 10 data science titles command the largest share of hiring volume? (RQ1)
  * *Variables*: `job_title`, `num_of_jobs`.
  * *Visualization*: Paired Horizontal Bar Chart showing Total Openings ($\sum \text{num\_of\_jobs}$) vs. Number of Postings ($N$) per role.
  * *Expected Interpretation*: Identifies volume concentration across Data Scientist, Data Engineer, and Analyst roles versus specialized titles like Data Architect.
* **Figure 4: Employer Hiring Concentration (Lorenz Curve / Top 20 Employers)**
  * *Analytical Question*: Is data science hiring concentrated among mega-IT employers or distributed across a long tail? (RQ1)
  * *Variables*: `company_name`, `num_of_jobs`.
  * *Visualization*: Ranked Bar Chart of Top-15 hiring companies alongside cumulative volume curve (Lorenz / Pareto distribution).
  * *Expected Interpretation*: Highlights enterprise hiring power (e.g. TCS, Accenture, IBM) and contextualizes volume outliers.

---

### Section C & G: Compensation Architecture & Salary Spread Analysis
* **Figure 5: Role-Wise Compensation Envelopes (Min, Avg, Max)**
  * *Analytical Question*: What are the baseline, average, and maximum salary expectations across the 10 data science roles? (RQ1, RQ2)
  * *Variables*: `job_title`, `min_salary_lakhs`, `avg_salary_lakhs`, `max_salary_lakhs`.
  * *Visualization*: Range Bar Plot / Boxplot showing median min, average, and max salary (in Lakhs INR) for each role, ordered by average salary.
  * *Expected Interpretation*: Illustrates the compensation hierarchy (e.g. Data Architect and Senior Data Scientist at the top; entry Analyst at the baseline).
* **Figure 6: Compensation Dispersion vs. Mean Salary**
  * *Analytical Question*: Do higher-paying roles feature wider salary negotiation spreads? (RQ2)
  * *Variables*: `avg_salary_lakhs`, `salary_spread` (`max - min`).
  * *Visualization*: Scatter Plot with OLS trendline and 95% confidence ribbon.
  * *Expected Interpretation*: Evaluates whether salary uncertainty and flexibility expand in senior, high-compensation roles.

---

### Section D & H: Experience Elasticity & Career Progression
* **Figure 7: Experience-to-Salary Curve & Elasticity Slope**
  * *Analytical Question*: What is the empirical wage return per year of minimum required experience? (RQ2 / H5)
  * *Variables*: `min_experience` (years), `avg_salary_lakhs` (Lakhs INR).
  * *Visualization*: Bivariate Scatter Plot with LOESS non-parametric curve and linear regression line with annotated slope ($\beta_1$, $R^2$, $p$).
  * *Expected Interpretation*: Quantifies the baseline annual salary appreciation associated with experience and identifies potential diminishing returns after 10+ years.
* **Figure 8: Career Experience Tier Salary Distributions**
  * *Analytical Question*: How does salary distribution shift across career stages (Entry: 0–2y, Mid: 3–5y, Senior: 6–9y, Lead: 10y+)?
  * *Variables*: `experience_tier`, `avg_salary_lakhs`.
  * *Visualization*: Split Violin Plot with overlaid boxplots and median annotations.
  * *Expected Interpretation*: Displays variance expansion and upward wage drift across career milestones.

---

### Section F & I: Skill Ecosystem & Geographic Clusters (Analytics Jobs)
* **Figure 9: Top-25 In-Demand Analytics Skills**
  * *Analytical Question*: Which specific technical tools and programming languages appear most frequently in job ads? (RQ4)
  * *Variables*: Tokenized `key_skills` frequencies ($N = 15,841$).
  * *Visualization*: Horizontal Bar Chart color-coded by skill category (Programming, Database/SQL, BI/Viz, Cloud, ML).
  * *Expected Interpretation*: Ranks core foundational skills (Python, SQL, Excel) against advanced competencies (AWS, Spark, Machine Learning).
* **Figure 10: Geographic Talent Demand & Regional Salary Alignment**
  * *Analytical Question*: Which metropolitan hubs dominate analytics hiring and offer higher salary brackets? (RQ3, RQ5 / H6)
  * *Variables*: `location_metro`, `salary` brackets.
  * *Visualization*: Stacked 100% Percentage Bar Chart showing salary bracket proportions across top hubs (Bengaluru, Mumbai, NCR, Pune, Hyderabad, Chennai).
  * *Expected Interpretation*: Reveals geographic concentration in Bengaluru and NCR, and identifies whether Bengaluru/Gurgaon offer higher proportions of $\ge 15\text{L}$ packages.
* **Figure 11: Skill Co-occurrence Network / Association Matrix**
  * *Analytical Question*: Which skills cluster together naturally in employer requisitions? (RQ4, RQ5)
  * *Variables*: Binary indicators for top-15 skills.
  * *Visualization*: Correlation / Jaccard Heatmap showing pairwise co-occurrence probabilities.
  * *Expected Interpretation*: Visualizes the typical "full-stack" bundles (e.g. Python + SQL + Tableau vs Python + Cloud + Spark).

---

### Section J: Junior Data Scientist Skill & Hike Differentiation (JDS)
* **Figure 12: Junior Technical Competency Profile (Radar / Distribution Chart)**
  * *Analytical Question*: How do Junior Data Scientists rate across the 5 technical skill dimensions? (RQ6)
  * *Variables*: `big_data_skills`, `maths-stats_skills`, `coding_skills`, `ai_and_ml_skills`, `dashboard_and_storytelling_skills`.
  * *Visualization*: Overlaid Density Ridgeline Plot or Boxplot series comparing all 5 skill distributions on the 1–5 scale.
  * *Expected Interpretation*: Identifies skills with high ceilings (AI/ML, Storytelling) versus wider variance (Big Data, Math/Stats).
* **Figure 13: Technical Skill Differences by Salary Hike Outcome**
  * *Analytical Question*: Which skills statistically differentiate high-hike from low-hike juniors? (RQ6 / H1, H2)
  * *Variables*: 5 skill scores grouped by `salary_hike_high_or_low` (0 vs 1).
  * *Visualization*: Grouped Bar Chart of Means $\pm$ 95% Confidence Intervals with annotated effect sizes (Cohen’s $d$) and significance stars ($* p < 0.05, ** p < 0.01$).
  * *Expected Interpretation*: Pinpoints which skills drive compensation progression in early tenure.

---

### Section K: Senior Personality Traits & Consulting Success (SDS)
* **Figure 14: Big Five Trait Profiles Across Consulting Success Classes**
  * *Analytical Question*: How do Big Five personality distributions differ between high-success and low-success senior practitioners? (RQ7 / H3, H4)
  * *Variables*: 5 Big Five trait scores grouped by `success_classification_high_low` (0 vs 1).
  * *Visualization*: Grouped Boxplot / Violin series with mean markers and individual data jitter, annotated with Cohen's $d$.
  * *Expected Interpretation*: Reveals which traits (e.g. Conscientiousness, Emotional Stability) exhibit divergence between successful and struggling senior leaders.
* **Figure 15: Personality Trait Correlation & Interaction Heatmap**
  * *Analytical Question*: How do personality traits interrelate among senior data scientists?
  * *Variables*: 5 Big Five traits.
  * *Visualization*: Correlation Matrix Heatmap with annotated Pearson $r$ and significance values.
  * *Expected Interpretation*: Checks for trait collinearity and identifies multidimensional behavioral profiles.
