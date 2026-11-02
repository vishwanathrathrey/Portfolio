# End-to-End Credit Risk ML System

## Overview

A credit-default prediction system built on the Kaggle **Home Credit Default Risk** dataset. A PySpark job turns standardized parquet files into a processed feature matrix, a scikit-learn script trains and selects a classifier, a **FastAPI** service serves predictions, and a **React + TypeScript (Vite)** dashboard lets a user score an applicant.

## What This Project Demonstrates

- Distributed data preparation with PySpark (type casting, deduplication, outlier handling, missing-value thresholds, quality reports)
- Model training and selection with scikit-learn pipelines (imputation, scaling, class weighting, ROC-AUC based selection)
- Model serving with FastAPI and Pydantic
- A typed React dashboard that consumes the API
- Docker / Docker Compose packaging for the API and the frontend dev server

## Architecture

```text
data/interim/*_standardized.parquet
        │  run_pipeline.py  →  pyspark/data_processor.py
        ▼
data/processed/feature_matrix_processed.parquet
        │  ml/train_model.py
        ▼
models/credit_model.pkl + models/credit_model_metrics.json
        │
        ▼
api/main.py (FastAPI, :8000)  ◄──  frontend (React/Vite, :5173, dev-server proxy)
```

| Component | Path | Notes |
|---|---|---|
| Pipeline runner | `run_pipeline.py` | Interactive menu that runs `pyspark/data_processor.py` over files in `data/interim/`; the menu offers full, sampled, and single-file runs. |
| PySpark processor | `pyspark/data_processor.py` | CLI with options such as `--sample`, `--missing-threshold`, `--dedup-keys`, `--outlier-method`. On Windows it configures `HADOOP_HOME` from the bundled `hadoop/bin` (`winutils.exe`, `hadoop.dll`). |
| Training | `ml/train_model.py` | Trains logistic regression and random forest pipelines on an 80/20 stratified split and keeps the one with the higher ROC-AUC. |
| API | `api/main.py` | FastAPI app (see below). |
| Frontend | `frontend/` | React 19, Vite 6, TypeScript; calls the API through relative URLs proxied by the Vite dev server. |

There is **no** MLflow, model registry, scheduler, Streamlit app, or CI/CD pipeline in this project; the model is a local `joblib` file.

## Prerequisites

- Python 3.12 (matches the `Dockerfile`; `pandas==3.0.1` requires Python 3.11+)
- Node.js 20+ for the frontend
- Data preparation additionally needs `pyspark` and a Java runtime. `pyspark` is intentionally **not** in `requirements.txt`, which only covers training and serving.
- The raw dataset is not committed. See `data/README.md` for the source.

## Running

### 1. Prepare data (only if you have the dataset)

```bash
pip install -r requirements.txt pyspark
python run_pipeline.py        # interactive menu; writes data/processed/
```

### 2. Train the model

```bash
python ml/train_model.py      # writes models/credit_model.pkl and models/credit_model_metrics.json
```

### 3. Start the API

```bash
uvicorn api.main:app --port 8000
```

### 4. Start the dashboard

```bash
cd frontend
npm install
npm run dev                   # http://localhost:5173
```

Set `VITE_API_BASE_URL` in `frontend/.env` (see `.env.example`) only if the API is not reached through the dev-server proxy. When unset, requests to `/health`, `/metrics`, and `/predict` are proxied to `http://localhost:8000` (override with the `API_PROXY_TARGET` environment variable).

### Docker Compose

```bash
docker compose up --build
```

Starts the API on `:8000` and the Vite dev server on `:5173` (proxying to the `api` service). The API needs `models/` and `data/processed/` to exist locally: both are mounted read-only and are not committed, so complete steps 1-2 first. The `Dockerfile` also copies `models/` and `data/` at build time.

## API

| Method & path | Description |
|---|---|
| `GET /health` | `{status, model_loaded, feature_count}`. Returns an error if the model or feature matrix is missing. |
| `GET /metrics` | Saved training metrics (`selected_model`, per-model ROC-AUC, accuracy, precision, recall, classification report). |
| `POST /predict` | Body `{"features": {<column>: <value>, ...}}`. Unknown keys are ignored and missing features are imputed by the model pipeline. Returns `{default_probability, risk_level, selected_model, missing_feature_count}`. |

`risk_level` is derived from the probability: `low` below 0.33, `medium` below 0.66, otherwise `high`. These cut-offs are fixed defaults, not calibrated business thresholds.

## Limitations

- Model quality depends entirely on the locally generated dataset; no metrics are committed with the repository, so none are claimed here.
- CORS is restricted to the local Vite origins (`localhost:5173`, `127.0.0.1:5173`).
- The model is loaded with `joblib`/pickle; only load artifacts you trained yourself.
- No authentication, input range validation, or model monitoring.
- The bundled Hadoop binaries are Windows-only helpers for running Spark locally.

## Repository Structure

```text
credit-risk-ml-system/
├── api/                # FastAPI service
├── data/               # dataset notes (data is not committed)
├── frontend/           # React + TypeScript dashboard
├── hadoop/             # Windows winutils for local Spark
├── ml/                 # model training
├── models/             # generated model artifacts (not committed)
├── pyspark/            # PySpark data processor
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── run_pipeline.py
```
