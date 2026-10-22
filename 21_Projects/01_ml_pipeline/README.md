# Project 01: ML Pipeline (diabetes progression predictor)

> **Difficulty:** Beginner-friendly capstone · **Time:** 1-3 hours (plus a 10-30 minute install) · **Runs on:** CPU, no API key needed

## 1. What this project does

This is a complete, small machine learning system from start to finish:

1. **Train:** it loads scikit-learn's built-in *diabetes* dataset (442 patients, 10 medical measurements each) and trains four models that try to predict a "disease progression score" one year later (a number roughly between 25 and 346).
2. **Compare and choose:** it measures how good each model is on patients it has not seen, records every experiment with **MLflow** (a tool that keeps a lab notebook of your training runs), and keeps the best one. It also measures how wrong the model typically is, so it can give an honest **prediction interval** (a range that should contain the true value 90% of the time).
3. **Serve:** a **FastAPI** web server loads the saved model and answers prediction requests. A small web page lets you type in the 10 values and see the prediction.

Predicting a number (instead of a category) is called **regression**.

**What you will learn**

- The *train, evaluate, select, save, serve* loop that almost every ML product follows.
- scikit-learn **Pipelines** (scaling + model glued together so they are always used together).
- Regression metrics: **MAE**, **RMSE** and **R²** (explained in section 5).
- **Cross-validation**, experiment tracking with MLflow, and a simple, honest prediction interval.
- Saving models with `joblib` and serving them behind a FastAPI endpoint with input validation.

## 2. Folder contents

| File | Purpose |
|---|---|
| `main.py` | The full training pipeline: trains LinearRegression, Ridge, RandomForest and XGBoost, logs each run to MLflow, picks the best by R², computes the 90% prediction interval, saves `models/best_model.joblib` and `models/model_meta.joblib`. **Start with this one.** |
| `train.py` | A command-line trainer for *one* model, e.g. `python train.py --model-type Ridge`. Writes the same two files, so the API can use either script. |
| `api.py` | The FastAPI server: `GET /health`, `GET /model-info`, `POST /predict`, and `GET /` (the web page). |
| `templates/index.html` | The web page with the 10 input boxes and the result card. |
| `requirements.txt` | The Python packages (pinned versions) the project needs. |
| `notes/01_ml_pipeline.md` | A longer explanation of the ideas behind the project. |

Created when you run it:

| Folder | Created by | What is inside |
|---|---|---|
| `models/` | `main.py` / `train.py` | The saved model and its metadata (name, scores, feature names, interval). |
| `mlruns/` | MLflow, during `main.py` (in the folder you run it from) | One folder per training run with its parameters, scores and a copy of the model. |

## 3. Prerequisites

Finish these first (paths are relative to the repo root):

- `03_Machine_Learning/00_start_here_your_first_ml_model.ipynb`
- `03_Machine_Learning/01_supervised/01_linear_regression.ipynb`, `04_ensemble_methods.ipynb` and `09_pipeline_and_leakage.ipynb`
- `15_MLOps/01_experiment_tracking/01_mlflow.ipynb` (what MLflow is)
- `12_FastAPI/01_fastapi_intro.ipynb` to `03_ml_serving_with_fastapi.ipynb`
- Optional, for the interval idea: `03_Machine_Learning/14_conformal_prediction/`

**Python:** tested with **Python 3.12**. Use 3.10, 3.11 or 3.12; the pinned `numpy==1.26.4` has no ready-made packages for newer Python versions.

**Disk and network:** the install downloads about 70 packages. The finished virtual environment was about **1.6 GB** (XGBoost alone pulls in a large NVIDIA library on Linux, even if you have no GPU).

## 4. How to run it (tested step by step)

Every step below was run on Linux with Python 3.12 in a fresh virtual environment, and the outputs shown are the real outputs. Commands are for **macOS/Linux**; Windows versions are given where they differ. **Run every command from inside this folder**: the code uses relative paths like `models/...` and `templates/index.html`.

### Step 1: Create a virtual environment

```bash
cd 21_Projects/01_ml_pipeline
python3 -m venv .venv
source .venv/bin/activate          # Windows (PowerShell): .venv\Scripts\Activate.ps1
                                   # Windows (cmd):        .venv\Scripts\activate.bat
```

### Step 2: Install the packages

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This finished with no errors or version conflicts (a `pip install --dry-run -r requirements.txt` also resolves cleanly).

### Step 3: Train the models

```bash
python main.py
```

Real output (shortened). You should see these numbers or very close ones; they are fixed by `random_state=42`:

```
INFO - Loaded dataset: 442 samples, 10 features
INFO -   LinearRegression: MAE=42.79, RMSE=53.85, R²=0.4526
INFO -   Ridge: MAE=42.81, RMSE=53.78, R²=0.4541
INFO -   RandomForest: MAE=44.17, RMSE=54.40, R²=0.4415
INFO -   XGBoost: MAE=46.39, RMSE=57.89, R²=0.3675
INFO - 90% prediction interval: pred -93.1 .. pred +97.7 (covered 94% of test patients)
INFO - Best model: Ridge (R²=0.4541)
INFO - Saved to models/best_model.joblib
Best model saved: Ridge
```

