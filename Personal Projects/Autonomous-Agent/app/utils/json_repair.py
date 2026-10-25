"""Safe recovery of JSON objects and arrays from model output."""

import json
from typing import Any


class JSONRepairError(Exception):
    """Raised when a response cannot be recovered as the expected JSON type."""


def extract_json(text: str) -> dict[Any, Any] | list[Any]:
    """Extract the first JSON object or array found in text."""
    try:
        return _load_json(text, text)
    except json.JSONDecodeError:
        pass

    fenced = _strip_code_fence(text)
    if fenced != text:
        try:
            return _load_json(fenced, text)
        except json.JSONDecodeError:
            pass

    candidate = _find_bracketed_json(text)
    if candidate is not None:
        try:
            return _load_json(candidate, text)
        except json.JSONDecodeError:
            pass

    raise JSONRepairError(f"Unable to parse JSON: {text[:500]}")


def safe_parse(text: str, expected: type[Any]) -> dict[Any, Any] | list[Any]:
    """Extract JSON and verify that it has the requested top-level type."""
    parsed = extract_json(text)
    if not isinstance(parsed, expected):
        raise JSONRepairError(
            f"Expected {expected.__name__}, received {type(parsed).__name__}: {text[:500]}"
        )
    return parsed


def _load_json(
    candidate: str,
    original_text: str,
) -> dict[Any, Any] | list[Any]:
    parsed: Any = json.loads(candidate)
    if not isinstance(parsed, (dict, list)):
        raise JSONRepairError(f"Expected a JSON object or array: {original_text[:500]}")
    return parsed


def _strip_code_fence(text: str) -> str:
    stripped = text.strip()
    if not stripped.startswith("```"):
        return text
    lines = stripped.splitlines()
    if len(lines) < 2:
        return text
    if lines[-1].strip().startswith("```"):
        return "\n".join(lines[1:-1]).strip()
    return "\n".join(lines[1:]).strip()


def _find_bracketed_json(text: str) -> str | None:
    opening_indexes = [
        index for index, character in enumerate(text) if character in ("{", "[")
    ]
    for start in opening_indexes:
        opening = text[start]
        closing = "}" if opening == "{" else "]"
        depth = 0
        in_string = False
        escaped = False
        for index in range(start, len(text)):
            character = text[index]
            if in_string:
                if escaped:
                    escaped = False
                elif character == "\\":
                    escaped = True
                elif character == '"':
                    in_string = False
                continue
            if character == '"':
                in_string = True
            elif character == opening:
                depth += 1
            elif character == closing:
                depth -= 1
                if depth == 0:
                    return text[start : index + 1]
    return None
