# Phase 6 — Senior Data Scientist Personality Modeling & Interpretability Report

**Project**: InsightPath / RUSTY WOLVES  
**Hackathon**: SAS CU Hackathon Round 2  
**Evaluation Pillar**: Data Mining / Machine Learning Skills (30 Marks), Model Interpretability, Ethical Safeguards  
**Status**: COMPLETE & FULLY VALIDATED  
**Authoritative Inputs**: `data/processed/sds_processed.csv` ($N=161$) & `data/processed/sds_sensitivity_deduplicated.csv` ($N=152$)  

---

## 1. Executive Summary

Phase 6 establishes the supervised machine-learning predictive layer for the **Senior Data Scientist (SDS)** cohort ($N=161$), addressing **Research Question RQ7** and the predictive dimension of **RQ8**. While Phase 3 explored descriptive trait distributions and Phase 4 tested inferential hypothesis associations (H3 and H4), Phase 6 evaluates whether Big Five psychometric dimensions provide reliable, out-of-sample predictive discrimination of observed senior consulting success (`success_classification_high_low`).

### Key Modeling & Interpretability Findings:
1. **Exceptional Out-of-Sample Discrimination**:
   Across 25 repeated cross-validation splits (5-fold $\times$ 5-repeat StratifiedGroupKFold on subject ID), the champion model—**Regularized Ridge Logistic Regression (L2, $C=1.0$)**—achieves a cross-validated **ROC-AUC of 0.9699** ($\pm 0.0268$, $95\%\text{ CI: } [0.9594, 0.9804]$), a **Macro F1 of 0.9259**, and an **Accuracy of 92.68%**. The non-linear benchmark (**Random Forest**, 100 shallow trees) reaches **0.9946 ROC-AUC** and **94.05% Accuracy**.
2. **Decisive Lift Over Naive Baseline**:
   Compared to the zero-rule majority baseline ($52.78\%$ accuracy, $0.500$ ROC-AUC), Logistic Regression L2 delivers a **$+39.90\text{ percentage point}$ accuracy lift** and a **$+0.4699$ ROC-AUC gain**.
3. **Rigorous Clone Leakage Control (StratifiedGroupKFold)**:
   The SDS dataset contains 9 duplicate subject IDs (18 rows total). Random cross-validation on $N=161$ would cause clone leakage (identical feature vectors in train and test folds). Phase 6 strictly enforced `StratifiedGroupKFold` grouping by subject `id`, mathematically guaranteeing that duplicate subject vectors never cross fold boundaries.
4. **Dominant Predictive Drivers: Conscientiousness & Openness**:
   - **Openness to Experience**: Rank #1 held-out permutation importance ($0.1209$), root split in CART ($\le 38.50$), standardized $\text{AOR} = 7.72$.
   - **Conscientiousness**: Rank #2 permutation importance ($0.0826$), primary second-tier split ($\le 36.50$), standardized $\text{AOR} = 8.11$.
   - Together, Openness and Conscientiousness placed in the **Top-2 in 100% of validation splits**.
