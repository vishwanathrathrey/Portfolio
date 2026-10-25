"""Guardrails are cheap, deterministic, and non-LLM.

They stop the most common failure classes (empty, oversized, prompt-injection,
obviously off-topic) before we pay for a model call.
"""

from app.config import settings

BUSINESS_ALLOWED_DOC_TYPES = {
    "proposal",
    "meeting_minutes",
    "project_plan",
    "business_report",
    "technical_design",
    "sop",
    "product_spec",
}

INJECTION_MARKERS = [
    "ignore previous instructions",
    "ignore all previous",
    "disregard the above",
    "system prompt",
    "reveal your instructions",
    "you are now",
    "act as",
    "jailbreak",
]

_BUSINESS_KEYWORDS = {
    "proposal",
    "minutes",
    "plan",
    "report",
    "design",
    "sop",
    "spec",
    "document",
    "memo",
    "brief",
    "agenda",
    "policy",
}


class GuardrailError(Exception):
    """Raised when a request violates a deterministic input guardrail."""

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


def validate_request(request: str) -> None:
    """Validate a request before model execution."""
    lowered_request = request.lower()
    if not request.strip():
        raise GuardrailError("request_empty", "Request must not be empty.")
    if len(request) < 10:
        raise GuardrailError(
            "request_too_short",
            "Request must contain at least 10 characters.",
        )
    if len(request) > settings.max_request_len:
        raise GuardrailError(
            "request_too_long",
            f"Request must not exceed {settings.max_request_len} characters.",
        )
    if any(marker in lowered_request for marker in INJECTION_MARKERS):
        raise GuardrailError(
            "suspicious_input",
            "Request contains content that resembles a prompt-injection attempt.",
        )
    if not any(keyword in lowered_request for keyword in _BUSINESS_KEYWORDS):
        raise GuardrailError(
            "not_a_business_document_request",
            "Request does not appear to ask for a business document.",
        )


def detect_doc_type_hint(request: str) -> str | None:
    """Return the first matching supported document type, if any."""
    lowered_request = request.lower()
    for doc_type in sorted(BUSINESS_ALLOWED_DOC_TYPES):
        if doc_type in lowered_request or doc_type.replace("_", " ") in lowered_request:
            return doc_type
    return None
