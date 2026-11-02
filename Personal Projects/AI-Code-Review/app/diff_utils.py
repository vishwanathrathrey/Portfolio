"""Patch parsing, file filtering and chunking.

The model is shown *file* line numbers next to each diff line, and findings are
only accepted for added lines, so line references cannot be invented."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import PurePosixPath

HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")
MAX_LINE_CHARS = 400

REVIEWABLE_SUFFIXES = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".rs", ".rb", ".php",
    ".c", ".h", ".cpp", ".hpp", ".cs", ".kt", ".swift", ".sh", ".sql",
}
LOCK_FILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock", "pipfile.lock",
    "cargo.lock", "composer.lock", "gemfile.lock", "go.sum",
}
GENERATED_DIRS = {
    "node_modules", "dist", "build", "vendor", "__pycache__", ".venv", "reviews", "reports",
}


@dataclass
class DiffLine:
    kind: str            # '+', '-' or ' '
    new_line: int | None
    text: str


@dataclass
class Chunk:
    filename: str
    text: str
    added: dict = field(default_factory=dict)   # new-file line number -> text
    truncated_lines: int = 0


def parse_patch(patch: str) -> list:
    """Return hunks, each a list of DiffLine carrying new-file line numbers."""
    hunks, current, new_no = [], None, 0
    for raw in (patch or "").splitlines():
        match = HUNK_RE.match(raw)
        if match:
            current = []
            hunks.append(current)
            new_no = int(match.group(1))
            continue
        if current is None or raw.startswith("\\"):
            continue
        kind, text = raw[:1], raw[1:]
        if kind == "+":
            current.append(DiffLine("+", new_no, text))
            new_no += 1
        elif kind == "-":
            current.append(DiffLine("-", None, text))
        else:
            current.append(DiffLine(" ", new_no, text))
            new_no += 1
    return hunks


def added_lines(patch: str) -> dict:
    return {l.new_line: l.text for h in parse_patch(patch) for l in h if l.kind == "+"}


def commentable_lines(patch: str) -> set:
    """Lines GitHub accepts for inline comments on the RIGHT side of the diff."""
    return {l.new_line for h in parse_patch(patch) for l in h if l.new_line is not None}


def _render(line: DiffLine) -> tuple:
    text, cut = line.text, 0
    if len(text) > MAX_LINE_CHARS:
        text, cut = text[:MAX_LINE_CHARS] + " ...[line truncated]", 1
    if line.kind == "+":
        return f"{line.new_line:>5} + {text}", cut
    if line.kind == " ":
        return f"{line.new_line:>5}   {text}", cut
    return f"      - {text}", cut


def chunk_patch(filename: str, patch: str, max_chars: int) -> list:
    """Split a patch into prompt-sized chunks without dropping any changed line.
    When a hunk is split, the last 3 rendered lines are repeated as context."""
    chunks: list = []
    state = {"lines": [], "added": {}, "trunc": 0, "size": 0}

    def flush():
        if state["added"]:
            chunks.append(
                Chunk(filename, "\n".join(state["lines"]), dict(state["added"]), state["trunc"])
            )
        state.update(lines=[], added={}, trunc=0, size=0)

    for hunk in parse_patch(patch):
        first = next((l.new_line for l in hunk if l.new_line is not None), "?")
        header = f"@@ changes near line {first} @@"
        state["lines"].append(header)
        state["size"] += len(header)
        for line in hunk:
            rendered, cut = _render(line)
            if state["size"] + len(rendered) > max_chars and state["added"]:
                tail = state["lines"][-3:]
                flush()
                state["lines"] = ["@@ (continued) @@"] + tail
                state["size"] = sum(len(x) for x in state["lines"])
            state["lines"].append(rendered)
            state["size"] += len(rendered) + 1
            state["trunc"] += cut
            if line.kind == "+":
                state["added"][line.new_line] = line.text
        flush()
    return chunks


def skip_reason(file: dict):
    """Why a changed file is not sent to the model (None means review it)."""
    name = file.get("filename", "")
    status = file.get("status", "")
    path = PurePosixPath(name)
    if status == "removed":
        return "deleted file"
    if path.name.lower() in LOCK_FILES or path.suffix == ".lock":
        return "lock file"
    if any(part in GENERATED_DIRS for part in path.parts[:-1]):
        return "generated or vendored directory"
    low = path.name.lower()
    if low.endswith((".min.js", ".min.css", ".map")) or "_pb2" in low or low.endswith(".pb.go"):
        return "generated file"
    if path.suffix.lower() not in REVIEWABLE_SUFFIXES:
        return "unsupported file type"
    if not file.get("patch"):
        if status == "renamed":
            return "renamed without content changes"
        return "no textual patch available (binary file or diff too large for the GitHub API)"
    return None