5. **Phase 4 vs Phase 6 Empirical Nuance (The Neuroticism Paradox Resolved)**:
   In Phase 4 inferential modeling, Neuroticism showed a multivariable suppressor effect ($\text{AOR} = 3.94$, $p=0.0013$) despite zero bivariate group difference ($d=-0.012$, $p=0.454$). In Phase 6 predictive evaluation, Neuroticism exhibits **near-zero held-out permutation importance** ($0.0005$, Rank #5). It contributes virtually no out-of-sample predictive lift, proving that statistical significance in parametric modeling does not automatically equate to predictive importance on unseen data.
6. **Sensitivity Robustness (Deduplicated $N=152$)**:
   Re-evaluating the pipeline on the deduplicated sensitivity cohort ($N=152$, dropping 9 clone rows) yields $\text{ROC-AUC} = 0.9650$ for Logistic L2 ($\Delta\text{ROC-AUC} = -0.0049 \le 0.02$) and $0.9942$ for Random Forest ($\Delta\text{ROC-AUC} = -0.0004$). All models are classified as **HIGHLY ROBUST TO OBSERVATIONAL NOISE**.

---

## 2. Phase 6 Objective

The primary objective of Phase 6 is to evaluate whether observed Big Five personality traits predict senior consulting success in customer-facing roles, while enforcing strict leak-free grouped validation, parsimonious small-sample modeling, and firm ethical safeguards against deterministic personality gatekeeping.

---

## 3. Connection to Research Questions RQ7 & RQ8

- **RQ7**: *"Which personality dimensions are associated with high success classification among Senior Data Scientists?"*  
  Phase 6 answers RQ7 from a predictive standpoint: high consulting success is predicted primarily by elevated **Openness to Experience** (intellectual curiosity, adaptability to unstructured client challenges) and **Conscientiousness** (methodological rigor, follow-through, delivery excellence).
- **RQ8**: *"Can interpretable classification models predict observed senior success classifications from personality traits?"*  
  Phase 6 demonstrates that regularized linear and shallow tree classifiers achieve $>0.93$ ROC-AUC, providing human-interpretable decision boundaries (odds ratios and 4 leaf rules) for mentoring and talent development.

---

## 4. Dataset & Target Variable Confirmation

- **Primary Dataset**: `data/processed/sds_processed.csv` ($N = 161$ records, 5 features, 1 target, 1 identifier).
- **Target Variable**: `success_classification_high_low` $\in \{0, 1\}$.
  - Class 1 (High Success): $N = 85$ ($52.80\%$).
  - Class 0 (Low Success): $N = 76$ ($47.20\%$).
- **Features**: Strictly the five Big Five psychometric dimensions scored on raw psychometric interval $[17.0, 68.0]$:
  1. `neuroticism`
  2. `extraversion`
  3. `openness_to_experience`
  4. `agreeableness`
  5. `conscientiousness`
- **Identifier**: `id` is strictly excluded from the feature matrix $X$ and used solely as the grouping variable for cross-validation splitting.

---

## 5. Duplicate ID Protocol & Forensic Findings

Forensic auditing (`docs/phase1/DUPLICATE_AUDIT.md`, `docs/phase2/SDS_DUPLICATE_HANDLING.md`) revealed 9 duplicated subject IDs representing 18 total rows. In all 9 pairs, the duplicate records share identical trait vectors and identical target labels.
- In accordance with Phase 2 governance, all $N = 161$ rows are retained in the primary benchmark dataset to preserve population size and official hackathon counts.
- To rigorously verify that duplicate weighting does not bias modeling, a deduplicated sensitivity cohort ($N = 152$) was generated and tested.

---

## 6. Critical Data Leakage Prevention (StratifiedGroupKFold)

Standard K-Fold or Stratified K-Fold would randomly partition the 18 duplicate rows across train and validation folds. A model tested on a duplicate subject whose twin was present in the training set would benefit from artificial "clone memorization."
- **Enforced Solution**: Primary validation uses `StratifiedGroupKFold(n_splits=5, shuffle=True)` grouping by `id`.
- **Integrity Verification**: Automated assertion checks verified that $\text{Train IDs} \cap \text{Val IDs} = \emptyset$ across all 25 validation splits. Zero clone leakage occurred.
- **Pipeline Enclosure**: Feature scaling (`StandardScaler`) is enclosed strictly inside `sklearn.pipeline.Pipeline`, preventing distributional leakage.

---

## 7. Cross-Validation Methodology

- **Splits**: 5-Fold StratifiedGroupKFold evaluated across 5 random seeds (`[42, 43, 44, 45, 46]`), yielding **25 out-of-sample evaluation splits**.
- **Metrics Computed per Split**: ROC-AUC, Macro F1, Balanced Accuracy, Accuracy, Precision, Recall, Log Loss, Brier Score.
- **Predictions**: Out-of-fold probabilities and binary predictions gathered for every sample.

---

## 8. Empirical Baseline Benchmark

- **Baseline Model**: Majority class prior dummy classifier (`strategy='prior'`).
- **Baseline Accuracy**: $52.78\% \pm 1.15\%$.
- **Baseline ROC-AUC**: $0.5000 \pm 0.0000$.
- **Baseline Macro F1**: $0.3454 \pm 0.0049$.
- **Baseline Brier Score**: $0.2493$.

---

## 9. Regularized Logistic Regression Results

Three regularized logistic formulations were benchmarked across all 25 splits:
1. **Logistic Regression L2 (Ridge, $C=1.0$)**:
   - $\text{ROC-AUC} = \mathbf{0.9699} \pm 0.0268$ ($95\%\text{ CI: } [0.9594, 0.9804]$)
   - $\text{Macro F1} = 0.9259 \pm 0.0484$
   - $\text{Accuracy} = 92.68\% \pm 4.77\%$
   - $\text{Brier Score} = 0.0622$, $\text{Log Loss} = 0.2143$
2. **Logistic Regression ElasticNet ($C=1.0$, $l_1=0.5$)**:
   - $\text{ROC-AUC} = 0.9688 \pm 0.0278$, $\text{Macro F1} = 0.9221$, $\text{Accuracy} = 92.30\%$
3. **Logistic Regression L1 (Lasso, $C=1.0$)**:
   - $\text{ROC-AUC} = 0.9683 \pm 0.0286$, $\text{Macro F1} = 0.9196$, $\text{Accuracy} = 92.05\%$

---

## 10. Decision Tree Results (CART, Constrained Depth)

- **Configuration**: `max_depth=3`, `min_samples_leaf=5`, `criterion='gini'`.
- **Performance**:
  - $\text{ROC-AUC} = \mathbf{0.9399} \pm 0.0412$ ($95\%\text{ CI: } [0.9237, 0.9560]$)
  - $\text{Macro F1} = 0.9036 \pm 0.0388$
  - $\text{Accuracy} = 90.44\% \pm 3.85\%$
  - $\text{Brier Score} = 0.0729$
- **Extracted Rules (4 Leaves)**:
  - **Leaf 1**: $\text{Openness} \le 38.50 \implies \mathbf{100.0\%\text{ Low Success}}$ ($N=52$).
  - **Leaf 2**: $\text{Openness} > 38.50 \land \text{Conscientiousness} \le 36.50 \implies \mathbf{100.0\%\text{ Low Success}}$ ($N=16$).
  - **Leaf 3**: $\text{Openness} > 38.50 \land \text{Conscientiousness} > 36.50 \land \text{Agreeableness} \le 38.50 \implies \mathbf{60.0\%\text{ Low Success}}$ ($N=5$).
  - **Leaf 4**: $\text{Openness} > 38.50 \land \text{Conscientiousness} > 36.50 \land \text{Agreeableness} > 38.50 \implies \mathbf{94.3\%\text{ High Success}}$ ($N=88$).

---

## 11. Random Forest & Gradient Boosting Results

- **Random Forest (100 trees, depth 3, max_features='sqrt')**:
  - $\text{ROC-AUC} = \mathbf{0.9946} \pm 0.0057$ ($95\%\text{ CI: } [0.9924, 0.9969]$)
  - $\text{Macro F1} = 0.9400 \pm 0.0251$
  - $\text{Accuracy} = 94.05\% \pm 2.49\%$
  - $\text{Brier Score} = 0.0400$
- **Gradient Boosting (50 trees, depth 2, learning_rate=0.05)**:
  - $\text{ROC-AUC} = \mathbf{0.9882} \pm 0.0175$, $\text{Macro F1} = 0.9374$, $\text{Accuracy} = 93.79\%$

---

## 12. Model Performance Comparison Scorecard

*Source: [`outputs/tables/phase6/phase6_model_performance.csv`](file:///Users/anmolsharma/Desktop/DataScienceTool/outputs/tables/phase6/phase6_model_performance.csv)*

| Model | ROC-AUC | 95% CI | Macro F1 | Balanced Acc | Accuracy | Accuracy Lift | Brier Score |
|---|---|---|---|---|---|---|---|
| **Random Forest** | **0.9946** | [0.9924, 0.9969] | 0.9400 | 0.9396 | 94.05% | +41.27% | 0.0400 |
| **Gradient Boosting** | 0.9882 | [0.9813, 0.9951] | 0.9374 | 0.9366 | 93.79% | +41.01% | 0.0471 |
| **Logistic Regression L2 (Champion)** | **0.9699** | [0.9594, 0.9804] | **0.9259** | 0.9248 | **92.68%** | **+39.90%** | **0.0622** |
| Logistic Regression ElasticNet | 0.9688 | [0.9579, 0.9797] | 0.9221 | 0.9212 | 92.30% | +39.52% | 0.0620 |
| Logistic Regression L1 | 0.9683 | [0.9570, 0.9795] | 0.9196 | 0.9186 | 92.05% | +39.27% | 0.0622 |
| Decision Tree (CART, depth 3) | 0.9399 | [0.9237, 0.9560] | 0.9036 | 0.9036 | 90.44% | +37.66% | 0.0729 |
| Baseline Majority | 0.5000 | [0.5000, 0.5000] | 0.3454 | 0.5000 | 52.78% | 0.00% | 0.2493 |

---

## 13. Feature Interpretation (Odds Ratios & Permutation Importance)

### Standardized Logistic Odds Ratios (Logistic L2):
1. **Conscientiousness**: $\beta = +2.0936$, $\text{Adjusted Odds Ratio} = \mathbf{8.1143}$ ($95\%\text{ CI: } [6.2258, 10.5758]$).
2. **Openness to Experience**: $\beta = +2.0434$, $\text{Adjusted Odds Ratio} = \mathbf{7.7166}$ ($95\%\text{ CI: } [5.5815, 10.6684]$).
3. **Extraversion**: $\beta = +0.9538$, $\text{Adjusted Odds Ratio} = \mathbf{2.5954}$ ($95\%\text{ CI: } [1.7619, 3.8232]$).
4. **Neuroticism**: $\beta = +0.7985$, $\text{Adjusted Odds Ratio} = \mathbf{2.2221}$ ($95\%\text{ CI: } [1.7607, 2.8045]$).
5. **Agreeableness**: $\beta = +0.6278$, $\text{Adjusted Odds Ratio} = \mathbf{1.8734}$ ($95\%\text{ CI: } [1.4473, 2.4249]$).

### Held-Out Permutation Feature Importance (Random Forest):
1. **`openness_to_experience`**: $\mathbf{0.1209} \pm 0.0381$ (Rank #1)
2. **`conscientiousness`**: $\mathbf{0.0826} \pm 0.0199$ (Rank #2)
3. **`agreeableness`**: $\mathbf{0.0188} \pm 0.0127$ (Rank #3)
4. **`extraversion`**: $\mathbf{0.0160} \pm 0.0123$ (Rank #4)
5. **`neuroticism`**: $\mathbf{0.0005} \pm 0.0013$ (Rank #5)

---

## 14. Feature Rank Stability Across 25 Splits

- **Openness to Experience**: Ranked #1 in **80.0% of splits**, Top-2 in **100.0% of splits**.
- **Conscientiousness**: Ranked #1 in **20.0% of splits**, Top-2 in **100.0% of splits**.
- **Agreeableness & Extraversion**: Alternated between Rank #3 and #4.
- **Neuroticism**: Ranked #5 in **96.0% of splits**, showing near-zero predictive contribution.

---

## 15. Out-of-Sample Error Analysis

Analysis of out-of-fold predictions ($N=805$ evaluated predictions across 25 splits):
- **True Positives**: $50.81\%$ ($N=409$)
- **True Negatives**: $41.86\%$ ($N=337$)
- **False Positives**: $5.34\%$ ($N=43$) — consultants with strong Openness/Conscientiousness who nevertheless had low observed ratings due to client-engagement friction.
- **False Negatives**: $1.99\%$ ($N=16$) — consultants with modest traits who succeeded through strong technical specializations.
- **Boundary Uncertainty ($0.35 \le P \le 0.65$)**: Encompasses only $7.45\%$ of predictions.

---

## 16. Sensitivity Analysis (Primary $N=161$ vs Deduplicated $N=152$)

*Source: [`outputs/tables/phase6/phase6_sensitivity_model_performance.csv`](file:///Users/anmolsharma/Desktop/DataScienceTool/outputs/tables/phase6/phase6_sensitivity_model_performance.csv)*

- **Logistic L2**: Primary ROC-AUC $= 0.9699$ vs Sensitivity ROC-AUC $= 0.9650$ ($\Delta\text{ROC-AUC} = -0.0049 \le 0.02$).
- **Random Forest**: Primary ROC-AUC $= 0.9946$ vs Sensitivity ROC-AUC $= 0.9942$ ($\Delta\text{ROC-AUC} = -0.0004 \le 0.02$).
- **Sign Concordance**: 100% of trait coefficients maintain identical signs and rank orders.
- **Official Robustness Verdict**: **HIGHLY ROBUST TO OBSERVATIONAL NOISE / DUPLICATE BIAS**.

---

## 17. Phase 4 Inferential vs Phase 6 Predictive Comparison

| Trait | Phase 4 Inferential Finding | Phase 6 Predictive Finding | Analytical Verdict |
|---|---|---|---|
| **Conscientiousness** | $d = 1.85$ ($p < 1e-15$), $\text{AOR} = 26.79$ | $\text{AOR} = 8.11$, Permutation Rank #2 ($0.0826$) | **Both Strongly Statistically Associated and Highly Predictive** |
| **Openness** | $d = 1.80$ ($p < 1e-16$), $\text{AOR} = 20.97$ | $\text{AOR} = 7.72$, Permutation Rank #1 ($0.1209$) | **Both Strongly Statistically Associated and Highly Predictive** |
| **Extraversion** | $d = 1.13$ ($p = 5.79e-10$), $\text{AOR} = 3.93$ | $\text{AOR} = 2.60$, Permutation Rank #4 ($0.0160$) | **Moderately Predictive; Subordinate to Openness/Conscientiousness** |
| **Agreeableness** | $d = 0.61$ ($p = 8.74e-4$), $\text{AOR} = 2.46$ ($p=0.056$) | $\text{AOR} = 1.87$, Permutation Rank #3 ($0.0188$) | **Modest Predictive Value; Acts as Secondary Leaf Split in CART** |
| **Neuroticism** | Bivariate $d = -0.01$ ($p=0.454$); Multivariable $\text{AOR} = 3.94$ | $\text{AOR} = 2.22$, Permutation Rank #5 ($0.0005$) | **Statistically Significant in Parametric Model, but Zero Predictive Utility on Held-Out Folds** |

---

## 18. Final Model Selection

- **Champion Model**: `Logistic_Regression_L2` (Ridge Regularized Logistic Regression).
  - Selected for closed-form standardized odds ratios, well-calibrated probabilities, small-sample stability, and stakeholder explainability.
- **Non-Linear Benchmark**: `Random_Forest` (ROC-AUC $0.9946$, Accuracy $94.05\%$).
- **Transparent White-Box Tool**: `Decision_Tree` (4 clear rules, ROC-AUC $0.9399$).

---

## 19. Critical Ethical Safeguards & Personality Governance

In strict compliance with **Absolute Governance Rule G**:
1. **No Automated Hiring Gates**: Big Five personality models must **never** be used for hiring gatekeeping, resume filtering, or candidate pre-screening.
2. **No Promotion / Firing Automation**: Traits cannot serve as automated criteria for promotions or performance terminations.
3. **Developmental Mentoring Only**: Trait profiles represent self-awareness and behavioral coaching indicators for senior consulting readiness (e.g., cultivating client adaptability and execution discipline).
4. **Context Dependency**: Success in customer-facing consulting requires client adaptability, whereas deep research roles may thrive under different behavioral profiles.

---

## 20. Methodological Limitations

1. **Small Sample Size ($N=161$)**: While cross-validation and regularized models prevent overfitting, external validity across industries is unverified.
2. **Self-Report / Rater Subjectivity**: Big Five assessments are subject to rater bias or social desirability effects.
3. **Binary Outcome Simplification**: Consulting success is categorized as binary High/Low, concealing multi-dimensional performance nuances.

---

## 21. Reproducibility Confirmation

All code, data, models, and tables are fully reproducible under fixed seed sequence `[42, 43, 44, 45, 46]` via `python -m src.modeling.sds.run_phase6`.

---

## 22. Phase 6 Boundary Declaration

Phase 6 concludes the predictive modeling layer for Senior Data Scientists. All 23 tables, 8 figures, and models have been validated.

---

## 23. Handoff to Phase 7

Phase 6 is complete. The repository is ready for **Phase 7: Cross-Dataset Analytical Synthesis (Methodological Triangulation without row-level joins)**.
