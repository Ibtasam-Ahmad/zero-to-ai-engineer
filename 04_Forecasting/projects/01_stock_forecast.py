"""
Stock Price Forecasting
Compares ARIMA, LSTM, and Prophet on AAPL (or synthetic) data.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings("ignore")


def load_stock_data(ticker="AAPL", period="2y"):
    """Download stock data or generate synthetic."""
    try:
        import yfinance as yf
        df = yf.download(ticker, period=period, progress=False)
        df = df[["Close"]].rename(columns={"Close": "price"})
        df.index = pd.to_datetime(df.index)
        print(f"Downloaded {ticker} data: {len(df)} days")
        return df
    except Exception:
        print("yfinance unavailable generating synthetic stock data...")
        np.random.seed(42)
        dates = pd.date_range("2022-01-01", periods=500, freq="B")
        # Geometric Brownian Motion
        returns = np.random.normal(0.0005, 0.015, len(dates))
        price = 150 * np.exp(np.cumsum(returns))
        df = pd.DataFrame({"price": price}, index=dates)
        return df


def add_technical_indicators(df):
    """Add MA, RSI, MACD indicators."""
    df = df.copy()
    p = df["price"]

    # Moving averages
    df["ma_7"] = p.rolling(7).mean()
    df["ma_21"] = p.rolling(21).mean()
    df["ma_50"] = p.rolling(50).mean()

    # RSI (14-day)
    delta = p.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / (loss + 1e-8)
    df["rsi"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = p.ewm(span=12).mean()
    ema26 = p.ewm(span=26).mean()
    df["macd"] = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]

    return df.dropna()


def mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))) * 100


def arima_forecast(train, test_len=30):
    """ARIMA model forecast."""
    try:
        from statsmodels.tsa.arima.model import ARIMA
        from statsmodels.tsa.stattools import adfuller

        series = train["price"]
        # Check stationarity
        adf_result = adfuller(series)
        d = 0 if adf_result[1] < 0.05 else 1

        model = ARIMA(series, order=(5, d, 1))
        fitted = model.fit()
        forecast = fitted.forecast(steps=test_len)
        return forecast.values
    except Exception as e:
        print(f"ARIMA failed: {e}")
        return np.full(test_len, train["price"].iloc[-1])


def lstm_forecast(train, test_len=30, lookback=20):
    """LSTM forecast using PyTorch."""
    try:
        import torch
        import torch.nn as nn

        prices = train["price"].values.astype(np.float32)
        # Normalize
        price_min, price_max = prices.min(), prices.max()
        prices_norm = (prices - price_min) / (price_max - price_min + 1e-8)

        # Create sequences
        X_seq, y_seq = [], []
        for i in range(len(prices_norm) - lookback):
            X_seq.append(prices_norm[i:i+lookback])
            y_seq.append(prices_norm[i+lookback])
        X_tensor = torch.FloatTensor(X_seq).unsqueeze(-1)
        y_tensor = torch.FloatTensor(y_seq)

        class LSTMForecaster(nn.Module):
            def __init__(self):
                super().__init__()
                self.lstm = nn.LSTM(1, 64, num_layers=2, batch_first=True, dropout=0.2)
                self.fc = nn.Linear(64, 1)
            def forward(self, x):
                out, _ = self.lstm(x)
                return self.fc(out[:, -1, :]).squeeze()

        model = LSTMForecaster()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
        criterion = nn.MSELoss()

        model.train()
        for epoch in range(50):
            optimizer.zero_grad()
            pred = model(X_tensor)
            loss = criterion(pred, y_tensor)
            loss.backward()
            optimizer.step()

        # Multi-step forecast
        model.eval()
        window = prices_norm[-lookback:].tolist()
        forecasts = []
        with torch.no_grad():
            for _ in range(test_len):
                x = torch.FloatTensor(window[-lookback:]).unsqueeze(0).unsqueeze(-1)
                p = model(x).item()
                forecasts.append(p)
                window.append(p)

        forecasts = np.array(forecasts) * (price_max - price_min) + price_min
        return forecasts
    except Exception as e:
        print(f"LSTM failed: {e}")
        return np.full(test_len, train["price"].iloc[-1])


def prophet_forecast(train, test_len=30):
    """Prophet forecast."""
    try:
        from prophet import Prophet
        df_prophet = train.reset_index()[["index", "price"]].rename(
            columns={"index": "ds", "price": "y"})
        df_prophet["ds"] = pd.to_datetime(df_prophet["ds"])
        model = Prophet(daily_seasonality=False, weekly_seasonality=True,
                        yearly_seasonality=True, changepoint_prior_scale=0.05)
        model.fit(df_prophet)
        future = model.make_future_dataframe(periods=test_len, freq="B")
        forecast = model.predict(future)
        return forecast["yhat"].tail(test_len).values
    except Exception as e:
        print(f"Prophet failed: {e}")
        return np.full(test_len, train["price"].iloc[-1])


def plot_forecasts(test, forecasts_dict, title="Stock Price Forecasts"):
    """Plot all model forecasts vs actual."""
    plt.figure(figsize=(14, 6))
    plt.plot(test.index, test["price"].values, "k-", linewidth=2, label="Actual", zorder=5)

    colors = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12"]
    for (name, forecast), color in zip(forecasts_dict.items(), colors):
        plt.plot(test.index[:len(forecast)], forecast[:len(test)],
                 "--", color=color, linewidth=1.5, label=name)

    plt.title(title, fontsize=14)
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("stock_forecasts.png", dpi=100)
    print("Forecast plot saved to stock_forecasts.png")
    plt.close()


if __name__ == "__main__":
    print("=" * 50)
    print("  STOCK PRICE FORECASTING")
    print("=" * 50)

    TEST_LEN = 30

    # Load data
    print("\n[1] Loading data...")
    df = load_stock_data("AAPL")
    df = add_technical_indicators(df)

    # Split
    train = df.iloc[:-TEST_LEN]
    test = df.iloc[-TEST_LEN:]
    print(f"Train: {len(train)} days | Test: {len(test)} days")

    # Forecasts
    print("\n[2] Running forecasts...")
    forecasts = {}

    print("  → ARIMA...")
    forecasts["ARIMA"] = arima_forecast(train, TEST_LEN)

    print("  → LSTM...")
    forecasts["LSTM"] = lstm_forecast(train, TEST_LEN)

    print("  → Prophet...")
    forecasts["Prophet"] = prophet_forecast(train, TEST_LEN)

    # Ensemble
    valid = {k: v for k, v in forecasts.items() if len(v) == TEST_LEN}
    if valid:
        forecasts["Ensemble"] = np.mean(list(valid.values()), axis=0)

    # Evaluate
    print("\n=== Forecast Metrics ===")
    y_true = test["price"].values
    metrics_rows = []
    for name, pred in forecasts.items():
        pred_aligned = pred[:len(y_true)]
        row = {
            "Model": name,
            "MAE": round(mean_absolute_error(y_true, pred_aligned), 4),
            "RMSE": round(np.sqrt(mean_squared_error(y_true, pred_aligned)), 4),
            "MAPE": round(mape(y_true, pred_aligned), 2),
        }
        metrics_rows.append(row)

    metrics_df = pd.DataFrame(metrics_rows).sort_values("RMSE")
    print(metrics_df.to_string(index=False))

    # Plot
    print("\n[3] Plotting...")
    plot_forecasts(test, forecasts)

    best = metrics_df.iloc[0]
    print(f"\nBest model: {best['Model']} (RMSE={best['RMSE']}, MAPE={best['MAPE']}%)")
    print("Done!")
