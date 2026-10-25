"""Planner converts a natural-language request into a typed Plan.

Semantic repairs after Pydantic validation guarantee the executor's required
invariants (outline first, render last) without rejecting otherwise-usable plans.
"""

import logging
from typing import Any

from pydantic import ValidationError

from app.config import settings
from app.llm.ollama_client import OllamaClient
from app.llm.prompts import planner_system_prompt, planner_user_prompt
from app.schemas import Plan, Todo, TodoStatusEnum
from app.utils.json_repair import JSONRepairError, safe_parse

logger = logging.getLogger(__name__)


class PlanValidationError(Exception):
    """Raised when the planner cannot produce a schema-valid plan."""


async def plan(
    request: str,
    ollama: OllamaClient,
    session_context: str | None = None,
) -> Plan:
    """Generate, validate, and semantically repair a document plan."""
    prompt = planner_user_prompt(request, session_context)
    try:
        generated = await _generate_plan(prompt, ollama)
        validated_plan = _validate_plan(generated)
    except ValidationError as error:
        corrective_prompt = (
            f"{prompt}\n\nYour previous output failed validation: {error.errors()}. "
            "Return valid JSON matching the schema."
        )
        try:
            generated = await _generate_plan(corrective_prompt, ollama)
            validated_plan = _validate_plan(generated)
        except (JSONRepairError, ValidationError) as retry_error:
            raise PlanValidationError(
                f"Planner output remained invalid after retry: {retry_error}"
            ) from retry_error
    except JSONRepairError as error:
        raise PlanValidationError(f"Planner returned invalid JSON: {error}") from error

    _ensure_outline_first(validated_plan, request)
    _ensure_render_last(validated_plan)
    _renumber_todos(validated_plan)
    _clear_invalid_dependencies(validated_plan)
    return validated_plan


async def _generate_plan(prompt: str, ollama: OllamaClient) -> dict[str, Any]:
    text = await ollama.generate(
        model=settings.model_planner,
        prompt=prompt,
        system=planner_system_prompt(),
        format_json=True,
        temperature=0.1,
        num_predict=1024,
    )
    parsed = safe_parse(text, dict)
    return parsed


def _validate_plan(raw: dict[str, Any]) -> Plan:
    return Plan.model_validate(raw)


def _ensure_outline_first(plan: Plan, request: str) -> None:
    outlines = [todo for todo in plan.todos if todo.tool == "generate_outline"]
    outline = outlines[0] if outlines else _new_outline_todo(plan, request)
    plan.todos = [outline, *(todo for todo in plan.todos if todo.tool != "generate_outline")]


def _new_outline_todo(plan: Plan, request: str) -> Todo:
    return Todo(
        id=0,
        description="Generate the document section outline.",
        tool="generate_outline",
        tool_args={
            "doc_type": plan.doc_type.value,
            "title": plan.title,
            "topic": request,
        },
        status=TodoStatusEnum.PENDING,
    )


def _ensure_render_last(plan: Plan) -> None:
    renders = [todo for todo in plan.todos if todo.tool == "render_docx"]
    render = renders[-1] if renders else _new_render_todo()
    plan.todos = [*(todo for todo in plan.todos if todo.tool != "render_docx"), render]


def _new_render_todo() -> Todo:
    return Todo(
        id=0,
        description="Render the completed document as a DOCX file.",
        tool="render_docx",
        status=TodoStatusEnum.PENDING,
    )


def _renumber_todos(plan: Plan) -> None:
    for identifier, todo in enumerate(plan.todos, start=1):
        todo.id = identifier


def _clear_invalid_dependencies(plan: Plan) -> None:
    known_ids = {todo.id for todo in plan.todos}
    for todo in plan.todos:
        valid_dependencies = [
            dependency
            for dependency in todo.depends_on
            if dependency in known_ids and dependency < todo.id
        ]
        if valid_dependencies != todo.depends_on:
            logger.warning(
                "Clearing invalid dependencies for todo %s: %s",
                todo.id,
                todo.depends_on,
            )
            todo.depends_on = valid_dependencies
