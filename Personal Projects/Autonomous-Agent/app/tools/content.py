"""Section-content generation tool backed by the writing model."""

import re

from app.config import settings
from app.llm.ollama_client import OllamaClient, OllamaError
from app.llm.prompts import section_writer_system_prompt, section_writer_user_prompt
from app.tools.registry import ToolRegistry, ToolSpec


async def generate_section_content(
    doc_type: str,
    doc_title: str,
    section_title: str,
    data_block: str,
    ollama: OllamaClient,
) -> str:
    """Write normalized prose for one document section."""
    try:
        content = await ollama.generate(
            model=settings.model_writer,
            prompt=section_writer_user_prompt(
                doc_type=doc_type,
                doc_title=doc_title,
                section_title=section_title,
                data_block=data_block,
            ),
            system=section_writer_system_prompt(),
            temperature=0.4,
            num_predict=400,
        )
    except OllamaError as error:
        return f"(Content unavailable: {error})"
    return _normalize_content(content)


def _normalize_content(content: str) -> str:
    normalized = (
        content.replace(r"\(", "")
        .replace(r"\)", "")
        .replace(r"\[", "")
        .replace(r"\]", "")
        .replace(r"\$", "$")
    )
    normalized = re.sub(
        r"^\s*(?:Section|Title):[^\n]*\n?",
        "",
        normalized,
        flags=re.IGNORECASE,
    )
    normalized = re.sub(r"^\s*#+\s*", "", normalized)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.strip()


def register_tool(registry: ToolRegistry) -> None:
    """Register the section-content generation tool."""
    registry.register(
        ToolSpec(
            name="generate_section_content",
            description="Write prose for a single document section.",
            args_schema={
                "doc_type": "str",
                "doc_title": "str",
                "section_title": "str",
                "data_block": "str",
                "ollama": "OllamaClient",
            },
            handler=generate_section_content,
        )
    )
