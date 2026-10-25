"""Outline-generation tool backed by the planning model."""

from typing import Any

from app.config import settings
from app.llm.ollama_client import OllamaClient
from app.tools.registry import ToolRegistry, ToolSpec
from app.utils.json_repair import JSONRepairError, safe_parse


class OutlineError(Exception):
    """Raised when an outline response is unusable."""


async def generate_outline(
    doc_type: str,
    title: str,
    topic: str,
    ollama: OllamaClient,
) -> dict[str, Any]:
    """Generate and validate a concise document outline."""
    prompt = (
        "Produce a document outline as STRICT JSON only. The JSON must have this "
        'shape: {"sections": [{"title": "...", "hint": "..."}]}. Return 4 to 8 '
        f"sections for a {doc_type} titled '{title}' about: {topic}"
    )
    try:
        response = await ollama.generate(
            model=settings.model_planner,
            prompt=prompt,
            format_json=True,
        )
        parsed = safe_parse(response, dict)
    except JSONRepairError as error:
        raise OutlineError(f"Unable to parse outline response: {error}") from error

    sections = parsed.get("sections")
    if not isinstance(sections, list) or not 4 <= len(sections) <= 8:
        raise OutlineError("Outline response must contain 4 to 8 sections.")
    if not all(
        isinstance(section, dict)
        and isinstance(section.get("title"), str)
        and isinstance(section.get("hint"), str)
        for section in sections
    ):
        raise OutlineError("Each outline section must include string title and hint fields.")
    return {"sections": sections}


def register_tool(registry: ToolRegistry) -> None:
    """Register the outline-generation tool."""
    registry.register(
        ToolSpec(
            name="generate_outline",
            description="Produce the section outline for the document.",
            args_schema={
                "doc_type": "str",
                "title": "str",
                "topic": "str",
                "ollama": "OllamaClient",
            },
            handler=generate_outline,
        )
    )
