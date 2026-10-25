"""Built-in tools registered for agent execution."""

from app.tools import content, docx_renderer, mock_data, outline, write_todos
from app.tools.registry import registry

for mod in (outline, content, mock_data, docx_renderer, write_todos):
    mod.register_tool(registry)

__all__ = ["registry"]
