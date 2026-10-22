# Project 04: Forecasting Dashboard

A web dashboard that predicts the next days of a **time series** (a list of numbers measured over time, such as daily sales). It runs four very different forecasting models on the same data and draws their predictions side by side:

| Model | Family | Idea in one line |
|---|---|---|
| **ARIMA** | Classical statistics | The next value is a weighted mix of recent values and recent errors |
| **Prophet** | Trend + seasonality | Split the series into trend + weekly + yearly patterns, then extend them |
| **XGBoost** | Machine learning (trees) | Use the last 14 values as input features and predict the next one, again and again |
| **LSTM** | Deep learning | A recurrent neural network reads the last 14 values and predicts the next one |

Each forecast comes with a **confidence interval**: a shaded band meaning "we expect the real value to land somewhere in here".

| | |
|---|---|
| **What you will learn** | How the four model families forecast; turning a series into a supervised problem with **lag features** (past values used as inputs); forecasting several steps ahead by feeding predictions back in; honest evaluation (score on a hold-out, then refit on all data before forecasting); serving models with FastAPI |
| **Difficulty** | Beginner to intermediate |
| **Time needed** | About 1 hour to run and read; 1-2 more hours for the exercises |
| **Runs on** | CPU, no API key. The web page loads Bootstrap and Chart.js from a CDN, so the browser needs internet to draw the chart |

---

## 1. What is in this folder

| File | What it does |
|---|---|
| `main.py` | The forecasting engine: `generate_sample_data()` makes 365 days of synthetic data (trend + yearly and weekly waves + random noise, seeded so it is the same every time); one function per model (`forecast_arima`, `forecast_prophet`, `forecast_xgboost`, `forecast_lstm`); `_mock_forecast()` used if a model fails; `run_forecast()` runs the models you ask for |
| `api.py` | FastAPI server: `GET /sample-data`, `POST /forecast`, `POST /upload-data`, `GET /models`, `GET /health`, `GET /` (the dashboard) |
| `templates/index.html` | The dashboard: horizon slider (7-90 days), model check boxes, chart with shaded confidence bands, comparison table, CSV upload |
| `requirements.txt` | Pinned libraries: FastAPI, uvicorn, pandas, scikit-learn, statsmodels (ARIMA), prophet + cmdstanpy, xgboost, torch (LSTM), python-multipart (file upload) |
| `notes/04_forecasting_dashboard.md` | Longer explanation of the concepts |

---

## 2. Before you start (prerequisites)

**Notebooks to finish first** (paths are relative to this folder):

- [`../../04_Forecasting/01_time_series_basics.ipynb`](../../04_Forecasting/01_time_series_basics.ipynb) (trend, seasonality, train/test split in time)
- [`../../04_Forecasting/02_classical_methods.ipynb`](../../04_Forecasting/02_classical_methods.ipynb) (ARIMA)
- [`../../04_Forecasting/03_ml_for_forecasting.ipynb`](../../04_Forecasting/03_ml_for_forecasting.ipynb) (lag features, XGBoost)
- [`../../04_Forecasting/04_deep_learning_forecasting.ipynb`](../../04_Forecasting/04_deep_learning_forecasting.ipynb) (LSTM)
- [`../../04_Forecasting/05_prophet.ipynb`](../../04_Forecasting/05_prophet.ipynb)
- [`../../12_FastAPI/01_fastapi_intro.ipynb`](../../12_FastAPI/01_fastapi_intro.ipynb)

**Python version:** 3.10, 3.11 or 3.12. `pip install --dry-run -r requirements.txt` resolves with no conflicts on Python 3.12. Python 3.13 or newer will not work with these pins (`numpy==1.26.4` and `torch==2.4.1` have no 3.13 builds).

**API keys:** none.

---

## 3. Run it step by step

Run every command from inside this folder (`21_Projects/04_forecasting_dashboard`). `api.py` opens `templates/index.html` with a relative path and imports `main.py` from the current folder.

