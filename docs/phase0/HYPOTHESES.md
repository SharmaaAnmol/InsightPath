# Formal Testable Hypotheses (Phase 0)

## 1. Methodological Principles for Hypothesis Testing

In accordance with rigorous statistical practice and the SAS evaluation criteria:
1. **Falsifiability**: Every hypothesis is formulated such that empirical data can reject the alternative hypothesis and fail to reject the null hypothesis.
2. **Pre-Registration**: Formulating hypotheses prior to data cleaning and testing prevents p-hacking and exploratory bias.
3. **Dual Assessment**: Statistical significance ($p$-values) must always be accompanied by measures of **practical significance** (effect sizes such as Cohen’s $d$, odds ratios, Cramér’s $V$, and $R^2$).
4. **Multiple Testing Control**: Where multiple pairwise comparisons are conducted simultaneously (e.g. across 5 skills or 5 personality traits), family-wise error rate or False Discovery Rate (Benjamini-Hochberg FDR) corrections will be applied.

---

## 2. Formal Hypothesis Portfolio

### Hypothesis 1 (H1): Junior Technical Skills and Salary-Hike Likelihood
* **Context**: Investigates whether technical proficiency generally associates with higher salary hike classification among Junior Data Scientists.
* **Null Hypothesis ($H_{0,1}$)**: There is no statistically significant difference in mean technical skill scores between Junior Data Scientists classified as high salary hike ($Y=1$) and those classified as low salary hike ($Y=0$).
  $$\mu_{\text{high}} = \mu_{\text{low}} \quad (\text{for each skill dimension})$$
* **Alternative Hypothesis ($H_{1,1}$)**: Junior Data Scientists classified as high salary hike have statistically significantly higher mean technical skill scores than those classified as low salary hike.
  $$\mu_{\text{high}} > \mu_{\text{low}}$$
* **Variables**:
  * Dependent: `salary_hike_high_or_low` (Binary: 0 vs 1)
  * Independent: `big_data_skills`, `maths-stats_skills`, `coding_skills`, `ai_and_ml_skills`, `dashboard_and_storytelling_skills` (Continuous 1–5 scale)
* **Statistical Method**:
  * Shapiro-Wilk test to assess normality of each skill distribution.
  * If normally distributed: Independent Two-Sample Student's t-test (one-tailed).
  * If non-normal / skewed / ceiling effect: Two-sample Mann–Whitney U test (one-tailed).
  * Effect Size: Cohen's $d$ (parametric) or Cliff's $\delta$ / Rank-Biserial $r$ (non-parametric).
* **Decision Criterion**: Reject $H_0$ if adjusted $p < 0.05$ (using Benjamini-Hochberg FDR at $q = 0.05$).
* **Interpretation Approach**: If rejected, provides empirical evidence that technical competence is positively associated with salary hike advancement within this cohort.

---

### Hypothesis 2 (H2): Differential Impact of Junior Technical Skill Dimensions
* **Context**: Evaluates whether specific technical skill dimensions have distinct, unequal associations with salary-hike classification when evaluated jointly.
* **Null Hypothesis ($H_{0,2}$)**: In a multivariable logistic regression model, all skill coefficients are equal to zero or contribute equally to the odds of a high salary hike.
  $$\beta_{\text{big\_data}} = \beta_{\text{maths\_stats}} = \beta_{\text{coding}} = \beta_{\text{ai\_ml}} = \beta_{\text{storytelling}} = 0$$
* **Alternative Hypothesis ($H_{1,2}$)**: At least one skill dimension exhibits a statistically significant, non-zero partial regression coefficient differing from the others when controlling for all technical dimensions.
  $$\exists j : \beta_j \neq 0$$
* **Variables**:
  * Target: `salary_hike_high_or_low`
  * Predictors: All 5 continuous skill dimensions.
* **Statistical Method**:
  * Multiple Binary Logistic Regression with robust standard errors.
  * Wald $\chi^2$ tests for individual parameter significance.
  * Likelihood Ratio Tests (LRT) comparing reduced models.
  * Diagnostic: Variance Inflation Factor (VIF) to detect multicollinearity among skills.
* **Decision Criterion**: Reject $H_0$ if overall model $\chi^2$ is significant ($p < 0.05$) and at least one skill parameter achieves Wald $p < 0.05$.
* **Interpretation Approach**: If rejected, distinguishes which specific competencies are primary drivers versus secondary correlates of career velocity, identifying "differentiating" vs "baseline" skills.

---

### Hypothesis 3 (H3): Senior Personality Trait Differentiation by Success Classification
* **Context**: Examines whether Big Five personality dimensions show statistically distinguishable distributions between successful and struggling Senior Data Scientists.
* **Null Hypothesis ($H_{0,3}$)**: The distribution of Big Five personality scores is identical between high-success and low-success Senior Data Scientists.
  $$F_{\text{high}}(X_k) = F_{\text{low}}(X_k) \quad \forall k \in \{\text{Neuroticism, Extraversion, Openness, Agreeableness, Conscientiousness}\}$$
