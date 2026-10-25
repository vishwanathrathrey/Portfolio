"""Lightweight in-process session memory.

Enables the session_context path in the planner so chained requests inherit
prior intent. Capped and TTL-evicted so it cannot grow unbounded.
"""

from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import uuid4


@dataclass
class SessionTurn:
    """A completed request retained for short-lived session context."""

    request: str
    summary: str
    doc_type: str
    created_at: datetime


class SessionStore:
    """A TTL- and capacity-bounded in-process store of session turns."""

    def __init__(self, max_sessions: int = 128, ttl_seconds: int = 3600) -> None:
        self._max_sessions = max_sessions
        self._ttl_seconds = ttl_seconds
        self._turns: OrderedDict[str, SessionTurn] = OrderedDict()

    def get_context(self, session_id: str) -> str | None:
        """Return concise context for a session's most recent completed turn."""
        self._evict()
        turn = self._turns.get(session_id)
        if turn is None:
            return None
        self._turns.move_to_end(session_id)
        return (
            f"previous doc_type={turn.doc_type}, last request={turn.request[:300]}, "
            f"last summary={turn.summary[:300]}"
        )

    def record(self, session_id: str, turn: SessionTurn) -> None:
        """Store the latest completed turn and refresh its LRU position."""
        self._evict()
        self._turns[session_id] = turn
        self._turns.move_to_end(session_id)
        self._evict()

    def _evict(self) -> None:
        """Remove expired turns and enforce the maximum number of sessions."""
        expires_before = datetime.now(timezone.utc) - timedelta(seconds=self._ttl_seconds)
        expired_ids = [
            session_id
            for session_id, turn in self._turns.items()
            if turn.created_at < expires_before
        ]
        for session_id in expired_ids:
            del self._turns[session_id]
        while len(self._turns) > self._max_sessions:
            self._turns.popitem(last=False)

    def new_session_id(self) -> str:
        """Create a new UUID4 session identifier."""
        return str(uuid4())


session_store = SessionStore()
