# Model Interpretability & Explainability Plan (Phase 0)

## 1. Principles of Model Explainability

In high-stakes talent analytics and career research:
1. **Explanation Over Pure Accuracy**: A marginally more accurate black-box model (e.g. +0.02 ROC-AUC) that cannot explain *why* it predicts an outcome is analytically inferior to a transparent model that provides clear, defensible decision boundaries.
2. **Prediction vs. Explanation**: We explicitly distinguish between **predictive association** (the model's capacity to classify holdout records) and **explanatory inference** (identifying underlying domain factors associated with career velocity).
3. **Non-Causal Guardrails**: Interpretations must be framed in associational terms ("associated with an observed increase in odds") rather than causal assertions ("improving coding skill causes a salary hike").

---

## 2. Multi-Level Interpretability Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                GLOBAL INTERPRETABILITY                       │
│  (What general rules and factors govern the whole population?)│
└──────────────────────────────┬───────────────────────────────┘
                               │
       ┌───────────────────────┴───────────────────────┐
       ▼                                               ▼
[PARAMETRIC / LINEAR]                         [NON-LINEAR / TREE]
• Logistic Regression Coefficients            • Decision Tree Visual Paths
• Odds Ratios (OR) with 95% CIs               • MDI Feature Importance
• Forest plots of factor weights              • Permutation Importance
                               │
┌──────────────────────────────▼───────────────────────────────┐
│                 LOCAL INTERPRETABILITY                       │
│  (Why was a specific individual classified as High or Low?)  │
└──────────────────────────────┬───────────────────────────────┘
                               │
       ┌───────────────────────┴───────────────────────┐
       ▼                                               ▼
[DECISION RULES]                              [CONTRIBUTION PLOTS]
• Exact path traversal:                       • Waterfall / SHAP plots
  "If Big Data > 4.2 & Storytelling > 4.5..." • Individual force breakdowns
```

---

## 3. Detailed Interpretability Methods by Algorithm

### 3.1. Logistic Regression: Odds Ratios & Margin Plots
* **Mechanism**: In a logistic regression model $\ln\left(\frac{p}{1-p}\right) = \beta_0 + \sum_{j=1}^5 \beta_j X_j$, each slope coefficient $\beta_j$ represents the change in log-odds of the positive class per unit increase in $X_j$.
* **Primary Interpretability Artifacts**:
  * **Adjusted Odds Ratios ($\text{AOR}_j = \exp(\beta_j)$)**: Quantifies the multiplicative increase in odds of a high hike (JDS) or consulting success (SDS).
  * **95% Confidence Intervals**: Displayed via a horizontal **Odds Ratio Forest Plot** centered at $\text{OR} = 1.0$. Features whose confidence intervals cross $1.0$ are highlighted as statistically non-differentiating.
  * **Marginal Effects**: Average Marginal Effects (AME) reporting the percentage point change in predicted probability ($\frac{\partial p}{\partial X_j}$).

### 3.2. Decision Trees: Transparent Rule Extraction
* **Mechanism**: CART trees recursively partition the feature space based on Gini impurity or entropy reduction.
* **Primary Interpretability Artifacts**:
  * **Visual Tree Diagrams**: Rendered decision trees (constrained to depth $\le 3$) displaying split thresholds (e.g. `coding_skills <= 3.8`), sample counts per node, and class probabilities.
  * **Rule Set Export**: Plain-text human-readable decision rules:
    > *Rule 1*: IF `ai_and_ml_skills > 4.5` AND `dashboard_and_storytelling_skills > 4.2` THEN Probability of High Hike = 82% ($N = 45$).
    > *Rule 2*: IF `conscientiousness > 48` AND `neuroticism < 35` THEN Probability of Consulting Success = 79% ($N = 52$).
  * **Threshold Benchmarks**: Identification of natural "threshold gates" that separate low from high outcomes.

### 3.3. Random Forest: Impurity vs. Permutation Importance
* **Mechanism**: Ensembles aggregate hundreds of trees, obscuring direct visual rules. We deploy two complementary importance measures:
  * **Mean Decrease in Impurity (MDI / Gini Importance)**: Measures the total reduction in node impurity brought by each feature across all trees. *(Caveat: Can favor high-cardinality continuous features; used as secondary benchmark)*.
  * **Permutation Feature Importance (PFI)**: Evaluates the decrease in model ROC-AUC / F1-Score when a specific feature's values are randomly shuffled on validation folds. Features causing severe performance drops upon shuffling are confirmed as critical predictive drivers.
* **Primary Interpretability Artifact**:
  * Paired Bar Chart comparing MDI vs. Permutation Importance rankings with standard error bars.

### 3.4. SHAP (SHapley Additive exPlanations)
* **Mechanism**: Grounded in cooperative game theory, SHAP computes the marginal contribution of each feature to the difference between individual prediction and baseline expected value.
* **Deployment Scope**:
  * Deployed selectively on champion models to generate:
    * **SHAP Summary Beeswarm Plots**: Revealing both feature importance ranking and the directional effect (e.g. high feature values driving positive vs negative impact).
    * **Representative Local Waterfall Plots**: Showing typical persona archetypes (e.g. "The High-Hike Specialist", "The Struggling Senior").

---

## 4. Ethical & Analytical Guardrails in Interpretation

1. **JDS Skill Model**:
   * Distinguish between **"Threshold Skills"** (features where everyone has high ratings, such that a low rating hurts, but high rating does not guarantee a hike) and **"Differentiating Skills"** (features that cleanly separate high-hike from low-hike individuals).
2. **SDS Personality Model**:
   * **Absolute Prohibition on Determinism**: A low conscientiousness score or high neuroticism score does **not** determine individual professional failure. It identifies potential vulnerability areas for coaching, stress management, and mentorship.
   * Trait findings must be interpreted strictly within the context of **senior, customer-facing consulting environments**, where client interaction, ambiguity management, and deadline pressure are magnified.
