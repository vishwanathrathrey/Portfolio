import re

from app.models import ReviewFinding

SECRET_PATTERNS = [
    (r"password\s*=\s*['\"].+['\"]", "Hardcoded password"),
    (r"token\s*=\s*['\"].+['\"]", "Hardcoded API token"),
    (r"secret\s*=\s*['\"].+['\"]", "Hardcoded secret"),
    (r"api_key\s*=\s*['\"].+['\"]", "Hardcoded API key"),
]


def scan_for_secrets(diff_text, filename):
    """Legacy scanner over a raw patch. NOTE: `line` is the index within the
    patch text, not a file line number; use scan_added_lines for real lines."""
    findings = []

    for index, line in enumerate(diff_text.splitlines(), start=1):
        # only scan newly added code
        if not line.startswith("+"):
            continue

        for pattern, description in SECRET_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                findings.append(
                    ReviewFinding(
                        category="security",
                        severity="Critical",
                        description=description,
                        recommendation=(
                            "Move secret to environment variables "
                            "or a secrets manager."
                        ),
                        line=index,
                        filename=filename,
                    )
                )

    return findings


def scan_added_lines(added: dict, filename: str):
    """Scan {file line number: text} of added lines. Line numbers are real file
    lines, and the secret value itself is never copied into the finding."""
    findings = []
    for line_no, text in sorted(added.items()):
        for pattern, description in SECRET_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                findings.append(
                    ReviewFinding(
                        category="security",
                        severity="Critical",
                        description=description,
                        recommendation=(
                            "Move the secret to an environment variable or secrets manager "
                            "and rotate the exposed value."
                        ),
                        line=line_no,
                        filename=filename,
                        confidence="High",
                        title=description,
                        why_it_matters=(
                            "Credentials committed to source control can be read by anyone "
                            "with access to the repository."
                        ),
                        source="scanner",
                    )
                )
    return findings
