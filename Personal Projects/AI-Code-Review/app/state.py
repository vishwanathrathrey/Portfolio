"""SQLite review-state store: duplicate prevention, status tracking, recovery.

One row per (repo, PR, head commit SHA). Claiming a row is atomic, so two
overlapping runs for the same commit cannot both review it."""
from __future__ import annotations

import sqlite3
import threading
import time
from contextlib import contextmanager
from pathlib import Path

STALE_RUNNING_SECONDS = 3600
MAX_ATTEMPTS = 3

SCHEMA = """
CREATE TABLE IF NOT EXISTS reviews (
    repo TEXT NOT NULL, pr INTEGER NOT NULL, sha TEXT NOT NULL,
    status TEXT NOT NULL, attempts INTEGER NOT NULL DEFAULT 1,
    started_at REAL NOT NULL, finished_at REAL,
    models TEXT DEFAULT '', error TEXT DEFAULT '',
    published INTEGER NOT NULL DEFAULT 0,
    emailed INTEGER NOT NULL DEFAULT 0,
    failure_notified INTEGER NOT NULL DEFAULT 0,
    report_json TEXT DEFAULT '',
    PRIMARY KEY (repo, pr, sha)
)"""
FLAGS = {"published", "emailed", "failure_notified"}


class ReviewStore:
    def __init__(self, path: str):
        self.path = path
        self._lock = threading.Lock()
        self._memory = None
        if path == ":memory:":
            self._memory = sqlite3.connect(":memory:", check_same_thread=False)
        else:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self._use() as conn:
            conn.execute(SCHEMA)

    @contextmanager
    def _use(self):
        """Serialised, auto-committing connection (closed afterwards for files)."""
        with self._lock:
            conn = self._memory or sqlite3.connect(self.path, timeout=30)
            conn.row_factory = sqlite3.Row
            try:
                with conn:  # commit on success, roll back on error
                    yield conn
            finally:
                if self._memory is None:
                    conn.close()

    def get(self, repo, pr, sha):
        with self._use() as conn:
            row = conn.execute(
                "SELECT * FROM reviews WHERE repo=? AND pr=? AND sha=?", (repo, pr, sha)
            ).fetchone()
            return dict(row) if row else None

    def claim(self, repo, pr, sha, force=False) -> bool:
        """Atomically start a review. False means: already done / in progress."""
        now = time.time()
        with self._use() as conn:
            conn.execute("BEGIN IMMEDIATE") if conn.in_transaction is False else None
            row = conn.execute(
                "SELECT * FROM reviews WHERE repo=? AND pr=? AND sha=?", (repo, pr, sha)
            ).fetchone()
            if row is None:
                conn.execute(
                    "INSERT INTO reviews (repo, pr, sha, status, started_at) VALUES (?,?,?,?,?)",
                    (repo, pr, sha, "running", now))
                return True
            reclaim = force or (
                row["status"] == "failed" and row["attempts"] < MAX_ATTEMPTS) or (
                row["status"] == "running" and now - row["started_at"] > STALE_RUNNING_SECONDS)
            if reclaim:
                conn.execute(
                    "UPDATE reviews SET status='running', attempts=attempts+1, started_at=?, "
                    "error='' WHERE repo=? AND pr=? AND sha=?", (now, repo, pr, sha))
            return reclaim

    def finish(self, repo, pr, sha, status, models=(), error="", report_json=""):
        with self._use() as conn:
            conn.execute(
                "UPDATE reviews SET status=?, finished_at=?, models=?, error=? "
                "WHERE repo=? AND pr=? AND sha=?",
                (status, time.time(), ",".join(models), error[:500], repo, pr, sha))
            if report_json:
                conn.execute(
                    "UPDATE reviews SET report_json=? WHERE repo=? AND pr=? AND sha=?",
                    (report_json, repo, pr, sha))

    def mark(self, repo, pr, sha, flag):
        if flag not in FLAGS:
            raise ValueError(flag)
        with self._use() as conn:
            conn.execute(f"UPDATE reviews SET {flag}=1 WHERE repo=? AND pr=? AND sha=?",
                         (repo, pr, sha))
