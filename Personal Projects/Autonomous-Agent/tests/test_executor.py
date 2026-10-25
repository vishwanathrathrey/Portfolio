from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

import pytest

from app.agent.executor import Executor, RenderError
from app.schemas import DocTypeEnum, Plan, Todo, TodoStatusEnum
from app.tools.registry import ToolNotFound, ToolSpec


class FakeRegistry:
    """Small async registry double with inspectable dispatch calls."""

    def __init__(self, handlers: dict[str, Callable[..., Awaitable[Any]]]) -> None:
        self._handlers = handlers
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def get(self, name: str) -> ToolSpec:
        if name not in self._handlers:
            raise ToolNotFound(name)
        return ToolSpec(name, "", {}, self._handlers[name])

    async def dispatch(self, name: str, args: dict[str, Any]) -> Any:
        self.calls.append((name, args))
        return await self._handlers[name](**args)


def _plan(todos: list[Todo]) -> Plan:
    return Plan(
        doc_type=DocTypeEnum.PROPOSAL,
        title="Test Proposal",
        todos=todos,
    )


def _handlers() -> dict[str, Callable[..., Awaitable[Any]]]:
    async def outline(**kwargs: Any) -> dict[str, list[dict[str, str]]]:
        return {"sections": []}

    async def mock_data(**kwargs: Any) -> dict[str, dict[str, dict[str, int]]]:
        return {"entities": {"budget": {"total": 50000}}}

    async def content(**kwargs: Any) -> str:
        return "Generated section content."

    async def render(**kwargs: Any) -> str:
        return str(kwargs["output_path"])

    return {
        "generate_outline": outline,
        "mock_data_provider": mock_data,
        "generate_section_content": content,
        "render_docx": render,
    }


@pytest.mark.asyncio
async def test_execute_happy_path() -> None:
    todos = [
        Todo(id=1, description="Generate outline.", tool="generate_outline"),
        Todo(id=2, description="Create budget data.", tool="mock_data_provider"),
        Todo(
            id=3,
            description="Write overview.",
            tool="generate_section_content",
            tool_args={"section_type": "overview"},
        ),
        Todo(id=4, description="Render document.", tool="render_docx"),
    ]
    executor = Executor(FakeRegistry(_handlers()), object(), Path("output"), "run-id")

    state = await executor.execute(_plan(todos))

    assert len(state.document.sections) == 1
    assert state.rendered_path == "output\\run-id.docx"
    assert all(todo.status is TodoStatusEnum.DONE for todo in todos)


@pytest.mark.asyncio
async def test_execute_records_tool_error_and_continues() -> None:
    async def failing_outline(**kwargs: Any) -> None:
        raise RuntimeError("outline unavailable")

    handlers = _handlers()
    handlers["generate_outline"] = failing_outline
    todos = [
        Todo(id=1, description="Generate outline.", tool="generate_outline"),
        Todo(id=2, description="Create budget data.", tool="mock_data_provider"),
    ]

    state = await Executor(FakeRegistry(handlers), object(), Path("output")).execute(
        _plan(todos)
    )

    assert todos[0].status is TodoStatusEnum.FAILED
    assert todos[1].status is TodoStatusEnum.DONE
    assert state.errors[1] == "outline unavailable"


@pytest.mark.asyncio
async def test_execute_render_failure_raises() -> None:
    async def failing_render(**kwargs: Any) -> None:
        raise RuntimeError("disk full")

    handlers = _handlers()
    handlers["render_docx"] = failing_render
    todos = [Todo(id=1, description="Render document.", tool="render_docx")]

    with pytest.raises(RenderError, match="disk full"):
        await Executor(FakeRegistry(handlers), object(), Path("output")).execute(
            _plan(todos)
        )


@pytest.mark.asyncio
async def test_execute_skips_todos_with_failed_deps() -> None:
    async def failing_outline(**kwargs: Any) -> None:
        raise RuntimeError("outline unavailable")

    handlers = _handlers()
    handlers["generate_outline"] = failing_outline
    todos = [
        Todo(id=1, description="Generate outline.", tool="generate_outline"),
        Todo(
            id=2,
            description="Create budget data.",
            tool="mock_data_provider",
            depends_on=[1],
        ),
    ]

    await Executor(FakeRegistry(handlers), object(), Path("output")).execute(_plan(todos))

    assert todos[1].status is TodoStatusEnum.FAILED
    assert todos[1].error == "upstream dependency failed"


@pytest.mark.asyncio
async def test_execute_auto_injects_arguments_for_section_content() -> None:
    todos = [
        Todo(
            id=1,
            description="Write executive summary.",
            tool="generate_section_content",
            tool_args={"section_type": "executive_summary"},
        )
    ]
    registry = FakeRegistry(_handlers())

    await Executor(registry, object(), Path("output")).execute(_plan(todos))

    _, args = registry.calls[0]
    assert set(args) == {"doc_type", "doc_title", "section_title", "data_block", "ollama"}
    assert args["doc_type"] == "proposal"
    assert args["doc_title"] == "Test Proposal"
    assert args["section_title"] == "Executive Summary"
    assert args["data_block"] == "No specific data provided."


@pytest.mark.asyncio
async def test_execute_skips_unknown_tools() -> None:
    todo = Todo(id=1, description="Add a table.", tool="add_table")

    await Executor(FakeRegistry(_handlers()), object(), Path("output")).execute(
        _plan([todo])
    )

    assert todo.status is TodoStatusEnum.SKIPPED
