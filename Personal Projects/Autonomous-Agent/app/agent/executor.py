"""Executor is a linear, resilient runner.

A failed non-render todo does not abort the run — the reflector and orchestrator
can still recover, and the render step still produces a document with whatever
was completed. Only render failures are fatal.
"""

from dataclasses import dataclass, field
import json
import logging
from pathlib import Path
from typing import Any
from uuid import uuid4

from app.config import settings
from app.docmodel.models import Block, BlockTypeEnum, Document, Section
from app.llm.ollama_client import OllamaClient
from app.schemas import Plan, Todo, TodoStatusEnum
from app.tools.registry import ToolNotFound, ToolRegistry

logger = logging.getLogger(__name__)


class RenderError(Exception):
    """Raised when the document renderer cannot produce the final file."""


@dataclass
class ExecutionState:
    """Mutable state accumulated while a plan is executed."""

    document: Document
    outline: dict[str, Any] | None = None
    mock_data: dict[str, dict[str, Any]] = field(default_factory=dict)
    section_text: dict[str, str] = field(default_factory=dict)
    section_titles: dict[int, str] = field(default_factory=dict)
    results: dict[int, str] = field(default_factory=dict)
    errors: dict[int, str] = field(default_factory=dict)
    rendered_path: str | None = None


class Executor:
    """Execute plan TODOs sequentially through a tool registry."""

    def __init__(
        self,
        registry: ToolRegistry,
        ollama: OllamaClient,
        output_dir: Path,
        request_id: str | None = None,
    ) -> None:
        self._registry = registry
        self._ollama = ollama
        self._output_dir = output_dir
        self._request_id = request_id or str(uuid4())

    async def execute(self, plan: Plan) -> ExecutionState:
        """Execute all TODOs in a plan and return the accumulated state."""
        state = ExecutionState(
            document=Document(title=plan.title, doc_type=plan.doc_type.value)
        )
        await self._execute_todos(plan.todos, plan, state)
        return state

    async def execute_followups(
        self,
        plan: Plan,
        followup_todos: list[Todo],
        state: ExecutionState,
    ) -> ExecutionState:
        """Append and execute reflection follow-up TODOs using existing state."""
        plan.todos.extend(followup_todos)
        await self._execute_todos(followup_todos, plan, state)
        return state

    async def _execute_todos(
        self,
        todos: list[Todo],
        plan: Plan,
        state: ExecutionState,
    ) -> None:
        ordered_todos = [
            *(todo for todo in todos if todo.tool != "render_docx"),
            *(todo for todo in todos if todo.tool == "render_docx"),
        ]
        for todo in ordered_todos:
            logger.info(
                "[EXECUTOR] Running todo #%s: %s",
                todo.id,
                todo.description,
            )
            if any(dependency in state.errors for dependency in todo.depends_on):
                self._mark_dependency_failure(todo, state)
                continue
            if todo.tool is None:
                todo.status = TodoStatusEnum.SKIPPED
                todo.result_summary = "No tool assigned; skipped."
                state.results[todo.id] = todo.result_summary
                continue
            try:
                result = await self._dispatch(todo, plan, state)
                self._record_success(todo, result, state)
                logger.debug("       Tool: %s, Status: done", todo.tool)
            except ToolNotFound:
                self._mark_unknown_tool(todo, state)
            except Exception as error:
                message = str(error)
                todo.status = TodoStatusEnum.FAILED
                todo.error = message
                state.errors[todo.id] = message
                if todo.tool == "render_docx":
                    raise RenderError(f"Document rendering failed: {message}") from error

    async def _dispatch(self, todo: Todo, plan: Plan, state: ExecutionState) -> Any:
        if todo.tool == "write_todos":
            return await self._dispatch_tool(
                todo.tool,
                {"todos": [planned_todo.model_dump() for planned_todo in plan.todos]},
                sanitize=False,
            )

        if todo.tool == "generate_outline":
            args = {
                "doc_type": plan.doc_type.value,
                "title": plan.title,
                "topic": plan.title,
                "ollama": self._ollama,
            }
            return await self._dispatch_tool(todo.tool, args, sanitize=False)
        if todo.tool == "generate_section_content":
            section_title = _section_title(todo)
            state.section_titles[todo.id] = section_title
            args = {
                "doc_type": plan.doc_type.value,
                "doc_title": plan.title,
                "section_title": section_title,
                "data_block": (
                    json.dumps(state.mock_data)
                    if state.mock_data
                    else "No specific data provided."
                ),
                "ollama": self._ollama,
            }
            return await self._dispatch_tool(todo.tool, args, sanitize=False)
        if todo.tool == "mock_data_provider":
            args = {
                "entity": _mock_data_entity(todo),
                "context": plan.title,
                "ollama": self._ollama,
            }
            return await self._dispatch_tool(todo.tool, args, sanitize=False)
        if todo.tool == "render_docx":
            args = {
                "document": state.document,
                "output_path": str(
                    Path(settings.output_dir) / f"{self._request_id}.docx"
                ),
            }
            return await self._dispatch_tool(todo.tool, args, sanitize=False)

        args = {**todo.tool_args, "ollama": self._ollama}
        return await self._dispatch_tool(todo.tool, args)

    async def _dispatch_tool(
        self,
        tool_name: str,
        args: dict[str, Any],
        *,
        sanitize: bool = True,
    ) -> Any:
        """Optionally sanitize planner arguments before dispatching a tool."""
        if not sanitize:
            return await self._registry.dispatch(tool_name, args)

        spec = self._registry.get(tool_name)
        allowed_keys = set(spec.args_schema)
        unexpected_keys = sorted(set(args) - allowed_keys)
        if unexpected_keys:
            logger.warning("Dropping unexpected tool arguments: %s", unexpected_keys)
        sanitized_args = {
            argument_name: value
            for argument_name, value in args.items()
            if argument_name in allowed_keys
        }
        return await self._registry.dispatch(tool_name, sanitized_args)

    def _mark_unknown_tool(self, todo: Todo, state: ExecutionState) -> None:
        message = f"Unknown tool '{todo.tool}'; skipped."
        logger.warning(message)
        todo.status = TodoStatusEnum.SKIPPED
        todo.result_summary = message
        state.results[todo.id] = message

    def _mark_dependency_failure(self, todo: Todo, state: ExecutionState) -> None:
        message = "upstream dependency failed"
        todo.status = TodoStatusEnum.FAILED
        todo.error = message
        state.errors[todo.id] = message

    def _record_success(self, todo: Todo, result: Any, state: ExecutionState) -> None:
        summary = str(result)
        todo.status = TodoStatusEnum.DONE
        todo.result_summary = summary
        state.results[todo.id] = summary

        if todo.tool == "generate_outline" and isinstance(result, dict):
            state.outline = result
        elif todo.tool == "mock_data_provider" and isinstance(result, dict):
            entity = _mock_data_entity(todo)
            state.mock_data[entity] = result
        elif todo.tool == "generate_section_content" and isinstance(result, str):
            section_title = state.section_titles.get(todo.id, _section_title(todo))
            state.section_text[section_title] = result
            state.document.sections.append(
                Section(
                    title=section_title,
                    blocks=[Block(type=BlockTypeEnum.PARAGRAPH, text=result)],
                )
            )
        elif todo.tool == "render_docx":
            state.rendered_path = str(result)


def _section_title(todo: Todo) -> str:
    section_type = str(todo.tool_args.get("section_type", "Overview"))
    return section_type.replace("_", " ").title()


def _mock_data_entity(todo: Todo) -> str:
    description = todo.description.lower()
    for entity in ("budget", "timeline", "pricing", "kpis", "risks"):
        if entity in description:
            return entity
    return "budget"
