# Statistical Analysis Plan & Inferential Framework (Phase 0)

## 1. Principles of Statistical Inference

Statistical analysis in this project bridges raw exploratory numbers and validated business conclusions. Under SAS Hackathon standards:
1. **Purpose-Driven Testing**: Every test must directly answer an established research question or evaluate a pre-registered hypothesis.
2. **Assumption Verification**: No parametric test will be reported without verifying its underlying assumptions (normality, homoscedasticity, linearity).
3. **Dual Metric Reporting**: Every hypothesis decision must report both inferential significance ($p$-value, adjusted for multiple testing) and substantive effect size (magnitude of practical difference).
4. **Transparent Fallback**: When parametric assumptions are violated, defensible non-parametric alternatives are pre-specified.

---

## 2. Statistical Methods Portfolio

### 2.1. Normality & Distributional Assessment
* **Question Answered**: Are skill scores (JDS) and personality trait scores (SDS) sufficiently normal to justify parametric t-tests and linear models?
* **Variables**: 5 JDS skill scores; 5 SDS Big Five trait scores.
* **Methods**:
  * Formal Test: Shapiro-Wilk test ($\alpha = 0.05$).
  * Visual Diagnostics: Q-Q plots, histogram kernel densities, skewness/kurtosis coefficients.
* **Decision Rule / Fallback**:
  * If $p \ge 0.05$ (normal): Proceed with Student's independent two-sample t-test.
  * If $p < 0.05$ (non-normal, skewed, or ceiling-compressed): Fall back to the non-parametric Mann–Whitney U test.

---

### 2.2. Two-Sample Mean & Median Comparisons
* **Question Answered**: 
  * Do junior data scientists with high salary hikes have significantly higher skill scores than low-hike peers? (RQ6 / H1)
  * Do senior data scientists with high success classification have significantly different personality scores than low-success peers? (RQ7 / H3)
* **Variables**:
  * JDS: Skill ratings across `salary_hike_high_or_low` (0 vs 1).
  * SDS: Personality scores across `success_classification_high_low` (0 vs 1).
* **Methods**:
  * Parametric: Two-sample Student's t-test (with Welch's correction if Levene's test reveals unequal variances, $\sigma_1^2 \neq \sigma_2^2$).
  * Non-parametric Fallback: Two-sample Mann–Whitney U test (Wilcoxon rank-sum test).
  * Multiple Testing Correction: Benjamini-Hochberg False Discovery Rate (FDR) applied across the 5 simultaneous tests in each dataset.
* **Effect Sizes**:
  * Parametric: Cohen’s $d = \frac{\bar{X}_1 - \bar{X}_2}{s_{\text{pooled}}}$ (with 95% confidence intervals). Thresholds: small ($|d| \ge 0.2$), medium ($|d| \ge 0.5$), large ($|d| \ge 0.8$).
  * Non-parametric: Cliff’s $\delta$ or Rank-Biserial correlation $r_{\text{rb}} = 1 - \frac{2U}{n_1 n_2}$.

---

### 2.3. Analysis of Variance (One-Way ANOVA) & Kruskal-Wallis Test
* **Question Answered**: Does average advertised salary vary significantly across the 10 data science job titles and across experience tiers? (RQ1, RQ2)
* **Variables**:
  * Dependent: `avg_salary_lakhs` (from `DataScience Jobs.csv`).
  * Grouping: `job_title` (10 groups), `experience_tier` (4 groups).
* **Assumptions**: Independence of observations, normality of residuals, homogeneity of variance (Levene's test).
* **Decision Rule / Fallback**:
  * If assumptions hold: One-Way ANOVA with Tukey's HSD post-hoc pairwise comparisons.
  * If heteroskedastic / non-normal: Welch’s ANOVA or non-parametric Kruskal-Wallis $H$-test followed by Dunn's post-hoc test with Bonferroni correction.
* **Effect Size**: Eta-squared ($\eta^2$) or Epsilon-squared ($\epsilon^2$).

---

### 2.4. Categorical Association Testing (Chi-Square & Cramér's V)
* **Question Answered**: Is representation in high-tier salary brackets (`15to25`, `25to50` Lakhs) statistically dependent on geographic location or specific skill indicators? (RQ3, RQ5 / H6)
* **Variables**: `salary_tier` (Binary / Ordinal), `location_metro` (Categorical), binary skill indicators (from `Analytics Jobs.csv`).
* **Methods**:
  * Pearson Chi-Square ($\chi^2$) test of independence on $R \times C$ contingency tables.
  * Expected frequency check: Verify expected cell counts $E_{ij} \ge 5$ in at least 80% of cells. If violated, aggregate sparse categories or apply Fisher's Exact Test for $2 \times 2$ tables.
  * Cell Contribution: Standardized adjusted residuals ($z = \frac{O_{ij} - E_{ij}}{\sqrt{E_{ij}(1-p_{i\cdot})(1-p_{\cdot j})}}$); values $|z| > 2.0$ indicate significant local divergence.
* **Effect Size**: Cramér’s $V = \sqrt{\frac{\chi^2}{N \cdot \min(R-1, C-1)}}$. Thresholds: negligible ($< 0.10$), weak ($0.10–0.20$), moderate ($0.20–0.40$), strong ($> 0.40$).

---

### 2.5. Multivariable Binary Logistic Regression
* **Question Answered**: Controlling for all skills simultaneously, which specific technical competencies independently predict junior salary hikes? (RQ6 / H2) Controlling for all traits, which personality dimensions independently predict senior consulting success? (RQ7 / H4)
* **Variables**:
  * Model A (JDS): Dependent = `salary_hike_high_or_low`; Predictors = 5 technical skill dimensions.
  * Model B (SDS): Dependent = `success_classification_high_low`; Predictors = 5 Big Five trait dimensions.
* **Assumptions & Diagnostics**:
  * Binary target with independent observations.
  * Linearity of the logit for continuous variables (Box-Tidwell test).
  * Multicollinearity diagnostic: Variance Inflation Factor ($\text{VIF} < 5.0$ acceptable, $< 2.5$ ideal).
  * Influential observations: Cook’s distance / leverage diagnostics.
* **Metrics & Interpretation**:
  * Parameter coefficients ($\beta_j$), standard errors ($SE$), and Wald $\chi^2$ statistics ($p$-values).
  * Adjusted Odds Ratios: $\text{AOR}_j = \exp(\beta_j)$ with 95% profile-likelihood confidence intervals.
  * Overall Model Fit: Likelihood Ratio $\chi^2$ test, McFadden’s Pseudo-$R^2$, Hosmer-Lemeshow goodness-of-fit test.

---

### 2.6. Correlation Analysis & Linear Association
* **Question Answered**: How strongly does required minimum experience correlate with advertised salary? (RQ2 / H5)
* **Variables**: `min_experience`, `avg_salary_lakhs`, `salary_spread`.
* **Methods**:
  * Parametric: Pearson product-moment correlation coefficient ($r$) with 95% Fisher z-transformed confidence intervals.
  * Non-parametric: Spearman rank-order correlation coefficient ($\rho$) to assess monotonic relationship robust to extreme values.
  * Robust Linear Regression (HC3 standard errors) to estimate marginal wage return per year of experience.
