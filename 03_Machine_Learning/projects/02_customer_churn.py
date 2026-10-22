"""
Telecom Customer Churn Prediction
Handles class imbalance with SMOTE, uses XGBoost, explains with SHAP.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, cross_val_predict
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (classification_report, confusion_matrix,
                              roc_auc_score, precision_recall_curve, f1_score)
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings("ignore")

try:
    from xgboost import XGBClassifier
except ImportError:
    print("XGBoost not found, using GradientBoostingClassifier")
    from sklearn.ensemble import GradientBoostingClassifier as XGBClassifier

try:
    from imblearn.over_sampling import SMOTENC
    from imblearn.pipeline import Pipeline as ImbPipeline
    SMOTE_AVAILABLE = True
except ImportError:
    print("imbalanced-learn not found, skipping SMOTE")
    SMOTE_AVAILABLE = False

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    print("SHAP not found, skipping SHAP plots")
    SHAP_AVAILABLE = False


def generate_churn_data(n=5000, churn_rate=0.15, seed=42):
    """Generate realistic synthetic telecom churn dataset."""
    np.random.seed(seed)

    tenure = np.random.exponential(24, n).clip(1, 72).astype(int)
    monthly_charges = np.random.normal(65, 30, n).clip(20, 120)
    total_charges = tenure * monthly_charges + np.random.normal(0, 50, n)

    data = pd.DataFrame({
        "tenure": tenure,
        "monthly_charges": monthly_charges,
        "total_charges": total_charges.clip(0),
        "contract": np.random.choice(["Month-to-month", "One year", "Two year"], n,
                                      p=[0.55, 0.25, 0.20]),
        "payment_method": np.random.choice(
            ["Electronic check", "Mailed check", "Bank transfer", "Credit card"], n),
        "internet_service": np.random.choice(["DSL", "Fiber optic", "No"], n, p=[0.34, 0.44, 0.22]),
        "phone_service": np.random.choice(["Yes", "No"], n, p=[0.90, 0.10]),
        "multiple_lines": np.random.choice(["Yes", "No", "No phone service"], n, p=[0.42, 0.48, 0.10]),
        "online_security": np.random.choice(["Yes", "No", "No internet"], n, p=[0.28, 0.50, 0.22]),
        "tech_support": np.random.choice(["Yes", "No", "No internet"], n, p=[0.29, 0.49, 0.22]),
        "streaming_tv": np.random.choice(["Yes", "No", "No internet"], n, p=[0.38, 0.40, 0.22]),
        "paperless_billing": np.random.choice(["Yes", "No"], n, p=[0.59, 0.41]),
        "senior_citizen": np.random.binomial(1, 0.16, n),
        "partner": np.random.choice(["Yes", "No"], n, p=[0.48, 0.52]),
        "dependents": np.random.choice(["Yes", "No"], n, p=[0.30, 0.70]),
        "num_support_calls": np.random.poisson(1.5, n),
    })

    # Churn probability influenced by features
    churn_prob = (
        0.35 * (data["contract"] == "Month-to-month").astype(float)
        + 0.20 * (data["internet_service"] == "Fiber optic").astype(float)
        + 0.15 * (data["online_security"] == "No").astype(float)
        + 0.10 * (data["tenure"] < 12).astype(float)
        + 0.10 * (data["payment_method"] == "Electronic check").astype(float)
        + 0.05 * (data["num_support_calls"] > 3).astype(float)
        - 0.10 * (data["tenure"] > 48).astype(float)
    )
    churn_prob = (churn_prob - churn_prob.min()) / (churn_prob.max() - churn_prob.min())
    churn_prob = churn_prob * 0.4 + 0.05  # scale to realistic range

    data["churn"] = (np.random.uniform(0, 1, n) < churn_prob).astype(int)
    print(f"Generated {n} customers | Churn rate: {data['churn'].mean():.1%}")
    return data


def preprocess(df):
    """Encode categoricals and engineer row-wise features (no statistics over the whole dataset)."""
    df = df.copy()

    # Feature engineering (row-wise only, so it is safe to do before the split)
    df["charges_per_tenure"] = df["total_charges"] / (df["tenure"] + 1)
    # NOTE: "high_monthly" needs a 75% quantile. Computing it here, on the full dataset,
    # would leak test-set information, so it is learned from training data by HighMonthlyFlag below.

    # Label encode categoricals
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    le = LabelEncoder()
    for col in cat_cols:
        df[col] = le.fit_transform(df[col].astype(str))

    return df


class HighMonthlyFlag(BaseEstimator, TransformerMixin):
    """Adds high_monthly = monthly_charges > 75% quantile, with the quantile learned in fit()
    (i.e. from the training data / training fold only)."""

    def __init__(self, quantile=0.75):
        self.quantile = quantile

    def fit(self, X, y=None):
        self.threshold_ = X["monthly_charges"].quantile(self.quantile)
        return self

    def transform(self, X):
        X = X.copy()
        X["high_monthly"] = (X["monthly_charges"] > self.threshold_).astype(int)
        return X


def optimize_threshold(y_true, y_prob):
    """Find threshold that maximizes F1 score."""
    precision, recall, thresholds = precision_recall_curve(y_true, y_prob)
    f1_scores = 2 * (precision * recall) / (precision + recall + 1e-8)
    best_idx = np.argmax(f1_scores)
    best_threshold = thresholds[best_idx] if best_idx < len(thresholds) else 0.5
    return best_threshold, f1_scores[best_idx]


def plot_results(y_test, y_pred, y_prob, feature_names, model):
    """Plot confusion matrix and precision-recall curve."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    import seaborn as sns
    sns.heatmap(cm, annot=True, fmt="d", cmap="Reds", ax=axes[0],
                xticklabels=["No Churn", "Churn"],
                yticklabels=["No Churn", "Churn"])
    axes[0].set_title("Confusion Matrix")

    # Precision-Recall curve
    precision, recall, _ = precision_recall_curve(y_test, y_prob)
    axes[1].plot(recall, precision, color="#e74c3c", lw=2)
    axes[1].fill_between(recall, precision, alpha=0.1, color="#e74c3c")
    axes[1].set_xlabel("Recall")
    axes[1].set_ylabel("Precision")
    axes[1].set_title("Precision-Recall Curve")
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("churn_results.png", dpi=100)
    print("Results saved to churn_results.png")
    plt.close()


