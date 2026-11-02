"""Result objects shared by the pipeline, publisher and notifier."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone

from app.models import ReviewFinding

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def severity_rank(severity: str) -> int:
    return SEVERITY_ORDER.get(severity.lower(), 9)


@dataclass
class PRContext:
    repo: str            # "owner/name"
    number: int
    title: str
    url: str
    author: str
    head_ref: str
    base_ref: str
    head_sha: str

    @property
    def owner(self):
        return self.repo.split("/")[0]

    @property
    def name(self):
        return self.repo.split("/")[1]


@dataclass
class ReviewResult:
    ctx: PRContext
    status: str                                   # completed | failed | skipped | duplicate
    findings: list = field(default_factory=list)  # list[ReviewFinding]
    models_used: list = field(default_factory=list)
    skipped_files: list = field(default_factory=list)   # [(filename, reason)]
    limitations: list = field(default_factory=list)
    notes: list = field(default_factory=list)     # delivery problems etc.
    reviewed_files: int = 0
    error: str = ""
    completed_at: str = ""
    publish_status: str = ""      # published | already-published | disabled | failed
    email_delivered: bool = False

    def finish_now(self):
        self.completed_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, raw: str) -> "ReviewResult":
        data = json.loads(raw)
        data["ctx"] = PRContext(**data["ctx"])
        data["findings"] = [ReviewFinding(**f) for f in data["findings"]]
        data["skipped_files"] = [tuple(x) for x in data["skipped_files"]]
        return cls(**data)

    def by_severity(self):
        groups = {k: [] for k in SEVERITY_ORDER}
        for f in self.findings:
            groups.setdefault(f.severity.lower(), []).append(f)
        return groups
