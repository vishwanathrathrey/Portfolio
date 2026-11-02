# Customer Data Pipeline

## Overview

A small containerized ETL pipeline. A **Flask mock server** exposes paginated customer data (loaded from a JSON file), and a **FastAPI pipeline service** pulls every page over HTTP, stores the records in **PostgreSQL** via SQLAlchemy, and serves them back through its own paginated REST API.

## What This Project Demonstrates

- API-based ingestion with pagination (`httpx`, async)
- ETL into a relational store (SQLAlchemy 2.x ORM, PostgreSQL)
- Two-service architecture orchestrated with Docker Compose, including health checks
- FastAPI background tasks, dependency-injected DB sessions, and input validation
- Offline tests that run the real services against SQLite

## Architecture

```text
customers.json -> mock-server (Flask, :5000) --HTTP pages--> pipeline-service (FastAPI, :8000) -> PostgreSQL (:5432)
```

| Service | Tech | Port | Role |
|---|---|---|---|
| `mock-server` | Flask 3.1 | 5000 | Serves `data/customers.json` (20 records) with `page`/`limit` pagination |
| `pipeline-service` | FastAPI, SQLAlchemy 2.0, httpx | 8000 | Ingests from the mock server into PostgreSQL and exposes the stored data |
| `postgres` | PostgreSQL 15 | 5432 | `customers` table (created automatically at service start-up) |

## Running

```bash
docker compose up --build
```

Then:

```bash
curl -X POST http://localhost:8000/api/ingest              # start ingestion (runs in the background)
curl "http://localhost:8000/api/customers?page=1&limit=10" # list ingested customers
curl http://localhost:8000/api/customers/CUST001           # single customer
curl http://localhost:8000/api/health
```

## API

### Mock server (`:5000`)

| Method & path | Description |
|---|---|
| `GET /api/customers?page=1&limit=10` | Paginated customers. `limit` is capped at 100. Non-integer values return `400`. |
| `GET /api/customers/{customer_id}` | One customer, or `404`. |
| `GET /api/health` | Liveness check. |

### Pipeline service (`:8000`)

| Method & path | Description |
|---|---|
| `POST /api/ingest` | Starts a background job and returns immediately (`{"status": "success", "message": ...}`). The job **clears the `customers` table first**, then loads all pages. Progress and totals are written to the service log. |
| `GET /api/customers?page=1&limit=10` | Paginated customers from PostgreSQL (`limit` 1-100). Response: `{data, total, page, limit}`. |
| `GET /api/customers/{customer_id}` | One stored customer, or `404`. |
| `GET /api/health` | Liveness check (used by the Compose health check). |

## Tests

The tests exercise the mock server's pagination and a full ingest-and-query round trip against an in-memory SQLite database (no Docker or PostgreSQL needed).

```bash
cd pipeline-service
pip install -r requirements.txt -r ../mock-server/requirements.txt pytest
python -m pytest -q
```

## Known Limitations

- Credentials in `docker-compose.yml` (`postgres` / `password`) are for local development only.
- Ingestion is a full reload (delete, then insert); it is not incremental or idempotent per record, and a failure partway through leaves a partial table.
- `POST /api/ingest` has no job-status endpoint; check the container logs for the result.
- Only the Python dependencies in each `requirements.txt` are pinned; the pipeline service pins older FastAPI/SQLAlchemy releases that were not upgraded as part of this review.

## Repository Structure

```text
customer-data-pipeline/
├── docker-compose.yml
├── mock-server/
│   ├── app.py
│   ├── data/customers.json
│   ├── Dockerfile
│   └── requirements.txt
└── pipeline-service/
    ├── app.py
    ├── test_app.py
    ├── Dockerfile
    └── requirements.txt
```
