# Feature Engineering & Transformation Plan (Phase 0)

## 1. Principles of Feature Engineering

Feature engineering in this project is guided by three non-negotiable principles:
1. **Domain Relevance**: Every engineered feature must reflect a meaningful economic, organizational, or behavioral concept.
2. **Leakage Prevention**: All transformations (scaling, standardization, encoding) must be computed strictly within cross-validation folds during predictive modeling.
3. **Parsimony & Preservation**: Preserve original raw scales alongside engineered variants; never perform destructive transformations that obscure the original data.

---

## 2. Planned Transformations by Dataset

### 2.1. Dataset 1: DataScience Jobs (`DataScience Jobs.csv`)

| Target Feature | Source Fields | Transformation Logic | Analytical Rationale |
|---|---|---|---|
| `min_salary_lakhs` | `min_salary` | Strip `'L'` / whitespace, cast to `float64` | Converts string currency to continuous numeric Lakhs INR. |
| `avg_salary_lakhs` | `avg_salary` | Strip `'L'` / whitespace, cast to `float64` | Core dependent variable for compensation analysis. |
| `max_salary_lakhs` | `max_salary` | Strip `'L'` / whitespace, cast to `float64` | Ceiling compensation boundary. |
| `salary_spread` | `max_salary_lakhs`, `min_salary_lakhs` | `max_salary_lakhs - min_salary_lakhs` | Measures employer salary dispersion / negotiation flexibility. |
| `salary_spread_ratio`| `salary_spread`, `avg_salary_lakhs` | `salary_spread / avg_salary_lakhs` | Normalized compensation uncertainty index. |
| `log_num_of_jobs` | `num_of_jobs` | $\log_{10}(\text{num\_of\_jobs})$ | Normalizes severe right-skewness of mega-recruitment volumes. |
| `experience_tier` | `min_experience` | Binned: `[0-2]` Entry, `[3-5]` Mid, `[6-9]` Senior, `[10+]` Lead/Architect | Standardized career milestone classification. |
| `company_tier` | `company_name`, `num_of_jobs` | Categorize top hiring volume enterprises vs long-tail employers | Enables comparison of corporate hiring concentration. |

---

### 2.2. Dataset 2: Analytics Jobs (`Analytics Jobs.csv`)

| Target Feature | Source Fields | Transformation Logic | Analytical Rationale |
|---|---|---|---|
| `min_exp` | `experience` | Regex: extract first integer in `'X-Y yrs'` | Minimum required years for the role. |
| `max_exp` | `experience` | Regex: extract second integer in `'X-Y yrs'` | Upper bound of required experience. |
| `midpoint_exp` | `min_exp`, `max_exp` | `(min_exp + max_exp) / 2.0` | Continuous proxy for expected candidate tenure. |
| `salary_band_ord` | `salary` | Ordinal mapping: `0to3` $\rightarrow 1$, `3to6` $\rightarrow 2$, `6to10` $\rightarrow 3$, `10to15` $\rightarrow 4$, `15to25` $\rightarrow 5$, `25to50` $\rightarrow 6$ | Enables non-parametric rank correlation and ordinal modeling. |
| `salary_midpoint` | `salary` | Interval midpoint: `0to3` $\rightarrow 1.5$, `3to6` $\rightarrow 4.5$, `6to10` $\rightarrow 8.0$, `10to15` $\rightarrow 12.5$, `15to25` $\rightarrow 20.0$, `25to50` $\rightarrow 37.5$ | Numerical approximation for wage trend exploration. |
| `is_high_salary` | `salary` | Binary: $1$ if `salary` $\in \{\text{'15to25'}, \text{'25to50'}\}$, else $0$ | Benchmark target for high-compensation odds ratio modeling. |
| `location_metro` | `location` | String match to major tech clusters: Bengaluru, Mumbai, NCR (Delhi/Gurgaon/Noida), Pune, Hyderabad, Chennai, Other | Consolidates 1,355 messy locations into actionable macro talent hubs. |
| `role_family` | `job_desig` | Keyword tagging into: Data Scientist, Data Analyst, Business Analyst, Data Engineer, BI/Dashboard Developer, Other/Non-Data | Filters and standardizes 10,097 free-text titles into structured families. |
| `skill_indicators`| `key_skills` | Multi-hot binary flags for top technical skills (Python, SQL, R, Tableau, PowerBI, Spark, AWS, Machine Learning, Excel) | Enables skill frequency profiling, co-occurrence analysis, and association mining. |
| `skill_count` | `key_skills` | Count of delimited tokens per posting | Measures job breadth and stack complexity demanded by employers. |

---

### 2.3. Dataset 3: Junior Data Scientist Skill Traits (`JDS Skill Traits.xlsx`)

| Target Feature | Source Fields | Transformation Logic | Analytical Rationale |
|---|---|---|---|
| `skills_raw` | All 5 skill columns | **Preserve original 1.0–5.0 ratings untouched** | Preserves original behavioral measurement scale for interpretability. |
| `skills_std` | All 5 skill columns | Z-score standardization: $(X - \mu) / \sigma$ (computed inside CV folds) | Essential for regularized logistic regression (L1/L2 penalty) comparison. |
| `composite_skill_mean`| All 5 skill columns | Arithmetic mean across all 5 skills: $\frac{1}{5}\sum_{j=1}^5 X_j$ | Evaluates if general technical excellence predicts hikes over individual skills. *(Only evaluated if statistically justified)*. |
| `skill_balance_std`| All 5 skill columns | Standard deviation across an individual's 5 skill ratings | Measures specialization vs generalist skill profiles across junior candidates. |

---

### 2.4. Dataset 4: Senior Data Scientist Personality Traits (`SDS Personality Traits.xlsx`)

| Target Feature | Source Fields | Transformation Logic | Analytical Rationale |
|---|---|---|---|
| `traits_raw` | All 5 Big Five columns | **Preserve raw score distributions (17–68)** | Retains the natural scale of the Big Five psychometric assessment. |
| `traits_std` | All 5 Big Five columns | Z-score standardization: $(X - \mu) / \sigma$ (computed inside CV folds) | Enables standardized odds ratio comparison ($\Delta$ odds per 1 standard deviation increase in trait). |
| `emotional_stability`| `neuroticism` | Inverse score: $\text{Max} - \text{Neuroticism}$ (or negative z-score) | Optional reframing to measure positive resilience rather than negative affectivity. |
| `trait_profile_type`| All 5 Big Five columns | **Explicit Rule**: Do NOT create arbitrary personality categories (e.g. "Leader", "Thinker") unless justified by rigorous cluster analysis. | Prevents pseudo-scientific stereotyping. |