It took about 70 seconds on our (busy) test machine. The `WARNING mlflow.models.model: Model logged without a signature and input example` lines are harmless.

**What just happened?**

- The simple Ridge model won. An R² of about 0.45 means the model explains roughly 45% of the differences between patients: useful, but far from perfect. A fancier model (XGBoost) is not automatically better.
- The interval line says: for a new patient, the true score is usually between *prediction minus 93* and *prediction plus 98*. That is wide, and that is the honest truth about a model with R² 0.45. On the 89 test patients the interval contained the true value 94% of the time (the target was 90%).

You can also train a single model: `python train.py --model-type RandomForest` (real output: `Results MAE: 44.17 | RMSE: 54.40 | R²: 0.4415`, `90% interval: pred -90.3 .. pred +99.0 (covered 93% of test patients)`, `Model saved to models/best_model.joblib`; the metadata goes to `models/model_meta.joblib`). Restart the server afterwards so it loads the new model.

### Step 4 (optional): Look at the experiments in MLflow

```bash
mlflow ui --port 5000
```

Open **http://localhost:5000**, click the `diabetes_prediction` experiment, and compare the runs side by side. (We tested this on another port: the page loaded and listed the runs `LinearRegression`, `Ridge`, `RandomForest`, `XGBoost`.) Stop it with `Ctrl+C`. Every time you run `main.py` again, four more runs are added.

### Step 5: Start the API server

```bash
uvicorn api:app --port 8000
```

Wait for `Application startup complete.` If port 8000 is already used by another program you will see `address already in use`: choose another number, for example `--port 8001`, and use it in every URL below. (`python api.py` also works, but it always uses port 8000 with auto-reload.)

Leave this terminal running and open a **second** terminal for the next steps.

### Step 6: Open the web page

Go to **http://localhost:8000/**. The "Model Information" card shows the winning model and its scores. Click **Predict** to send the pre-filled example patient; the result card shows the score and the 90% prediction interval. You can also test every endpoint by hand at **http://localhost:8000/docs**.

### Step 7: Try the API with curl

On Windows PowerShell type `curl.exe` instead of `curl`, or use the `/docs` page, which avoids quoting problems.

**Health check**

```bash
curl http://localhost:8000/health
```
```json
{"status":"ok","model_loaded":true}
```

(Before training, or if a model file is missing, you get `{"status":"ok","model_loaded":false}` and the other endpoints answer HTTP 503 `{"detail":"Model not found. Run main.py first."}`.)

**Model information** (shortened)

```bash
curl http://localhost:8000/model-info
```
```json
{"model_name":"Ridge",
 "metrics":{"MAE":42.81199941834888,"RMSE":53.777454065343896,"R2":0.45414652070698225},
 "feature_names":["age","sex","bmi","bp","s1","s2","s3","s4","s5","s6"],
 "all_results":{"LinearRegression":{...},"Ridge":{...},"RandomForest":{...},"XGBoost":{...}}}
```

**A prediction**

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"age":0.038,"sex":0.05,"bmi":0.062,"bp":-0.025,"s1":-0.044,"s2":-0.034,"s3":-0.043,"s4":-0.002,"s5":0.019,"s6":-0.017}'
```
```json
{"prediction":193.76,"prediction_lower":100.66,"prediction_upper":291.49,"interval_level":0.9,"model_used":"Ridge",
 "features_received":{"age":0.038,"sex":0.05,"bmi":0.062,"bp":-0.025,"s1":-0.044,"s2":-0.034,"s3":-0.043,"s4":-0.002,"s5":0.019,"s6":-0.017}}
```

Read it as: "best guess 193.8; with 90% confidence the true score is between 100.7 and 291.5".

Note that the inputs are small numbers like `0.038`, not "age 50". The diabetes dataset in scikit-learn is already **standardised** (each column was centred around 0 and scaled; every value lies between about -0.14 and 0.20), so the API expects values in that same scaled form and rejects anything outside -0.5 to 0.5:

```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
  -d '{"age":50,"sex":1,"bmi":30,"bp":120,"s1":200,"s2":100,"s3":50,"s4":4,"s5":5,"s6":90}'
