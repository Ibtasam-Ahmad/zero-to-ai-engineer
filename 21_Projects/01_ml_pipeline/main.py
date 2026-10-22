"""
ML Pipeline: Diabetes Disease Progression Prediction
Trains multiple models, evaluates, selects best, and saves with MLflow tracking.
"""

import logging
import os
import warnings
from typing import Dict, Tuple

import joblib
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_predict, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    logger.warning("XGBoost not installed. Skipping XGBoost model.")

MODEL_DIR = "models"
INTERVAL_LEVEL = 0.90  # the API reports a 90% prediction interval
os.makedirs(MODEL_DIR, exist_ok=True)


def load_data() -> Tuple[pd.DataFrame, pd.Series]:
    """Load and return the sklearn diabetes dataset."""
    data = load_diabetes()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target, name="target")
    logger.info(f"Loaded dataset: {X.shape[0]} samples, {X.shape[1]} features")
    return X, y


def evaluate_model(model, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
    """Compute MAE, RMSE, R² for a fitted model."""
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)
    return {"MAE": mae, "RMSE": rmse, "R2": r2}


def compute_interval(pipeline, X_train, y_train, X_test, y_test, level: float = INTERVAL_LEVEL) -> Dict[str, float]:
    """
    Prediction interval from cross-validated residuals (a simple "split conformal" idea).
    residual = true value - predicted value, measured on folds the model did NOT train on.
    With level=0.90 the 5% and 95% quantiles of the residuals give: pred + low ... pred + high.
    Also reports how often the interval contained the true value on the test set.
    """
    residuals = np.asarray(y_train) - cross_val_predict(pipeline, X_train, y_train, cv=5)
    alpha = (1 - level) / 2
    low, high = np.quantile(residuals, [alpha, 1 - alpha])
    test_preds = pipeline.predict(X_test)
    y_test = np.asarray(y_test)
    covered = float(((y_test >= test_preds + low) & (y_test <= test_preds + high)).mean())
    return {"level": level, "lower_offset": float(low), "upper_offset": float(high), "test_coverage": covered}


def build_models() -> Dict[str, Pipeline]:
    """Return dict of named sklearn pipelines."""
    models = {
        "LinearRegression": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LinearRegression()),
        ]),
        "Ridge": Pipeline([
            ("scaler", StandardScaler()),
            ("model", Ridge(alpha=1.0)),
        ]),
        "RandomForest": Pipeline([
            ("scaler", StandardScaler()),
            ("model", RandomForestRegressor(n_estimators=100, random_state=42)),
        ]),
    }
    if XGBOOST_AVAILABLE:
        models["XGBoost"] = Pipeline([
            ("scaler", StandardScaler()),
            ("model", xgb.XGBRegressor(n_estimators=100, random_state=42, verbosity=0)),
        ])
    return models


def train_and_evaluate(test_size: float = 0.2, random_state: int = 42) -> str:
    """
    Train all models, log to MLflow, save best model.
    Returns name of the best model.
    """
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    mlflow.set_experiment("diabetes_prediction")
    models = build_models()
    results = {}

    for name, pipeline in models.items():
        logger.info(f"Training {name}...")
        with mlflow.start_run(run_name=name):
            pipeline.fit(X_train, y_train)
            metrics = evaluate_model(pipeline, X_test, y_test)
            cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring="r2")

            mlflow.log_param("model_type", name)
            mlflow.log_param("test_size", test_size)
            mlflow.log_params(pipeline.get_params())
            mlflow.log_metrics(metrics)
            mlflow.log_metric("cv_r2_mean", cv_scores.mean())
            mlflow.log_metric("cv_r2_std", cv_scores.std())
            try:
                mlflow.sklearn.log_model(pipeline, "model")
            except Exception as e:  # e.g. MLflow 3.x refuses to save XGBoost this way; metrics are still logged
                logger.warning(f"  Could not log {name} model to MLflow ({type(e).__name__}); continuing.")

            results[name] = metrics
            logger.info(f"  {name}: MAE={metrics['MAE']:.2f}, RMSE={metrics['RMSE']:.2f}, R²={metrics['R2']:.4f}")

    # Select best by R²
    best_name = max(results, key=lambda k: results[k]["R2"])
    best_pipeline = models[best_name]
    best_pipeline.fit(X_train, y_train)  # refit on train
    interval = compute_interval(best_pipeline, X_train, y_train, X_test, y_test)
    logger.info(f"{interval['level']:.0%} prediction interval: pred {interval['lower_offset']:+.1f} .. "
                f"pred {interval['upper_offset']:+.1f} (covered {interval['test_coverage']:.0%} of test patients)")

    model_path = os.path.join(MODEL_DIR, "best_model.joblib")
    meta_path = os.path.join(MODEL_DIR, "model_meta.joblib")
    joblib.dump(best_pipeline, model_path)
    joblib.dump({
        "best_model": best_name,
        "metrics": results[best_name],
        "feature_names": list(X.columns),
        "all_results": results,
        "interval": interval,
    }, meta_path)

    logger.info(f"\nBest model: {best_name} (R²={results[best_name]['R2']:.4f})")
    logger.info(f"Saved to {model_path}")
    return best_name


if __name__ == "__main__":
    best = train_and_evaluate()
    print(f"\nBest model saved: {best}")