* **Alternative Hypothesis ($H_{1,3}$)**: High-success Senior Data Scientists exhibit statistically significantly different distributions in at least one Big Five personality trait compared to low-success peers.
  $$\exists k : F_{\text{high}}(X_k) \neq F_{\text{low}}(X_k)$$
* **Variables**:
  * Dependent: `success_classification_high_low` (Binary: 0 vs 1)
  * Independent: `neuroticism`, `extraversion`, `openness_to_experience`, `agreeableness`, `conscientiousness` (Continuous raw scores 17–68)
* **Statistical Method**:
  * Two-sample independent t-test (or Mann–Whitney U test if distributional assumptions fail).
  * Two-tailed testing across all 5 traits.
  * P-value adjustment: Benjamini-Hochberg FDR correction across the 5 tests.
  * Effect Size: Standardized mean difference (Cohen’s $d$ with 95% confidence intervals).
* **Decision Criterion**: Reject $H_0$ if adjusted $p < 0.05$ and $|d| \ge 0.30$ (minimum meaningful behavioral effect size).
* **Interpretation Approach**: If rejected, identifies behavioral traits that empirically differentiate senior customer-facing practitioners.

---

### Hypothesis 4 (H4): Directional Trait Contributions in Senior Success Modeling
* **Context**: Analyzes the specific directional contributions of Conscientiousness, Extraversion, and Neuroticism in senior consulting success.
* **Null Hypothesis ($H_{0,4}$)**: Individual personality trait odds ratios in a joint logistic model do not differ significantly from 1.0.
  $$\text{OR}_k = \exp(\beta_k) = 1.0 \quad \forall k$$
* **Alternative Hypothesis ($H_{1,4}$)**: Conscientiousness and Extraversion are positively associated ($\text{OR} > 1.0$), while Neuroticism is negatively associated ($\text{OR} < 1.0$), with high success classification in customer-facing analytics roles.
* **Variables**:
  * Dependent: `success_classification_high_low`
  * Predictors: Big Five standardized continuous scores.
* **Statistical Method**:
  * Multivariable Logistic Regression.
  * Evaluation of Adjusted Odds Ratios ($\text{AOR}$) and 95% profile likelihood confidence intervals.
  * Receiver Operating Characteristic (ROC-AUC) curve evaluation via cross-validation.
* **Decision Criterion**: Reject $H_0$ if 95% confidence intervals for respective odds ratios exclude 1.0 ($\text{CI} \not\ni 1.0$).
* **Interpretation Approach**: Translates psychological profiles into practical behavioral implications for senior client-facing performance.

---

### Hypothesis 5 (H5): Experience-to-Compensation Elasticity in Market Data
* **Context**: Examines whether required minimum years of experience exhibits a statistically significant positive relationship with advertised salary in data science postings.
* **Null Hypothesis ($H_{0,5}$)**: There is no correlation between required minimum experience and average advertised salary ($\rho = 0, \beta_1 = 0$).
* **Alternative Hypothesis ($H_{1,5}$)**: Minimum experience is positively and significantly correlated with average advertised salary ($\rho > 0, \beta_1 > 0$).
* **Variables**:
  * Dependent: `avg_salary` (Continuous numeric Lakhs INR)
  * Independent: `min_experience` (Continuous numeric years)
* **Statistical Method**:
  * Pearson linear correlation ($r$) and Spearman rank correlation ($\rho$).
  * Ordinary Least Squares (OLS) bivariate regression with heteroskedasticity-robust standard errors (HC3).
* **Decision Criterion**: Reject $H_0$ if $p < 0.001$ and $r \ge 0.20$.
* **Interpretation Approach**: If rejected, confirms and quantifies the economic value of professional experience in data science recruitment.

---

### Hypothesis 6 (H6): Geographic and Skill Categorical Independence in Analytics Roles
* **Context**: Evaluates whether demand for high-tier salary brackets (`15to25`, `25to50` Lakhs) is independent of geographic hiring hub and specialized technical skills.
* **Null Hypothesis ($H_{0,6}$)**: High-tier salary classification is statistically independent of geographic hiring location and specialized skill presence.
* **Alternative Hypothesis ($H_{1,6}$)**: High-tier salary classification is significantly associated with specific geographic hubs (e.g., Bengaluru, Gurgaon) and advanced skills (e.g., Cloud, Advanced ML).
* **Variables**:
  * Categorical Variables: `salary_tier` (Binary: High $\ge 15\text{L}$ vs Standard $< 15\text{L}$), `location_cluster` (Top metro hubs), `skill_flag` (Presence of key skills).
* **Statistical Method**:
  * Pearson Chi-Square ($\chi^2$) test of independence.
  * Cramér's $V$ for categorical association strength.
  * Adjusted standardized residuals for cell-level post-hoc contribution.
* **Decision Criterion**: Reject $H_0$ if $\chi^2$ test $p < 0.01$ and Cramér's $V \ge 0.10$.
* **Interpretation Approach**: If rejected, confirms regional wage premiums and high-value skill clusters in the analytics job market.
