"""Offline unit tests for the deterministic parts of the review pipeline."""
import json

import pytest

from app.finding_filter import is_valid_finding, remove_duplicate_findings
from app.json_utils import extract_json
from app.models import ReviewFinding
from app.review_scope import get_pr_file_exclusion_reason, should_review_pr_file
from app.security_scanner import scan_for_secrets


def make_finding(line=1, description="Missing timeout"):
    return ReviewFinding(
        category="quality", severity="Warning", description=description,
        recommendation="Fix it", line=line, filename="app/x.py",
    )


def test_scanner_flags_only_added_lines():
    diff = '-password = "old"\n+password = "hunter2"\n+API_KEY = "abc"\n context'
    findings = scan_for_secrets(diff, "app/x.py")
    assert [f.description for f in findings] == ["Hardcoded password", "Hardcoded API key"]
    assert all(f.severity == "Critical" for f in findings)


def test_scanner_ignores_clean_code():
    assert scan_for_secrets('+password = os.getenv("PW")', "a.py") == []


def test_extract_json_strips_fences_and_prose():
    assert json.loads(extract_json('```json\n{"a": 1}\n```\nnotes')) == {"a": 1}
    assert extract_json("no json here") == "{}"


def test_finding_filter_rejects_hallucinations_and_vague_text():
    assert not is_valid_finding("No issues found in this file")
    assert not is_valid_finding("Readability can be improved")
    assert is_valid_finding("SQL query built with string concatenation")


def test_remove_duplicate_findings_keeps_first():
    unique = remove_duplicate_findings([make_finding(), make_finding(), make_finding(line=2)])
    assert [f.line for f in unique] == [1, 2]


@pytest.mark.parametrize("name,reason", [
    ("README.md", "non-python-file"),
    ("tests/test_a.py", "test-file"),
    ("app/service.py", None),
    ("test_a.py", "test-file"),
    ("reviews/a.py", "generated-artifact-directory"),
])
def test_pr_file_scope(name, reason):
    assert get_pr_file_exclusion_reason(name) == reason
    assert should_review_pr_file(name) == (reason is None)
