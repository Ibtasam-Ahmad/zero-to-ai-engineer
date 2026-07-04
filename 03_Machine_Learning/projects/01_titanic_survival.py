"""
Titanic Survival Prediction
Complete ML pipeline: EDA → Feature Engineering → Model → Evaluation
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
import warnings
warnings.filterwarnings("ignore")


def load_or_generate_data():
    """Load Titanic data from seaborn or generate synthetic."""
    try:
        df = sns.load_dataset("titanic")
        print(f"Loaded Titanic dataset: {df.shape}")
        return df
    except Exception:
        print("Generating synthetic Titanic-like dataset...")
        np.random.seed(42)
        n = 891
        df = pd.DataFrame({
            "survived": np.random.binomial(1, 0.38, n),
            "pclass": np.random.choice([1, 2, 3], n, p=[0.24, 0.21, 0.55]),
            "sex": np.random.choice(["male", "female"], n, p=[0.65, 0.35]),
            "age": np.random.normal(29.7, 14.5, n).clip(1, 80),
            "sibsp": np.random.choice([0,1,2,3], n, p=[0.68,0.23,0.07,0.02]),
            "parch": np.random.choice([0,1,2,3], n, p=[0.76,0.13,0.09,0.02]),
            "fare": np.random.exponential(32, n).clip(5, 512),
            "embarked": np.random.choice(["S","C","Q"], n, p=[0.72,0.19,0.09]),
            "name": [f"Smith, Mr. John {i}" for i in range(n)],
        })
        # Introduce missing values like real dataset
        df.loc[np.random.choice(n, 177, replace=False), "age"] = np.nan
        df.loc[np.random.choice(n, 2, replace=False), "embarked"] = np.nan
        return df


def feature_engineering(df):
    """Extract new features from raw columns."""
    df = df.copy()

    # Extract title from name
    if "name" in df.columns:
        df["title"] = df["name"].str.extract(r",\s*([^\.]+)\.")
        df["title"] = df["title"].str.strip()
        rare_titles = df["title"].value_counts()[df["title"].value_counts() < 10].index
        df["title"] = df["title"].replace(rare_titles, "Rare")
        df["title"] = df["title"].replace({"Mlle": "Miss", "Ms": "Miss", "Mme": "Mrs"})
    else:
        df["title"] = "Mr"

    # Family size
    df["family_size"] = df["sibsp"] + df["parch"] + 1
    df["is_alone"] = (df["family_size"] == 1).astype(int)

    # Fare bins
    df["fare_bin"] = pd.qcut(df["fare"].fillna(df["fare"].median()), 4,
                              labels=["low", "mid", "high", "very_high"])

    # Age groups
    df["age_group"] = pd.cut(df["age"].fillna(df["age"].median()), 5,
                              labels=["child", "teen", "adult", "middle", "senior"])

    return df


def eda(df):
    """Quick EDA plots."""
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    fig.suptitle("Titanic EDA", fontsize=14, fontweight="bold")

    # Survival rate
    df["survived"].value_counts().plot(kind="bar", ax=axes[0, 0], color=["#e74c3c", "#2ecc71"])
    axes[0, 0].set_title("Survival Count")
    axes[0, 0].set_xticklabels(["Died", "Survived"], rotation=0)

    # Survival by sex
    df.groupby("sex")["survived"].mean().plot(kind="bar", ax=axes[0, 1], color=["#3498db", "#e91e63"])
    axes[0, 1].set_title("Survival Rate by Sex")
    axes[0, 1].set_ylim(0, 1)

    # Survival by class
    df.groupby("pclass")["survived"].mean().plot(kind="bar", ax=axes[0, 2], color=["gold", "silver", "#cd7f32"])
    axes[0, 2].set_title("Survival Rate by Class")
    axes[0, 2].set_ylim(0, 1)

    # Age distribution
    df[df["survived"] == 1]["age"].dropna().hist(ax=axes[1, 0], bins=20, alpha=0.7, label="Survived", color="#2ecc71")
    df[df["survived"] == 0]["age"].dropna().hist(ax=axes[1, 0], bins=20, alpha=0.7, label="Died", color="#e74c3c")
    axes[1, 0].set_title("Age Distribution by Survival")
    axes[1, 0].legend()

    # Family size
    df.groupby("family_size")["survived"].mean().plot(kind="bar", ax=axes[1, 1])
    axes[1, 1].set_title("Survival Rate by Family Size")
    axes[1, 1].set_ylim(0, 1)

    # Fare vs survival
    df.boxplot(column="fare", by="survived", ax=axes[1, 2])
    axes[1, 2].set_title("Fare by Survival")

    plt.tight_layout()
    plt.savefig("titanic_eda.png", dpi=100)
    print("EDA saved to titanic_eda.png")
    plt.close()


def build_pipeline():
    """Build sklearn preprocessing + model pipeline."""
    numeric_features = ["age", "fare", "family_size", "sibsp", "parch"]
    categorical_features = ["pclass", "sex", "embarked", "title", "fare_bin", "age_group", "is_alone"]

    numeric_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ])

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(random_state=42)),
    ])

    return pipeline


def tune_hyperparameters(pipeline, X_train, y_train):
    """GridSearchCV for hyperparameter tuning."""
    param_grid = {
        "classifier__n_estimators": [100, 200],
        "classifier__max_depth": [5, 10, None],
        "classifier__min_samples_split": [2, 5],
    }
    print("Running GridSearchCV (this may take a moment)...")
    grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring="roc_auc", n_jobs=-1)
    grid_search.fit(X_train, y_train)
    print(f"Best params: {grid_search.best_params_}")
    print(f"Best CV ROC-AUC: {grid_search.best_score_:.4f}")
    return grid_search.best_estimator_


def evaluate(model, X_test, y_test):
    """Evaluate model and plot confusion matrix."""
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred, target_names=["Died", "Survived"]))
    print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax,
                xticklabels=["Died", "Survived"], yticklabels=["Died", "Survived"])
    ax.set_title("Confusion Matrix")
    ax.set_ylabel("True Label")
    ax.set_xlabel("Predicted Label")
    plt.tight_layout()
    plt.savefig("titanic_confusion_matrix.png", dpi=100)
    print("Confusion matrix saved to titanic_confusion_matrix.png")
    plt.close()


def plot_feature_importance(model, X_train):
    """Plot feature importances from the Random Forest."""
    rf = model.named_steps["classifier"]
    preprocessor = model.named_steps["preprocessor"]

    # Get feature names after preprocessing
    num_features = ["age", "fare", "family_size", "sibsp", "parch"]
    cat_features = preprocessor.named_transformers_["cat"]["encoder"].get_feature_names_out(
        ["pclass", "sex", "embarked", "title", "fare_bin", "age_group", "is_alone"]
    )
    all_features = num_features + list(cat_features)

    importances = rf.feature_importances_
    indices = np.argsort(importances)[-20:]  # top 20

    plt.figure(figsize=(10, 8))
    plt.barh(range(len(indices)), importances[indices], align="center")
    plt.yticks(range(len(indices)), [all_features[i] for i in indices])
    plt.title("Top 20 Feature Importances (Random Forest)")
    plt.tight_layout()
    plt.savefig("titanic_feature_importance.png", dpi=100)
    print("Feature importance saved to titanic_feature_importance.png")
    plt.close()


if __name__ == "__main__":
    print("=" * 50)
    print("  TITANIC SURVIVAL PREDICTION")
    print("=" * 50)

    # Load data
    df = load_or_generate_data()

    # Feature engineering
    print("\n[1] Feature Engineering...")
    df = feature_engineering(df)

    # EDA
    print("[2] Generating EDA plots...")
    eda(df)

    # Prepare features/target
    target = "survived"
    features = ["pclass", "sex", "age", "sibsp", "parch", "fare", "embarked",
                "title", "family_size", "is_alone", "fare_bin", "age_group"]

    df_model = df[features + [target]].copy()
    X = df_model.drop(columns=[target])
    y = df_model[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                          random_state=42, stratify=y)
    print(f"\nTrain size: {len(X_train)} | Test size: {len(X_test)}")

    # Build pipeline
    print("\n[3] Building pipeline...")
    pipeline = build_pipeline()

    # Quick cross-validation before tuning
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring="roc_auc")
    print(f"Base CV ROC-AUC: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    # Tune
    print("\n[4] Hyperparameter tuning...")
    best_model = tune_hyperparameters(pipeline, X_train, y_train)

    # Evaluate
    print("\n[5] Evaluation on test set...")
    evaluate(best_model, X_test, y_test)

    # Feature importance
    print("\n[6] Feature importance...")
    plot_feature_importance(best_model, X_train)

    print("\nDone! All outputs saved.")
