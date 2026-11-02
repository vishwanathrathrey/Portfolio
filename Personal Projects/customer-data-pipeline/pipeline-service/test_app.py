"""Offline tests: the pipeline service against SQLite and the real mock-server app.

Run from the pipeline-service directory:  python -m pytest -q
"""
import asyncio
import importlib.util
import os
import sys
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import httpx
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import app as pipeline  # noqa: E402


def _load_mock_server():
    spec = importlib.util.spec_from_file_location("mock_app", HERE.parent / "mock-server" / "app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(autouse=True)
def sqlite_db(monkeypatch):
    engine = pipeline.create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    monkeypatch.setattr(pipeline, "engine", engine)
    monkeypatch.setattr(pipeline, "SessionLocal", pipeline.sessionmaker(bind=engine, autoflush=False))
    pipeline.Base.metadata.create_all(bind=engine)
    yield


def test_mock_server_pagination():
    client = _load_mock_server().app.test_client()
    body = client.get("/api/customers?page=2&limit=5").get_json()
    assert body["total"] == 20 and len(body["data"]) == 5 and body["page"] == 2
    assert client.get("/api/customers?page=abc").status_code == 400
    assert client.get("/api/customers/NOPE").status_code == 404


def test_ingest_and_query(monkeypatch):
    mock_client = _load_mock_server().app.test_client()

    class FakeAsyncClient:
        async def __aenter__(self): return self
        async def __aexit__(self, *a): return False
        async def get(self, url, params=None, timeout=None):
            r = mock_client.get("/api/customers", query_string=params)
            return httpx.Response(r.status_code, json=r.get_json())

    monkeypatch.setattr(pipeline.httpx, "AsyncClient", FakeAsyncClient)
    asyncio.run(pipeline.fetch_and_ingest())

    client = TestClient(pipeline.app)
    listing = client.get("/api/customers?page=1&limit=100").json()
    assert listing["total"] == 20
    first = listing["data"][0]
    assert client.get(f"/api/customers/{first['customer_id']}").json()["email"] == first["email"]
    assert client.get("/api/customers/NOPE").status_code == 404


def test_health():
    assert TestClient(pipeline.app).get("/api/health").json()["status"] == "healthy"
