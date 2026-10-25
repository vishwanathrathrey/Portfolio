"""No-op tool for committing a planner TODO list."""

from typing import Any

from app.tools.registry import ToolRegistry, ToolSpec


async def write_todos(todos: list[dict[str, Any]]) -> str:
    """Acknowledge the number of TODO items committed to executor state."""
    return f"ok: {len(todos)} todos written"


def register_tool(registry: ToolRegistry) -> None:
    """Register the TODO-writing tool."""
    registry.register(
        ToolSpec(
            name="write_todos",
            description="Commit the TODO list into executor state (no-op logger).",
            args_schema={"todos": "list[dict]"},
            handler=write_todos,
        )
    )