```
```json
{"detail":[{"type":"less_than_equal","loc":["body","age"],"msg":"Input should be less than or equal to 0.5","input":50,"ctx":{"le":0.5}}, ...]}
```

(HTTP status 422. Missing fields are rejected the same way, with `"msg":"Field required"`.)

### Step 8: Stop the server

Press `Ctrl+C` in the server terminal.

## 5. How it works

```
 OFFLINE (python main.py)                              ONLINE (uvicorn api:app)
 ------------------------                              ------------------------
 load_diabetes()  442 rows x 10 columns                browser form / curl
        |                                                      |
 train_test_split  80% train / 20% test                        v
        |                                              POST /predict
 for each of 4 models:                                         |
   Pipeline = StandardScaler -> model                  Pydantic checks the 10 fields
   fit on train, score on test (MAE, RMSE, R²)         (present, numbers, between -0.5 and 0.5)
   5-fold cross-validation on all data                         |
   log params + scores + model to MLflow (mlruns/)             v
        |                                              get_model(): load models/*.joblib
 pick the highest R²                                   once, keep in memory
        |                                                      |
 cross-validated residuals -> 5% and 95% quantiles             v
        |                                              model.predict()
 joblib.dump  ->  models/best_model.joblib  ---------->        |
                  models/model_meta.joblib  ---------->  prediction + interval offsets
                                                               |
                                                               v
                                         JSON: prediction, 90% interval, model name
```

The three scores, in plain English (the target is a score from about 25 to 346):

| Metric | Meaning | Ridge result |
|---|---|---|
| **MAE** (mean absolute error) | On average, how far off is the prediction? | about 43 points |
| **RMSE** (root mean squared error) | Like MAE, but big mistakes count extra | about 54 points |
| **R²** | Share of the patient-to-patient differences the model explains (1.0 = perfect, 0 = no better than always guessing the average) | about 0.45 |

**How the prediction interval is made** (`compute_interval` in `main.py`): the model is trained 5 times on 4/5 of the training data and asked to predict the remaining 1/5 it has never seen (`cross_val_predict`). For every training patient we now have an honest error, a **residual** = true value minus prediction. The 5% and 95% quantiles of those residuals (about -93 and +98) are stored in `model_meta.joblib`. At prediction time the API adds them to the prediction. This is a simple version of **conformal prediction**.

The training half and the serving half only share the files in `models/`. You can retrain at any time; the server picks up the new model after a restart (it keeps the first model it loaded in memory).

## 6. Known limitations

These are not bugs, but things to keep in mind (all checked on the test machine):

1. **The interval has the same width for every patient.** It is a 90% interval *on average*, built from one set of residuals, so it does not get narrower for "easy" patients or wider for unusual ones. On 89 test patients it covered 94%; on a different split the number will differ a little.
2. **Inputs must be standardised values.** The API only accepts numbers between -0.5 and 0.5, because that is the form of the training data. Entering a real age or blood pressure is not possible without rebuilding the project on `load_diabetes(scaled=False)` (see exercise 5).
3. **The server keeps the model in memory.** After retraining, restart the server to load the new model.
4. **Use the pinned MLflow version.** With newer MLflow 3.x, saving the XGBoost model to MLflow is refused for security reasons. `main.py` now prints `Could not log XGBoost model to MLflow (MlflowException); continuing.` and still logs its scores and finishes normally (tested with MLflow 3.14), but that run then has no model copy in the MLflow UI.
5. **Large install for a small project.** XGBoost brings a big NVIDIA library on Linux. If disk space is tight, uninstall `xgboost`: `main.py` then simply skips that model.
6. **Run from this folder.** `models/` and `templates/index.html` are found relative to the folder you start the scripts and the server from. Started elsewhere, you get "Model not found" or an error on `/`.
7. **`python api.py` always uses port 8000.** Use `uvicorn api:app --port <number>` to pick another port.
8. **The web page needs the internet for styling.** It loads Bootstrap from a CDN; offline it still works but looks plain.

### What was fixed (October 2026)

| Problem in the original code | Fix |
|---|---|
| `train.py` saved its metadata as `model_meta_meta.joblib`, so the API crashed (HTTP 500) after `train.py` and showed the wrong model name after `main.py` + `train.py` | `train.py` now writes `models/model_meta.joblib` |
| The "±10% band", labelled "95% CI" on the page, was made up (`pred * 0.10`) and upside down for negative predictions | Replaced by a real 90% prediction interval from cross-validated residuals |
| `/health` reported `model_loaded: true` when the metadata file was missing | Both files must load before the model counts as loaded |
| Any number was accepted (`age: 50` gave a prediction of -37323) | Inputs are limited to -0.5 ... 0.5 (HTTP 422 otherwise); the page shows the validation message |
| Feature-name `UserWarning` on every prediction; Pydantic `model_` namespace warnings | The API passes a DataFrame with column names; warnings fixed |
| `main.py` crashed with MLflow 3.x | Logging the model is now optional (scores are still logged) |

## 7. Ideas to extend it

1. **Easy:** add `Lasso` and `ElasticNet` to `build_models()` in `main.py`, run it again, and compare all runs in the MLflow UI.
2. **Easy:** change `INTERVAL_LEVEL` in `main.py` to 0.8 and to 0.95, retrain, and see how the interval width and the test coverage change.
3. **Medium:** add a test with FastAPI's `TestClient` (from `fastapi.testclient import TestClient`) that checks `/predict` returns HTTP 422 for `age: 50` and HTTP 200 for the example patient.
4. **Medium:** make the interval depend on the patient: train a second model that predicts the *size* of the residual, and scale the interval with it.
5. **Harder:** rebuild the project on the unscaled data (`load_diabetes(scaled=False)`), so users can type real ages and blood pressures, and update the field limits and the web page.
