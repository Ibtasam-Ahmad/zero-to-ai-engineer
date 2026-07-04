"""
House Price Regression
Compares Ridge, Lasso, ElasticNet with polynomial features.
Includes learning curves and residual plots.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score, learning_curve
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings("ignore")


def load_data():
    """Load California housing or generate synthetic data."""
    try:
        data = fetch_california_housing(as_frame=True)
        df = data.frame
        print(f"Loaded California Housing: {df.shape}")
        return df, "MedHouseVal"
    except Exception:
        print("Generating synthetic housing data...")
        np.random.seed(42)
        n = 2000
        df = pd.DataFrame({
            "size_sqft": np.random.normal(1500, 500, n).clip(500, 5000),
            "bedrooms": np.random.choice([1, 2, 3, 4, 5], n, p=[0.05, 0.20, 0.40, 0.25, 0.10]),
            "bathrooms": np.random.choice([1, 2, 3], n, p=[0.30, 0.50, 0.20]),
            "age_years": np.random.exponential(20, n).clip(0, 100),
            "garage": np.random.binomial(1, 0.7, n),
            "distance_center_km": np.random.exponential(10, n).clip(1, 50),
            "school_rating": np.random.uniform(1, 10, n),
            "crime_rate": np.random.exponential(5, n).clip(0, 50),
            "lat": np.random.uniform(34, 38, n),
            "lon": np.random.uniform(-122, -118, n),
        })
        df["price"] = (
            df["size_sqft"] * 200
            + df["bedrooms"] * 10000
            + df["bathrooms"] * 15000
            - df["age_years"] * 500
            + df["garage"] * 20000
            - df["distance_center_km"] * 3000
            + df["school_rating"] * 8000
            - df["crime_rate"] * 1000
            + np.random.normal(0, 30000, n)
        ).clip(50000, 2000000)
        return df, "price"


def evaluate_model(name, model, X_train, X_test, y_train, y_test):
    """Fit and evaluate a model, return metrics dict."""
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    cv_rmse = np.sqrt(-cross_val_score(model, X_train, y_train,
                                        cv=5, scoring="neg_mean_squared_error").mean())

    return {"Model": name, "RMSE": rmse, "MAE": mae, "R²": r2, "CV_RMSE": cv_rmse,
            "y_pred": y_pred}


def plot_learning_curve(model, X, y, name, ax):
    """Plot training vs validation learning curve."""
    train_sizes, train_scores, val_scores = learning_curve(
        model, X, y, cv=5, scoring="neg_root_mean_squared_error",
        train_sizes=np.linspace(0.1, 1.0, 8), n_jobs=-1)

    train_mean = -train_scores.mean(axis=1)
    val_mean = -val_scores.mean(axis=1)

    ax.plot(train_sizes, train_mean, "o-", label="Train RMSE", color="#2ecc71")
    ax.plot(train_sizes, val_mean, "o-", label="Val RMSE", color="#e74c3c")
    ax.fill_between(train_sizes, train_mean - train_scores.std(axis=1),
                    train_mean + train_scores.std(axis=1), alpha=0.1, color="#2ecc71")
    ax.fill_between(train_sizes, val_mean - val_scores.std(axis=1),
                    val_mean + val_scores.std(axis=1), alpha=0.1, color="#e74c3c")
    ax.set_title(f"Learning Curve: {name}")
    ax.set_xlabel("Training Samples")
    ax.set_ylabel("RMSE")
    ax.legend()
    ax.grid(True, alpha=0.3)


def plot_residuals(results, y_test, axes):
    """Plot residuals for each model."""
    for ax, result in zip(axes, results):
        residuals = y_test.values - result["y_pred"]
        ax.scatter(result["y_pred"], residuals, alpha=0.4, s=10, color="#3498db")
        ax.axhline(y=0, color="red", linestyle="--", linewidth=1)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Residuals")
        ax.set_title(f"Residuals: {result['Model']}")
        ax.grid(True, alpha=0.3)


if __name__ == "__main__":
    print("=" * 50)
    print("  HOUSE PRICE REGRESSION")
    print("=" * 50)

    # Load data
    print("\n[1] Loading data...")
    df, target_col = load_data()
    print(df.describe().round(2))

    X = df.drop(columns=[target_col])
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define models with polynomial features
    models = {
        "Ridge (poly=2)": Pipeline([
            ("poly", PolynomialFeatures(degree=2, include_bias=False)),
            ("scaler", StandardScaler()),
            ("model", Ridge(alpha=1.0)),
        ]),
        "Lasso (poly=2)": Pipeline([
            ("poly", PolynomialFeatures(degree=2, include_bias=False)),
            ("scaler", StandardScaler()),
            ("model", Lasso(alpha=0.1, max_iter=5000)),
        ]),
        "ElasticNet (poly=2)": Pipeline([
            ("poly", PolynomialFeatures(degree=2, include_bias=False)),
            ("scaler", StandardScaler()),
            ("model", ElasticNet(alpha=0.1, l1_ratio=0.5, max_iter=5000)),
        ]),
    }

    # Evaluate all models
    print("\n[2] Training and evaluating models...")
    results = []
    for name, model in models.items():
        print(f"  → {name}...")
        res = evaluate_model(name, model, X_train, X_test, y_train, y_test)
        results.append(res)

    # Print comparison table
    metrics_df = pd.DataFrame([{k: v for k, v in r.items() if k != "y_pred"} for r in results])
    metrics_df = metrics_df.round(4)
    print("\n=== Model Comparison ===")
    print(metrics_df.to_string(index=False))

    # Learning curves
    print("\n[3] Plotting learning curves...")
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for ax, (name, model) in zip(axes, models.items()):
        plot_learning_curve(model, X_train, y_train, name.split(" ")[0], ax)
    plt.suptitle("Learning Curves", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("house_learning_curves.png", dpi=100)
    print("Learning curves saved to house_learning_curves.png")
    plt.close()

    # Residual plots
    print("[4] Plotting residuals...")
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    plot_residuals(results, y_test, axes)
    plt.suptitle("Residual Plots", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("house_residuals.png", dpi=100)
    print("Residuals saved to house_residuals.png")
    plt.close()

    # Best model
    best = min(results, key=lambda x: x["RMSE"])
    print(f"\nBest model: {best['Model']} (RMSE={best['RMSE']:.4f}, R²={best['R²']:.4f})")
    print("\nDone!")
