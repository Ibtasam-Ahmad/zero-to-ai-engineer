"""
Retail Sales Forecasting
Multi-store hierarchical forecasting with Prophet, bottom-up and top-down.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings("ignore")


def generate_sales_data(n_stores=5, n_weeks=104):
    """Generate synthetic multi-store weekly sales."""
    np.random.seed(42)
    store_configs = {
        f"Store_{i+1}": {
            "base": np.random.uniform(5000, 20000),
            "trend": np.random.uniform(0.001, 0.005),
            "noise_std": np.random.uniform(200, 800),
            "seasonality_amp": np.random.uniform(500, 2000),
        } for i in range(n_stores)
    }

    dates = pd.date_range("2022-01-03", periods=n_weeks, freq="W")
    records = []

    for store, cfg in store_configs.items():
        t = np.arange(n_weeks)
        # Trend + yearly seasonality + noise
        yearly = cfg["seasonality_amp"] * np.sin(2 * np.pi * t / 52 - np.pi / 4)
        # Holiday boost (weeks 50-52 and 1)
        holiday = np.where((t % 52 >= 48) | (t % 52 <= 1), cfg["base"] * 0.3, 0)
        sales = (
            cfg["base"] * (1 + cfg["trend"] * t)
            + yearly + holiday
            + np.random.normal(0, cfg["noise_std"], n_weeks)
        ).clip(0)

        for date, s in zip(dates, sales):
            records.append({"date": date, "store": store, "sales": round(s, 2)})

    df = pd.DataFrame(records)
    print(f"Generated sales data: {df.shape} | Stores: {n_stores} | Weeks: {n_weeks}")
    return df


def mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / (np.abs(y_true) + 1e-8))) * 100


def prophet_forecast_store(df_store, test_weeks=12):
    """Forecast a single store using Prophet."""
    try:
        from prophet import Prophet
        train = df_store.iloc[:-test_weeks]
        test = df_store.iloc[-test_weeks:]

        df_p = train.rename(columns={"date": "ds", "sales": "y"})
        model = Prophet(yearly_seasonality=True, weekly_seasonality=False,
                        changepoint_prior_scale=0.05, interval_width=0.95)
        model.fit(df_p)

        future = model.make_future_dataframe(periods=test_weeks, freq="W")
        forecast = model.predict(future)
        pred = forecast["yhat"].tail(test_weeks).values
        ci = forecast[["yhat_lower", "yhat_upper"]].tail(test_weeks).values
        return pred, ci, test["sales"].values
    except Exception as e:
        val = df_store["sales"].iloc[-test_weeks-1]
        return np.full(test_weeks, val), None, df_store["sales"].iloc[-test_weeks:].values


def hierarchical_bottom_up(store_forecasts):
    """Bottom-up: sum individual store forecasts."""
    all_preds = np.array([f[0] for f in store_forecasts.values()])
    return all_preds.sum(axis=0)


def hierarchical_top_down(df, total_forecast, test_weeks=12):
    """Top-down: allocate total forecast by historical proportions."""
    # Historical proportion per store
    store_totals = df.groupby("store")["sales"].sum()
    proportions = store_totals / store_totals.sum()

    allocations = {}
    for store, prop in proportions.items():
        allocations[store] = total_forecast * prop

    return allocations, proportions


if __name__ == "__main__":
    print("=" * 50)
    print("  RETAIL SALES FORECASTING")
    print("=" * 50)

    TEST_WEEKS = 12

    # Generate data
    print("\n[1] Generating multi-store sales data...")
    df = generate_sales_data(n_stores=5, n_weeks=104)

    stores = df["store"].unique()
    print(f"\nTotal sales summary:")
    print(df.groupby("store")["sales"].agg(["mean", "sum", "std"]).round(2))

    # Forecast per store with Prophet
    print(f"\n[2] Forecasting {len(stores)} stores with Prophet...")
    store_forecasts = {}
    store_actuals = {}

    for store in stores:
        df_store = df[df["store"] == store].sort_values("date").reset_index(drop=True)
        pred, ci, actual = prophet_forecast_store(df_store, TEST_WEEKS)
        store_forecasts[store] = (pred, ci)
        store_actuals[store] = actual
        mae = mean_absolute_error(actual, pred)
        mape_val = mape(actual, pred)
        print(f"  {store}: MAE={mae:.0f}, MAPE={mape_val:.1f}%")

    # Hierarchical forecasts
    print("\n[3] Hierarchical aggregation...")

    # Bottom-up total
    bu_total = hierarchical_bottom_up(store_forecasts)
    actual_total = np.array(list(store_actuals.values())).sum(axis=0)

    print(f"Bottom-up total MAE: {mean_absolute_error(actual_total, bu_total):.0f}")
    print(f"Bottom-up total MAPE: {mape(actual_total, bu_total):.1f}%")

    # Top-down allocations
    td_allocations, proportions = hierarchical_top_down(df, bu_total, TEST_WEEKS)
    print("\nHistorical sales proportions:")
    for store, prop in proportions.items():
        print(f"  {store}: {prop:.1%}")

    # Metrics table
    print("\n=== Per-Store Forecast Metrics ===")
    rows = []
    for store in stores:
        pred = store_forecasts[store][0]
        actual = store_actuals[store]
        rows.append({
            "Store": store,
            "MAE": round(mean_absolute_error(actual, pred), 2),
            "RMSE": round(np.sqrt(mean_squared_error(actual, pred)), 2),
            "MAPE (%)": round(mape(actual, pred), 2),
        })
    metrics_df = pd.DataFrame(rows)
    print(metrics_df.to_string(index=False))

    # Plot: per-store forecast
    print("\n[4] Plotting results...")
    fig, axes = plt.subplots(3, 2, figsize=(14, 12))
    axes = axes.flatten()

    test_dates = df[df["store"] == stores[0]].sort_values("date")["date"].tail(TEST_WEEKS)

    for i, store in enumerate(stores):
        ax = axes[i]
        pred, ci = store_forecasts[store]
        actual = store_actuals[store]

        ax.plot(test_dates, actual, "k-", linewidth=2, label="Actual")
        ax.plot(test_dates, pred, "r--", linewidth=1.5, label="Forecast")
        if ci is not None:
            ax.fill_between(test_dates, ci[:, 0], ci[:, 1], alpha=0.2, color="red",
                            label="95% CI")
        ax.set_title(store)
        ax.set_ylabel("Sales ($)")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis="x", rotation=30)

    # Total in last subplot
    ax = axes[-1]
    ax.plot(test_dates, actual_total, "k-", linewidth=2, label="Actual Total")
    ax.plot(test_dates, bu_total, "b--", linewidth=1.5, label="Bottom-Up")
    ax.set_title("Total Sales (All Stores)")
    ax.set_ylabel("Sales ($)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis="x", rotation=30)

    plt.suptitle("Multi-Store Sales Forecast", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("sales_forecast.png", dpi=100)
    print("Dashboard saved to sales_forecast.png")
    plt.close()

    print("\nDone!")
