"""Reflector is a self-check stage.

It may emit follow-up TODOs if the original request wasn't fully covered.
Failures are swallowed and reported as notes — reflection must never block
document generation.
"""

import json
from dataclasses import dataclass
from typing import Any

from app.config import settings
from app.llm.ollama_client import OllamaClient
from app.llm.prompts import reflector_system_prompt, reflector_user_prompt
from app.schemas import Plan, Todo, TodoStatusEnum
from app.utils.json_repair import safe_parse


@dataclass
class ReflectionResult:
    """The reflector's coverage assessment and optional follow-up actions."""

    covered: bool
    gaps: list[str]
    followup_todos: list[Todo]
    notes: list[str]


async def reflect(
    original_request: str,
    plan: Plan,
    results: dict[int, str],
    ollama: OllamaClient,
) -> ReflectionResult:
    """Assess completed work and return non-blocking follow-up TODOs."""
    try:
        plan_json = plan.model_dump_json()
        results_json = json.dumps(results)
        text = await ollama.generate(
            model=settings.model_reflector,
            prompt=reflector_user_prompt(original_request, plan_json, results_json),
            system=reflector_system_prompt(),
            format_json=True,
            temperature=0.1,
            num_predict=512,
        )
        raw = safe_parse(text, dict)
        return _to_reflection_result(raw, plan)
    except Exception as error:
        return ReflectionResult(
            covered=True,
            gaps=[],
            followup_todos=[],
            notes=[f"Reflection failed: {error}; proceeding with existing plan."],
        )


def _to_reflection_result(raw: dict[str, Any], plan: Plan) -> ReflectionResult:
    covered = raw.get("covered")
    gaps = raw.get("gaps")
    followup_data = raw.get("followup_todos")
    if not isinstance(covered, bool):
        raise ValueError("Reflection response requires a boolean covered field.")
    if not isinstance(gaps, list) or not all(isinstance(gap, str) for gap in gaps):
        raise ValueError("Reflection response requires gaps as a list of strings.")
    if not isinstance(followup_data, list):
        raise ValueError("Reflection response requires followup_todos as a list.")

    followup_todos = [] if covered else _build_followup_todos(followup_data, plan)
    notes = ["Reflection confirmed coverage."] if covered else [
        f"Gap identified: {gap}" for gap in gaps
    ]
    return ReflectionResult(
        covered=covered,
        gaps=gaps,
        followup_todos=followup_todos,
        notes=notes,
    )


def _build_followup_todos(raw_todos: list[Any], plan: Plan) -> list[Todo]:
    next_identifier = max((todo.id for todo in plan.todos), default=0) + 1
    followups: list[Todo] = []
    for raw_todo in raw_todos:
        if not isinstance(raw_todo, dict):
            raise ValueError("Each follow-up TODO must be an object.")
        todo_data = {
            **raw_todo,
            "id": next_identifier,
            "status": TodoStatusEnum.PENDING,
        }
        followups.append(Todo.model_validate(todo_data))
        next_identifier += 1
    return followups
