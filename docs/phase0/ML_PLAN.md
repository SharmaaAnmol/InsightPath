# Machine Learning Plan & Validation Strategy (Phase 0)

## 1. Machine Learning Philosophy & Context

In accordance with the SAS Hackathon briefing:
* **Purpose Over Complexity**: Machine learning is not deployed for its own sake or to chase marginal decimal gains in unvalidated accuracy. It serves a precise analytical purpose: to test whether observed junior salary hikes and senior consulting success can be reliably predicted from skill and personality profiles, and to extract interpretable decision boundaries.
* **Small Sample Discipline**: With valid samples of $N = 139$ (JDS) and $N = 161$ (SDS), hyper-parameterized "black-box" deep learning or complex ensembles are methodologically inappropriate and prone to catastrophic overfitting.
* **Interpretability as a First-Class Citizen**: Models must be explainable to enterprise stakeholders, HR leaders, and academic administrators.

---

## 2. Supervised Learning Tasks Specification

### 2.1. Task A: Junior Data Scientist Salary-Hike Classification
* **Dataset**: `JDS Skill Traits.xlsx` ($N = 139$ valid observations)
* **Target Variable**: `salary_hike_high_or_low` $\in \{0, 1\}$
  * Class 1 (High Hike): 73 instances (52.5%)
  * Class 0 (Low Hike): 66 instances (47.5%)
* **Feature Set ($p = 5$)**:
  * $X_1$: `big_data_skills`
  * $X_2$: `maths-stats_skills`
  * $X_3$: `coding_skills`
  * $X_4$: `ai_and_ml_skills`
  * $X_5$: `dashboard_and_storytelling_skills`
* **Baseline Benchmark**: Zero-Rule / Majority Class Classifier ($\text{Accuracy} = 52.5\%$, $\text{ROC-AUC} = 0.500$).

### 2.2. Task B: Senior Data Scientist Success Classification
* **Dataset**: `SDS Personality Traits.xlsx` ($N = 161$ observations)
* **Target Variable**: `success_classification_high_low` $\in \{0, 1\}$
  * Class 1 (High Success): 85 instances (52.8%)
  * Class 0 (Low Success): 76 instances (47.2%)
* **Feature Set ($p = 5$)**:
  * $X_1$: `neuroticism`
  * $X_2$: `extraversion`
  * $X_3$: `openness_to_experience`
  * $X_4$: `agreeableness`
  * $X_5$: `conscientiousness`
* **Baseline Benchmark**: Zero-Rule / Majority Class Classifier ($\text{Accuracy} = 52.8\%$, $\text{ROC-AUC} = 0.500$).

---

## 3. Candidate Model Architectures

For both classification tasks, four candidate algorithms representing distinct inductive biases will be systematically trained and evaluated:

```
[ MODEL 1: Logistic Regression ] ──► Linear, Parametric, Log-Odds Interpretable
[ MODEL 2: Decision Tree ]       ──► Non-Linear, Rule-Based, Threshold Visible
[ MODEL 3: Random Forest ]       ──► Bagging Ensemble, Variance Reducing
[ MODEL 4: Gradient Boosting ]   ──► Boosting Benchmark (Strict Regularization)
```

| Model Family | Algorithm Specification | Primary Hyperparameters to Constrain | Justification & Expected Role |
|---|---|---|---|
| **Linear Parametric** | Logistic Regression (L1 Lasso / L2 Ridge / ElasticNet) | Regularization strength $C \in [0.01, 10.0]$; penalty $\in \{\text{'l1'}, \text{'l2'}\}$ | Serves as the primary interpretable baseline. Extracts odds ratios and evaluates linear separability. |
| **Rule-Based Non-Linear** | Decision Tree Classifier (CART) | `max_depth` $\in [2, 4]$; `min_samples_leaf` $\ge 5$; `criterion` $\in \{\text{'gini'}, \text{'entropy'}\}$ | Extracts transparent "if-then" decision pathways for career mentoring. |
| **Ensemble Bagging** | Random Forest Classifier | `n_estimators` $= 100$; `max_depth` $\in [3, 5]$; `min_samples_split` $\ge 6$; `max_features` $\in [\sqrt{p}, p]$ | Non-linear benchmark that handles feature interactions and reduces variance without extreme overfitting. |
| **Ensemble Boosting** | LightGBM / Gradient Boosting | `n_estimators` $\le 50$; `learning_rate` $\in [0.03, 0.1]$; `max_depth` $\le 3$ | Evaluates if sequential boosting yields superior discrimination; monitored closely for overfitting. |

---

## 4. Resampling & Cross-Validation Strategy

Given the sample sizes ($N \approx 140 - 160$), a single train/test split (e.g. 80/20) leaves only ~28 test samples, resulting in high variance and unreliable performance estimates depending on the random split seed.

### 4.1. Resampling Protocol
* **Primary Evaluation Scheme**: **Repeated Stratified K-Fold Cross-Validation** (5 Folds $\times$ 5 Repeats = 25 evaluation splits).
  * Stratification ensures identical target class ratios (~53:47) across every fold.
  * 5 repeats provide empirical confidence intervals (mean $\pm$ standard error) for all performance metrics.
* **Holdout Validation**: Optional stratified 80/20 train/test split fixed with a pre-registered random seed (`random_state=42`) used solely for final model illustration and confusion matrix display.

### 4.2. Leakage Prevention Protocol
* All preprocessing steps—including Z-score standardization (`StandardScaler`) and any imputation—are embedded inside `sklearn.pipeline.Pipeline` objects.
* Pipeline parameters are fit strictly on training folds and applied out-of-fold to validation data, preventing data leakage.

---

## 5. Evaluation Metrics Portfolio

No model will be selected purely on Accuracy. Evaluation uses a balanced suite of metrics:

| Metric | Business & Statistical Meaning | Selection Weight |
|---|---|---|
| **ROC-AUC** | Area Under the Receiver Operating Characteristic curve; measures overall ranking discrimination independent of threshold. | High (Primary discrimination metric) |
| **F1-Score (Macro & Weighted)**| Harmonic mean of Precision and Recall; penalizes unbalanced classification errors. | High (Primary balance metric) |
| **Balanced Accuracy** | Average of recall obtained on each class; robust to minor imbalances. | High |
| **Precision (Class 1)** | Proportion of predicted high-performers who are truly high-performers (minimizes false promotions). | Medium |
| **Recall (Class 1)** | Proportion of true high-performers correctly captured (minimizes missed talent). | Medium |
| **Brier Score / Log Loss** | Calibration metric evaluating probabilistic prediction accuracy. | Medium |

---

## 6. Multi-Criteria Model Selection Framework

The final "Champion Model" for JDS and SDS will be determined using a **Balanced Scorecard**:
1. **Predictive Performance (40%)**: Cross-validated ROC-AUC and F1-Score.
2. **Model Stability (25%)**: Low standard deviation across the 25 CV splits (absence of volatility).
3. **Interpretability & Transparency (25%)**: Clarity of coefficients, decision paths, or feature importance for business stakeholders.
4. **Generalization Gap (10%)**: Minimal divergence between train score and cross-validated test score ($|\text{Train} - \text{Test}| \le 0.10$).
