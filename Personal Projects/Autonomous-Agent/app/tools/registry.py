"""Tool registration and async dispatch primitives."""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any


class ToolNotFound(Exception):
    """Raised when a requested tool has not been registered."""


class ToolArgError(Exception):
    """Raised when tool argument names do not match the registered schema."""


@dataclass(frozen=True)
class ToolSpec:
    """Metadata and async handler for an executable tool."""

    name: str
    description: str
    args_schema: dict[str, str]
    handler: Callable[..., Awaitable[Any]]


class ToolRegistry:
    """Registry for named async tools."""

    def __init__(self) -> None:
        self._specs: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        """Register a tool specification under its unique name."""
        if spec.name in self._specs:
            raise ValueError(f"Tool '{spec.name}' is already registered.")
        self._specs[spec.name] = spec

    def get(self, name: str) -> ToolSpec:
        """Return a registered tool or raise ToolNotFound."""
        try:
            return self._specs[name]
        except KeyError as error:
            raise ToolNotFound(f"Tool '{name}' is not registered.") from error

    def list_names(self) -> list[str]:
        """Return registered tool names in insertion order."""
        return list(self._specs)

    async def dispatch(self, name: str, args: dict[str, Any]) -> Any:
        """Validate argument names and invoke the named async tool."""
        spec = self.get(name)
        expected_keys = set(spec.args_schema)
        actual_keys = set(args)
        missing = expected_keys - actual_keys
        extra = actual_keys - expected_keys
        if missing or extra:
            details: list[str] = []
            if missing:
                details.append(f"missing: {', '.join(sorted(missing))}")
            if extra:
                details.append(f"extra: {', '.join(sorted(extra))}")
            raise ToolArgError(f"Invalid arguments for '{name}' ({'; '.join(details)}).")
        return await spec.handler(**args)


registry = ToolRegistry()
