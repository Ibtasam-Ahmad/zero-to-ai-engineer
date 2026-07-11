"""
Energy Demand Forecasting
Synthetic hourly data, STL decomposition, SARIMA, XGBoost, Prophet with CI.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings("ignore")


def generate_energy_data(n_hours=8760):
    """Generate synthetic hourly energy demand with realistic patterns."""
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=n_hours, freq="h")
    t = np.arange(n_hours)

    # Long-term trend
    trend = 500 + 0.01 * t

    # Yearly seasonality (winter/summer peaks)
    yearly = 80 * np.sin(2 * np.pi * t / 8760 - np.pi / 2)

    # Weekly seasonality (weekday vs weekend)
    weekly = 40 * np.sin(2 * np.pi * t / (24 * 7))

    # Daily seasonality (morning and evening peaks)
    daily = (
        60 * np.sin(2 * np.pi * t / 24 - np.pi / 3)
        + 30 * np.sin(4 * np.pi * t / 24)
    )

    # Noise
    noise = np.random.normal(0, 15, n_hours)

    demand = trend + yearly + weekly + daily + noise
    df = pd.DataFrame({"demand": demand.clip(300, 900)}, index=dates)
    print(f"Generated {n_hours} hours of energy demand data")
    print(f"Mean demand: {df['demand'].mean():.1f} MW | Std: {df['demand'].std():.1f} MW")
    return df


def create_time_features(df):
    """Create time-based features for ML models."""
    df = df.copy()
    df["hour"] = df.index.hour
    df["day_of_week"] = df.index.dayofweek
    df["month"] = df.index.month
    df["day_of_year"] = df.index.dayofyear
    df["is_weekend"] = (df.index.dayofweek >= 5).astype(int)

    # Lag features
    for lag in [1, 2, 24, 48, 168]:  # 1h, 2h, 1d, 2d, 1w
        df[f"lag_{lag}"] = df["demand"].shift(lag)

    # Rolling statistics
    df["rolling_mean_24"] = df["demand"].shift(1).rolling(24).mean()
    df["rolling_std_24"] = df["demand"].shift(1).rolling(24).std()
    df["rolling_mean_168"] = df["demand"].shift(1).rolling(168).mean()

    return df.dropna()


def stl_decomposition(df_daily):
    """STL decomposition on daily aggregated data."""
    try:
        from statsmodels.tsa.seasonal import STL
        stl = STL(df_daily["demand"], period=7, robust=True)
        result = stl.fit()

        fig, axes = plt.subplots(4, 1, figsize=(12, 10))
        axes[0].plot(df_daily.index, df_daily["demand"], color="#2c3e50")
        axes[0].set_title("Original")
        axes[1].plot(result.trend, color="#3498db")
        axes[1].set_title("Trend")
        axes[2].plot(result.seasonal, color="#e74c3c")
        axes[2].set_title("Seasonal")
        axes[3].plot(result.resid, color="#95a5a6")
        axes[3].set_title("Residual")
        for ax in axes:
            ax.grid(True, alpha=0.3)
        plt.suptitle("STL Decomposition (Daily Energy Demand)", fontsize=13)
        plt.tight_layout()
        plt.savefig("energy_stl.png", dpi=100)
        print("STL decomposition saved to energy_stl.png")
        plt.close()
        return result
    except Exception as e:
        print(f"STL failed: {e}")
        return None


def sarima_forecast(train_daily, test_len=30):
    """SARIMA forecast on daily data."""
    try:
        from statsmodels.tsa.statespace.sarimax import SARIMAX
        model = SARIMAX(train_daily["demand"],
                        order=(1, 1, 1),
                        seasonal_order=(1, 1, 1, 7),
                        enforce_stationarity=False,
                        enforce_invertibility=False)
        fitted = model.fit(disp=False)
        forecast = fitted.get_forecast(steps=test_len)
        return forecast.predicted_mean.values, forecast.conf_int().values
    except Exception as e:
        print(f"SARIMA failed: {e}")
        val = train_daily["demand"].iloc[-1]
        return np.full(test_len, val), np.column_stack([np.full(test_len, val-10), np.full(test_len, val+10)])


def xgboost_forecast(df_feat, test_len=30):
    """XGBoost forecast using time features."""
    try:
        from xgboost import XGBRegressor
    except ImportError:
        from sklearn.ensemble import GradientBoostingRegressor as XGBRegressor

    feature_cols = [c for c in df_feat.columns if c != "demand"]
    X = df_feat[feature_cols]
    y = df_feat["demand"]

    X_train, X_test = X.iloc[:-test_len], X.iloc[-test_len:]
    y_train = y.iloc[:-test_len]

    try:
        model = XGBRegressor(n_estimators=200, max_depth=5, learning_rate=0.05,
                             subsample=0.8, colsample_bytree=0.8, random_state=42,
                             verbosity=0)
    except TypeError:
        model = XGBRegressor(n_estimators=200, random_state=42)

    model.fit(X_train, y_train)
    return model.predict(X_test)


def prophet_energy_forecast(df_daily, test_len=30):
    """Prophet forecast with holidays."""
    try:
        from prophet import Prophet
        df_p = df_daily.reset_index().rename(columns={"index": "ds", "demand": "y"})
        df_p["ds"] = pd.to_datetime(df_p["ds"])
        train_p = df_p.iloc[:-test_len]

        model = Prophet(
            yearly_seasonality=True, weekly_seasonality=True,
            daily_seasonality=False, changepoint_prior_scale=0.05,
            interval_width=0.95
        )
        model.fit(train_p)
        future = model.make_future_dataframe(periods=test_len, freq="D")
        forecast = model.predict(future)
        return (forecast["yhat"].tail(test_len).values,
                forecast[["yhat_lower", "yhat_upper"]].tail(test_len).values)
    except Exception as e:
        print(f"Prophet failed: {e}")
        val = df_daily["demand"].iloc[-test_len-1]
        return np.full(test_len, val), np.column_stack([np.full(test_len, val-10), np.full(test_len, val+10)])


def mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / (np.abs(y_true) + 1e-8))) * 100


if __name__ == "__main__":
    print("=" * 50)
    print("  ENERGY DEMAND FORECASTING")
    print("=" * 50)

    TEST_DAYS = 30

    # Generate hourly data
    print("\n[1] Generating synthetic energy data...")
    df_hourly = generate_energy_data(n_hours=365 * 2 * 24)

    # Aggregate to daily
    df_daily = df_hourly.resample("D").mean()
    print(f"Daily data shape: {df_daily.shape}")

    # STL decomposition
    print("\n[2] STL decomposition...")
    stl_result = stl_decomposition(df_daily)

    # Time features for XGBoost
    print("\n[3] Creating ML features...")
    df_feat_hourly = create_time_features(df_hourly)
    # Aggregate features to daily for comparison
    df_feat_daily = df_feat_hourly.resample("D").mean()

    # Train/test split
    train_daily = df_daily.iloc[:-TEST_DAYS]
    test_daily = df_daily.iloc[-TEST_DAYS:]
    y_true = test_daily["demand"].values

    print(f"Train days: {len(train_daily)} | Test days: {TEST_DAYS}")

    # Models
    print("\n[4] Running models...")
    results = {}

    print("  → SARIMA...")
    sarima_pred, sarima_ci = sarima_forecast(train_daily, TEST_DAYS)
    results["SARIMA"] = (sarima_pred, sarima_ci)

    print("  → XGBoost...")
    xgb_pred = xgboost_forecast(df_feat_daily, TEST_DAYS)
    results["XGBoost"] = (xgb_pred, None)

    print("  → Prophet...")
    prophet_pred, prophet_ci = prophet_energy_forecast(df_daily, TEST_DAYS)
    results["Prophet"] = (prophet_pred, prophet_ci)

    # Metrics
    print("\n=== Forecast Metrics ===")
    metrics_rows = []
    for name, (pred, _) in results.items():
        p = pred[:TEST_DAYS]
        metrics_rows.append({
            "Model": name,
            "MAE": round(mean_absolute_error(y_true, p), 2),
            "RMSE": round(np.sqrt(mean_squared_error(y_true, p)), 2),
            "MAPE": round(mape(y_true, p), 2),
        })

    metrics_df = pd.DataFrame(metrics_rows).sort_values("RMSE")
    print(metrics_df.to_string(index=False))

    # Plot with confidence intervals
    print("\n[5] Plotting forecasts with confidence intervals...")
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(test_daily.index, y_true, "k-", linewidth=2, label="Actual", zorder=5)

    colors = {"SARIMA": "#e74c3c", "XGBoost": "#3498db", "Prophet": "#2ecc71"}
    for name, (pred, ci) in results.items():
        color = colors.get(name, "gray")
        ax.plot(test_daily.index[:len(pred)], pred[:len(y_true)],
                "--", color=color, linewidth=1.5, label=name)
        if ci is not None:
            ax.fill_between(test_daily.index[:len(pred)],
                            ci[:len(y_true), 0], ci[:len(y_true), 1],
                            alpha=0.15, color=color)

    ax.set_title("Energy Demand Forecast with 95% Confidence Intervals", fontsize=13)
    ax.set_xlabel("Date")
    ax.set_ylabel("Demand (MW)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("energy_forecasts.png", dpi=100)
    print("Forecast plot saved to energy_forecasts.png")
    plt.close()

    print("\nDone!")