if __name__ == "__main__":
    print("=" * 50)
    print("  CUSTOMER CHURN PREDICTION")
    print("=" * 50)

    # Generate data
    print("\n[1] Generating synthetic churn dataset...")
    df = generate_churn_data(n=5000)
    print(f"Class distribution:\n{df['churn'].value_counts()}")

    # Preprocess
    print("\n[2] Preprocessing...")
    # Categorical columns (label-encoded below). Plain SMOTE would interpolate their codes, so a
    # synthetic customer "between" code 0 and code 2 gets code 1, a category neither neighbour has.
    # SMOTENC treats these columns as categories instead.
    cat_cols = df.select_dtypes(include="object").columns.tolist() + ["senior_citizen", "high_monthly"]
    df = preprocess(df)

    X = df.drop(columns=["churn"])
    y = df["churn"]
    feature_names = X.columns.tolist()
    # column positions after HighMonthlyFlag (which appends "high_monthly" as the last column)
    cat_idx = [i for i, c in enumerate(feature_names + ["high_monthly"]) if c in cat_cols]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    # Handle imbalance with SMOTE.
    # SMOTE lives INSIDE the pipeline, so it only ever oversamples the data a model is trained on
    # (the training folds during cross-validation); validation folds and the test set stay real.
    print(f"\n[3] Before SMOTE: {y_train.value_counts().to_dict()}")
    if SMOTE_AVAILABLE:
        _, y_demo_res = SMOTENC(categorical_features=cat_idx, random_state=42).fit_resample(
            HighMonthlyFlag().fit_transform(X_train), y_train)
        print(f"After SMOTE (training data only, for illustration): {pd.Series(y_demo_res).value_counts().to_dict()}")
    else:
        print("SMOTE skipped using scale_pos_weight instead")

    # Train XGBoost
    print("\n[4] Training XGBoost...")
    try:
        model = XGBClassifier(
            n_estimators=200, max_depth=5, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8,
            scale_pos_weight=(1 if SMOTE_AVAILABLE else (y_train == 0).sum() / (y_train == 1).sum()),
            random_state=42, eval_metric="logloss", verbosity=0
        )
    except TypeError:
        model = XGBClassifier(n_estimators=200, max_depth=5, random_state=42)

    if SMOTE_AVAILABLE:
        pipe = ImbPipeline([("high_monthly", HighMonthlyFlag()),
                            ("smote", SMOTENC(categorical_features=cat_idx, random_state=42)),
                            ("model", model)])
    else:
        pipe = Pipeline([("high_monthly", HighMonthlyFlag()), ("model", model)])

    # Cross-validation on the ORIGINAL training data: the quantile and SMOTE are re-fitted
    # inside each training fold, and each validation fold contains only real customers.
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="roc_auc")
    print(f"CV ROC-AUC: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    pipe.fit(X_train, y_train)
    model = pipe.named_steps["model"]

    # Threshold optimization on out-of-fold predictions from the TRAINING data,
    # so the test set is used only once, for the final report.
    print("\n[5] Threshold optimization (out-of-fold, training data)...")
    oof_prob = cross_val_predict(pipe, X_train, y_train, cv=cv, method="predict_proba")[:, 1]
    best_threshold, best_f1 = optimize_threshold(y_train, oof_prob)
    print(f"Optimal threshold: {best_threshold:.3f} | Best out-of-fold F1: {best_f1:.4f}")

    y_prob = pipe.predict_proba(X_test)[:, 1]

    y_pred = (y_prob >= best_threshold).astype(int)

    # Evaluate
    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred, target_names=["No Churn", "Churn"]))
    print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")

    # Plots
    print("\n[6] Plotting results...")
    plot_results(y_test, y_pred, y_prob, feature_names, model)

    # SHAP explanations
    if SHAP_AVAILABLE:
        print("\n[7] Computing SHAP values...")
        X_test_feat = pipe.named_steps["high_monthly"].transform(X_test)  # same features the model saw
        feature_names = X_test_feat.columns.tolist()
        try:
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_test_feat[:200])
        except ValueError:
            # Older shap releases (< 0.48) cannot parse models saved by XGBoost >= 3.1
            # ("could not convert string to float: '[5E-1]'"). XGBoost computes the same
            # TreeSHAP values itself; the last column it returns is the bias term.
            import xgboost
            contribs = model.get_booster().predict(xgboost.DMatrix(X_test_feat[:200]), pred_contribs=True)
            shap_values = contribs[:, :-1]
        plt.figure()
        shap.summary_plot(shap_values, X_test_feat[:200], feature_names=feature_names,
                          show=False, max_display=15)
        plt.tight_layout()
        plt.savefig("churn_shap.png", dpi=100, bbox_inches="tight")
        print("SHAP summary saved to churn_shap.png")
        plt.close()

    print("\nDone!")
