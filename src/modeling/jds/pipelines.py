"""
pipelines.py
------------
Defines leakage-free scikit-learn model pipelines for JDS skill modeling:
  - Naive majority-class baseline (DummyClassifier)
  - Regularized Logistic Regression: L1 Lasso, L2 Ridge, ElasticNet (with StandardScaler)
  - Decision Tree Classifier (constrained max_depth <= 3)
  - Random Forest Classifier (100 trees, constrained depth)
  - Gradient Boosting Classifier (pre-registered sequential boosting benchmark)
  - Reduced 2-feature pipelines for parsimony evaluation
"""

from typing import Dict, Any
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


def build_candidate_pipelines(random_state: int = 42) -> Dict[str, Pipeline]:
    """
    Constructs all primary candidate classification pipelines.
    Guarantees no pre-split leakage: StandardScaler is inside each pipeline.
    """
    pipelines = {
        "Baseline_Majority": Pipeline([
            ("clf", DummyClassifier(strategy="most_frequent"))
        ]),
        "Logistic_Regression_L2": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(
                l1_ratio=0.0,
                solver="lbfgs",
                C=1.0,
                max_iter=1000,
                random_state=random_state
            ))
        ]),
        "Logistic_Regression_L1": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(
                l1_ratio=1.0,
                solver="saga",
                C=1.0,
                max_iter=2500,
                random_state=random_state
            ))
        ]),
        "Logistic_Regression_ElasticNet": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(
                l1_ratio=0.5,
                solver="saga",
                C=1.0,
                max_iter=2500,
                random_state=random_state
            ))
        ]),
        "Decision_Tree": Pipeline([
            ("clf", DecisionTreeClassifier(
                max_depth=3,
                min_samples_leaf=5,
                criterion="gini",
                random_state=random_state
            ))
        ]),
        "Random_Forest": Pipeline([
            ("clf", RandomForestClassifier(
                n_estimators=100,
                max_depth=3,
                min_samples_leaf=4,
                max_features="sqrt",
                random_state=random_state
            ))
        ]),
        "Gradient_Boosting": Pipeline([
            ("clf", GradientBoostingClassifier(
                n_estimators=50,
                max_depth=2,
                learning_rate=0.05,
                min_samples_leaf=4,
                random_state=random_state
            ))
        ])
    }
    return pipelines


def build_reduced_pipelines(random_state: int = 42) -> Dict[str, Pipeline]:
    """
    Constructs reduced 2-feature pipelines (Maths/Stats + Storytelling).
    Evaluates parsimonious predictive sufficiency without cherry-picking.
    """
    reduced_pipelines = {
        "Logistic_L2_Reduced_2Feat": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(
                l1_ratio=0.0,
                solver="lbfgs",
                C=1.0,
                max_iter=1000,
                random_state=random_state
            ))
        ]),
        "Decision_Tree_Reduced_2Feat": Pipeline([
            ("clf", DecisionTreeClassifier(
                max_depth=3,
                min_samples_leaf=5,
                criterion="gini",
                random_state=random_state
            ))
        ]),
        "Random_Forest_Reduced_2Feat": Pipeline([
            ("clf", RandomForestClassifier(
                n_estimators=100,
                max_depth=3,
                min_samples_leaf=4,
                max_features="sqrt",
                random_state=random_state
            ))
        ])
    }
    return reduced_pipelines


def build_model_configuration_table() -> pd.DataFrame:
    """Builds Table 3: phase5_model_configuration.csv."""
    configs = [
        {
            "model_id": "Baseline_Majority",
            "model_family": "Heuristic Baseline",
            "algorithm": "DummyClassifier (Strategy: Most Frequent)",
            "hyperparameters": "strategy='most_frequent'",
            "preprocessing": "None (Raw categorical distribution)",
            "inductive_bias": "Zero-Rule / Empirical Base Rate (52.52%)",
            "interpretability_level": "Trivial"
        },
        {
            "model_id": "Logistic_Regression_L2",
            "model_family": "Linear Parametric",
            "algorithm": "Ridge Logistic Regression (L2 penalty)",
            "hyperparameters": "C=1.0, l1_ratio=0.0, solver='lbfgs', max_iter=1000",
            "preprocessing": "StandardScaler() inside Pipeline",
            "inductive_bias": "Linear decision boundary with L2 weight shrinkage",
            "interpretability_level": "High (Standardized Odds Ratios)"
        },
        {
            "model_id": "Logistic_Regression_L1",
            "model_family": "Linear Parametric",
            "algorithm": "Lasso Logistic Regression (L1 penalty)",
            "hyperparameters": "C=1.0, l1_ratio=1.0, solver='saga', max_iter=2500",
            "preprocessing": "StandardScaler() inside Pipeline",
            "inductive_bias": "Linear decision boundary with sparse feature selection",
            "interpretability_level": "High (Sparse Odds Ratios)"
        },
        {
            "model_id": "Logistic_Regression_ElasticNet",
            "model_family": "Linear Parametric",
            "algorithm": "ElasticNet Logistic Regression (50% L1, 50% L2)",
            "hyperparameters": "C=1.0, l1_ratio=0.5, solver='saga', max_iter=2500",
            "preprocessing": "StandardScaler() inside Pipeline",
            "inductive_bias": "Linear boundary balancing sparsity and ridge grouping",
            "interpretability_level": "High (Penalized Odds Ratios)"
        },
        {
            "model_id": "Decision_Tree",
            "model_family": "Rule-Based Non-Linear",
            "algorithm": "Classification & Regression Tree (CART)",
            "hyperparameters": "max_depth=3, min_samples_leaf=5, criterion='gini'",
            "preprocessing": "None (Tree invariant to monotonic scaling)",
            "inductive_bias": "Axis-aligned hierarchical threshold partitions",
            "interpretability_level": "High (Visual IF-THEN Rules)"
        },
        {
            "model_id": "Random_Forest",
            "model_family": "Bagging Ensemble",
            "algorithm": "Random Forest Classifier",
            "hyperparameters": "n_estimators=100, max_depth=3, min_samples_leaf=4, max_features='sqrt'",
            "preprocessing": "None (Tree ensemble invariant to monotonic scaling)",
            "inductive_bias": "Bootstrap aggregating with random feature subspace sampling",
            "interpretability_level": "Moderate (Permutation Feature Importance)"
        },
        {
            "model_id": "Gradient_Boosting",
            "model_family": "Sequential Boosting Ensemble",
            "algorithm": "Gradient Boosting Classifier",
            "hyperparameters": "n_estimators=50, max_depth=2, learning_rate=0.05, min_samples_leaf=4",
            "preprocessing": "None (Sequential tree boosting)",
            "inductive_bias": "Additive functional gradient descent on log-loss",
            "interpretability_level": "Moderate (Permutation Feature Importance)"
        }
    ]
    return pd.DataFrame(configs)