### Step 1: Create and activate a virtual environment

A **virtual environment** is a private folder of libraries for one project, so its pinned versions don't clash with other projects.

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 2: Install the libraries

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

💡 **Tip (Linux, CPU only):** on Linux, `torch==2.4.1` from PyPI also downloads about 13 `nvidia-*` CUDA packages (several GB). The CPU build is much smaller:

```bash
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
```

`xgboost==2.1.1` on Linux still pulls `nvidia-nccl-cu12` (about 350 MB), so expect a large download either way. On Windows and macOS, the normal PyPI torch is already CPU-only.

### Step 3: (Optional) try the engine without the web server

```bash
python -c "import main; df = main.generate_sample_data(); r = main.run_forecast(df, horizon=7, models=['arima']); print(r[0]['model'], [round(x, 1) for x in r[0]['forecast']], r[0]['mae'])"
```

Output I got (the sample data is seeded, so yours should match closely):

```
ARIMA [120.4, 120.6, 118.5, 115.7, 114.4, 115.3, 117.5] 2.368
```

### Step 4: Start the server

`python api.py` starts on **port 8003** with auto-reload (`api.py`, last line). To choose your own port (for example, if 8003 is busy):

```bash
python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000/>, choose a horizon and models, and click **▶ Forecast**. The forecasts start the day after the last date in the chart, each with a shaded band. Upload a CSV with columns `ds` (date) and `y` (number), and the next **▶ Forecast** forecasts *your* data (at least 40 rows).

### Step 5: Try the API with curl

On Windows PowerShell, use `curl.exe`, and put JSON bodies in a file and send them with `-d @body.json`.

```bash
curl http://127.0.0.1:8000/health
# {"status":"ok"}
curl http://127.0.0.1:8000/sample-data
# {"dates":["2022-01-01", ... ,"2022-12-31"],"values":[100.609,102.051,106.82, ... ,117.778]}   (same every call)
```

Forecast 3 days with ARIMA:

```bash
curl -X POST http://127.0.0.1:8000/forecast -H "Content-Type: application/json" \
     -d '{"horizon":3,"models":["arima"]}'
```
```json
{"horizon":3,"results":[{"model":"ARIMA","forecast":[120.43,120.62,118.46],"lower":[115.45,114.54,112.33],"upper":[125.41,126.70,124.60],"mae":2.641}]}
```

(The real numbers have more decimals.) All four models with `{"horizon":7}`, summarised. The last real value is 117.78 on 2022-12-31:

```
ARIMA    first=120.43  last=117.52  mae 2.368
Prophet  first=122.48  last=119.78  mae 1.858
XGBoost  first=115.48  last=114.40  mae 2.56
LSTM     first=115.07  last=114.93  mae None
```

`mae` is the mean absolute error of a copy of the model trained on the first 80% and scored on the next `horizon` days of the last 20%. The LSTM doesn't compute one.

Forecast your own series: send `dates` and `values` (this is what the dashboard does after an upload):

```bash
curl -X POST http://127.0.0.1:8000/forecast -H "Content-Type: application/json" \
     -d '{"horizon":7,"models":["arima"],"dates":["2024-01-01", ...],"values":[1000.63, ...]}'
