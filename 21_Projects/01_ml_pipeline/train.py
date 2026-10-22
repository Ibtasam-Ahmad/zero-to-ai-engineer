"""
CLI training script for the diabetes prediction pipeline.
Usage: python train.py --model-type RandomForest --test-size 0.2 --random-state 42
"""

import argparse
import logging

import joblib
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_predict, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

MODEL_MAP = {
    "LinearRegression": LinearRegression(),
    "Ridge": Ridge(alpha=1.0),
    "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42),
}

try:
    import xgboost as xgb
    MODEL_MAP["XGBoost"] = xgb.XGBRegressor(n_estimators=100, random_state=42, verbosity=0)
except ImportError:
    pass


def main():
    parser = argparse.ArgumentParser(description="Train a diabetes prediction model.")
    parser.add_argument("--model-type", type=str, default="RandomForest",
                        choices=list(MODEL_MAP.keys()), help="Model to train")
    parser.add_argument("--test-size", type=float, default=0.2, help="Test split fraction")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed")
    parser.add_argument("--output", type=str, default="models/best_model.joblib",
                        help="Output path for saved model")
    args = parser.parse_args()

    data = load_diabetes(as_frame=True)  # keep column names, like main.py (api.py sends named columns)
    X, y = data.data, data.target
    feature_names = data.feature_names

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=args.random_state
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", MODEL_MAP[args.model_type]),
    ])

    logger.info(f"Training {args.model_type}...")
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)

    mae  = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2   = r2_score(y_test, preds)

    logger.info(f"Results MAE: {mae:.2f} | RMSE: {rmse:.2f} | R²: {r2:.4f}")

    # 90% prediction interval from cross-validated residuals (same method as compute_interval in main.py)
    residuals = np.asarray(y_train) - cross_val_predict(pipeline, X_train, y_train, cv=5)
    low, high = np.quantile(residuals, [0.05, 0.95])
    covered = float(((y_test >= preds + low) & (y_test <= preds + high)).mean())
    logger.info(f"90% interval: pred {low:+.1f} .. pred {high:+.1f} (covered {covered:.0%} of test patients)")

    import os; os.makedirs(os.path.dirname(args.output), exist_ok=True)
    joblib.dump(pipeline, args.output)
    joblib.dump({
        "best_model": args.model_type,
        "metrics": {"MAE": mae, "RMSE": rmse, "R2": r2},
        "feature_names": list(feature_names),
        "all_results": {args.model_type: {"MAE": mae, "RMSE": rmse, "R2": r2}},
        "interval": {"level": 0.90, "lower_offset": float(low), "upper_offset": float(high), "test_coverage": covered},
    }, os.path.join(os.path.dirname(args.output), "model_meta.joblib"))  # the file name api.py loads

    logger.info(f"Model saved to {args.output}")


if __name__ == "__main__":
    main()
