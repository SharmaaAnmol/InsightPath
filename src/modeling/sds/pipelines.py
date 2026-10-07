"""
src/modeling/sds/pipelines.py
-----------------------------
Model pipeline construction for Senior Data Scientist (SDS) personality classification.
Encapsulates all preprocessing (StandardScaler) strictly within scikit-learn Pipelines
to prevent data leakage during grouped cross-validation.
"""

from typing import Dict, Any
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

SDS_FEATURE_NAMES = [
    "neuroticism",
    "extraversion",
    "openness_to_experience",
    "agreeableness",
    "conscientiousness"
]

SDS_TARGET_NAME = "success_classification_high_low"


def get_sds_models(random_state: int = 42) -> Dict[str, Pipeline]:
    """
    Constructs the set of candidate small-sample classification pipelines.
    All models are regularized to protect against overfitting on N=161.
    """
    models = {
        "Baseline_Majority": Pipeline([
            ("clf", DummyClassifier(strategy="prior"))
        ]),
        "Logistic_Regression_L2": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(
                penalty="l2",
                C=1.0,
                solver="lbfgs",
                random_state=random_state,
                max_iter=1000
            ))
        ]),
        "Logistic_Regression_L1": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(
                penalty="l1",
                C=1.0,
                solver="saga",
                random_state=random_state,
                max_iter=2000
            ))
        ]),
        "Logistic_Regression_ElasticNet": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(
                penalty="elasticnet",
                l1_ratio=0.5,
                C=1.0,
                solver="saga",
                random_state=random_state,
                max_iter=2000
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
                min_samples_leaf=3,
                max_features="sqrt",
                random_state=random_state
            ))
        ]),
        "Gradient_Boosting": Pipeline([
            ("clf", GradientBoostingClassifier(
                n_estimators=50,
                max_depth=2,
                learning_rate=0.05,
                random_state=random_state
            ))
        ])
    }
    return models
