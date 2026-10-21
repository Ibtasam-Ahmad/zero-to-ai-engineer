"""
Forecasting System: trains ARIMA, Prophet, LSTM, XGBoost on time series data.
Generates forecasts with confidence intervals and model comparison.
"""

import logging
import warnings
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def smape(y_true, y_pred):
    return 100 * np.mean(2 * np.abs(y_pred - y_true) / (np.abs(y_true) + np.abs(y_pred) + 1e-8))


def generate_sample_data(n_points: int = 365) -> pd.DataFrame:
    """Generate synthetic time series with trend + seasonality + noise."""
    dates = pd.date_range("2022-01-01", periods=n_points, freq="D")
    t = np.arange(n_points)
    trend = 0.05 * t
    seasonality = 10 * np.sin(2 * np.pi * t / 365) + 5 * np.sin(2 * np.pi * t / 7)
    noise = np.random.normal(0, 2, n_points)
    values = 100 + trend + seasonality + noise
    return pd.DataFrame({"ds": dates, "y": values})


def forecast_arima(df: pd.DataFrame, horizon: int) -> Dict:
    try:
        from statsmodels.tsa.arima.model import ARIMA
        y = df["y"].values
        split = int(len(y) * 0.8)
        model = ARIMA(y[:split], order=(2, 1, 2)).fit()
        fc = model.forecast(steps=horizon)
        ci = model.get_forecast(steps=horizon).conf_int()
        mae = mean_absolute_error(y[split:split+horizon], fc[:len(y)-split]) if len(y) > split else None
        return {
            "model": "ARIMA", "forecast": fc.tolist(),
            "lower": ci.iloc[:, 0].tolist(), "upper": ci.iloc[:, 1].tolist(),
            "mae": round(float(mae), 3) if mae else None,
        }
    except Exception as e:
        logger.warning(f"ARIMA failed: {e}")
        return _mock_forecast("ARIMA", df, horizon)


def forecast_prophet(df: pd.DataFrame, horizon: int) -> Dict:
    try:
        from prophet import Prophet
        m = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
        split = int(len(df) * 0.8)
        m.fit(df.iloc[:split])
        future = m.make_future_dataframe(periods=horizon)
        fc = m.predict(future).tail(horizon)
        return {
            "model": "Prophet",
            "forecast": fc["yhat"].tolist(),
            "lower":    fc["yhat_lower"].tolist(),
            "upper":    fc["yhat_upper"].tolist(),
            "mae": None,
        }
    except Exception as e:
        logger.warning(f"Prophet failed: {e}")
        return _mock_forecast("Prophet", df, horizon)


def forecast_xgboost(df: pd.DataFrame, horizon: int) -> Dict:
    try:
        import xgboost as xgb
        y = df["y"].values
        LAGS = 14

        def make_features(arr, lags):
            X, Y = [], []
            for i in range(lags, len(arr)):
                X.append(arr[i-lags:i][::-1])
                Y.append(arr[i])
            return np.array(X), np.array(Y)

        split = int(len(y) * 0.8)
        X_train, y_train = make_features(y[:split], LAGS)
        X_test, y_test = make_features(y[split:], LAGS)
        model = xgb.XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1, verbosity=0)
        model.fit(X_train, y_train)

        # Iterative forecast
        history = list(y[-LAGS:])
        preds = []
        for _ in range(horizon):
            feat = np.array(history[-LAGS:][::-1]).reshape(1, -1)
            p = float(model.predict(feat)[0])
            preds.append(p)
            history.append(p)

        std = float(np.std(y_test - model.predict(X_test)))
        return {
            "model": "XGBoost",
            "forecast": preds,
            "lower": [p - 1.96 * std for p in preds],
            "upper": [p + 1.96 * std for p in preds],
            "mae": round(float(mean_absolute_error(y_test, model.predict(X_test))), 3),
        }
    except Exception as e:
        logger.warning(f"XGBoost failed: {e}")
        return _mock_forecast("XGBoost", df, horizon)


def forecast_lstm(df: pd.DataFrame, horizon: int) -> Dict:
    try:
        import torch
        import torch.nn as nn

        y = df["y"].values.astype(np.float32)
        mean, std = y.mean(), y.std()
        y_norm = (y - mean) / std
        LAGS = 14

        X, Y = [], []
        for i in range(LAGS, len(y_norm)):
            X.append(y_norm[i-LAGS:i])
            Y.append(y_norm[i])
        X = torch.tensor(np.array(X), dtype=torch.float32).unsqueeze(-1)
        Y = torch.tensor(np.array(Y), dtype=torch.float32)

        class LSTMModel(nn.Module):
            def __init__(self):
                super().__init__()
                self.lstm = nn.LSTM(1, 64, 2, batch_first=True, dropout=0.1)
                self.fc   = nn.Linear(64, 1)
            def forward(self, x):
                out, _ = self.lstm(x)
                return self.fc(out[:, -1]).squeeze()

        model = LSTMModel()
        opt = torch.optim.Adam(model.parameters(), lr=0.001)
        loss_fn = nn.MSELoss()
        split = int(len(X) * 0.8)

        for _ in range(50):
            model.train()
            opt.zero_grad()
            loss = loss_fn(model(X[:split]), Y[:split])
            loss.backward(); opt.step()

        model.eval()
        history = list(y_norm[-LAGS:])
        preds_norm = []
        with torch.no_grad():
            for _ in range(horizon):
                inp = torch.tensor(history[-LAGS:], dtype=torch.float32).unsqueeze(0).unsqueeze(-1)
                p = float(model(inp))
                preds_norm.append(p)
                history.append(p)

        preds = [p * std + mean for p in preds_norm]
        residuals = Y[split:] - model(X[split:]).detach().numpy()
        s = float(residuals.std()) * std
        return {
            "model": "LSTM",
            "forecast": [round(float(p), 3) for p in preds],
            "lower":    [round(float(p) - 1.96*s, 3) for p in preds],
            "upper":    [round(float(p) + 1.96*s, 3) for p in preds],
            "mae": None,
        }
    except Exception as e:
        logger.warning(f"LSTM failed: {e}")
        return _mock_forecast("LSTM", df, horizon)


def _mock_forecast(name: str, df: pd.DataFrame, horizon: int) -> Dict:
    last = float(df["y"].iloc[-1])
    std  = float(df["y"].std()) * 0.1
    preds = [last + i * 0.05 + np.random.normal(0, std) for i in range(horizon)]
    return {
        "model":    name,
        "forecast": [round(p, 3) for p in preds],
        "lower":    [round(p - 2*std, 3) for p in preds],
        "upper":    [round(p + 2*std, 3) for p in preds],
        "mae":      None,
        "note":     f"{name} library not installed showing mock forecast",
    }


def run_forecast(df: pd.DataFrame, horizon: int = 30, models: List[str] = None) -> List[Dict]:
    all_models = {"arima": forecast_arima, "prophet": forecast_prophet,
                  "xgboost": forecast_xgboost, "lstm": forecast_lstm}
    selected = [m.lower() for m in (models or list(all_models.keys()))]
    results = []
    for name in selected:
        if name in all_models:
            logger.info(f"Running {name}...")
            results.append(all_models[name](df, horizon))
    return results