```

With a 120-day series around 1000-1240, ARIMA forecast `[1263.6, 1266.6, 1250.7, 1227.9, 1215.3, 1222.2, 1243.3]`.

Errors you can trigger on purpose:

| Request | Response |
|---|---|
| `{"horizon":0}` | HTTP 422, `"Input should be greater than or equal to 1"` (allowed range: 1-365) |
| `values` with only 10 numbers | HTTP 400, `{"detail":"Need at least 40 values to forecast, got 10"}` |
| upload a CSV without `ds`/`y` columns | HTTP 400, `{"detail":"CSV must have 'ds' (date) and 'y' (value) columns"}` |

Stop the server with `Ctrl+C`.

**How this was verified:** I ran it on Python 3.12, using newer library versions than the pins (FastAPI 0.138, NumPy 2.4, statsmodels 0.14.6, xgboost 3.3, torch 2.12 CPU, prophet 1.1.6 with cmdstanpy 1.2.5). The numbers above are from that run. I also took a headless-Chrome screenshot of the dashboard: the shaded bands appear and start after 2022-12-31. On a busy machine the first `/forecast` with all four models can take a minute or more (the LSTM trains on every request).

---

## 4. How it works

```
 browser                          api.py                          main.py
 ───────                          ──────                          ───────
 page load ── GET /sample-data ─► generate_sample_data(365) ───► same seeded series every time

 (optional) upload CSV ─ POST /upload-data ─► check ds/y columns, echo dates + values back

 ▶ Forecast ─ POST /forecast ───► {horizon, models, dates, values}
                                   no values? → sample series
                                   run_forecast(df, horizon, models)
                                     ├─ ARIMA    score on 80/20 split, refit on ALL data, forecast
                                     ├─ Prophet  score on 80/20 split, refit on ALL data, forecast
                                     ├─ XGBoost  14 lag features → predict step by step
                                     └─ LSTM     14-day windows → predict step by step
                                   each returns {model, forecast, lower, upper, mae, note?}
                                   (a failing model → _mock_forecast with a note)
 chart: history, then each forecast from the day after the last date,
        shaded band = lower ... upper
```

Key ideas:

- **Evaluate, then refit.** To get an honest error score, a model is trained on the first 80% and tested on data it hasn't seen. For the *real* forecast it is retrained on everything, so the forecast continues from the last real date.
- **Lag features (XGBoost):** for every day, the input is the previous 14 values and the target is today's value. To forecast 30 days, the model predicts day 1, appends that prediction to the history, predicts day 2, and so on.
- **Residual-based intervals (XGBoost, LSTM):** the spread (standard deviation) of the errors on the held-out 20%, times 1.96, gives an approximate 95% band. ARIMA and Prophet compute their own intervals.

---

## 5. Known issues and limitations

- **XGBoost can't follow a trend outside the values it has seen.** Tree models predict averages of training values, so on a rising series the forecast goes flat. With the 120-day upload above, XGBoost predicted 1210.2 for every day while ARIMA kept following the series. This is a property of trees, not a bug, and a good discussion point.
- **The LSTM is small and briefly trained** (50 full-batch steps), so its forecast is usually flatter than the data. It is also retrained on every request, which is slow on a busy CPU.
- **Uploaded data is assumed to be daily.** The chart and Prophet both add *days* after your last date. Weekly or monthly data still gets forecasts, but the future dates on the x-axis will be daily.
- **A failing model falls back to a "mock" forecast** (last value + noise) with a note in the table. Check the server log for the `WARNING:main:... failed:` line that says why.
- **The card headings on the dashboard are hard to read** (dark text on a dark background). This is cosmetic only.
- **Not verified:** a fresh `pip install -r requirements.txt` followed by running the server on exactly the pinned versions. The pins were checked with `pip install --dry-run` only (no conflicts); the code was run on the newer versions listed above.

---

## 6. Ideas to extend it

1. **Easy: a seasonal baseline.** Add a fifth "model": "same value as 7 days ago". If a fancy model can't beat this baseline, it isn't earning its complexity.
2. **Easy-medium: sMAPE.** `main.py` defines `smape()` but never uses it. Compute it next to MAE for every model and show both in the table.
3. **Medium: check the bands.** Using the 80/20 split, count how many of the held-out points fall inside each model's band. A 95% band should contain roughly 95% of them.
4. **Medium: fix the trend problem for XGBoost.** Train it on *differences* (`y[t] - y[t-1]`) instead of raw values, then add the predicted differences back up. Compare the forecast on the uploaded 120-day series.
5. **Harder: model files instead of retraining.** Train each model once (for example at start-up or via a `POST /train` endpoint), save it, and make `/forecast` only predict. Measure how much faster requests become.
