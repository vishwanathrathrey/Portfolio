import json
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.llm.ollama_client import get_ollama_client
from app.main import app

OUTLINE_JSON = json.dumps(
    {
        "sections": [
            {"title": "Overview", "hint": "Purpose and scope."},
            {"title": "Approach", "hint": "Recommended approach."},
            {"title": "Timeline", "hint": "Delivery milestones."},
            {"title": "Next Steps", "hint": "Actions to proceed."},
        ]
    }
)
MOCK_DATA_JSON = json.dumps({"entities": {"budget": {"currency": "USD", "total": 50000}}})
SECTION_TEXT = "This section provides a concise, evidence-based business overview."
REFLECTION_JSON = json.dumps(
    {"covered": True, "gaps": [], "followup_todos": []}
)


def _plan_payload() -> dict[str, Any]:
    return {
        "doc_type": "proposal",
        "title": "Customer Onboarding Proposal",
        "assumptions": [],
        "todos": [
            {
                "id": 1,
                "description": "Generate the document outline.",
                "tool": "generate_outline",
                "tool_args": {
                    "doc_type": "proposal",
                    "title": "Customer Onboarding Proposal",
                    "topic": "Customer onboarding",
                },
                "depends_on": [],
            },
            {
                "id": 2,
                "description": "Prepare budget mock data.",
                "tool": "mock_data_provider",
                "tool_args": {},
                "depends_on": [1],
            },
            {
                "id": 3,
                "description": "Write the overview section.",
                "tool": "generate_section_content",
                "tool_args": {"section_type": "overview"},
                "depends_on": [2],
            },
            {
                "id": 4,
                "description": "Add a supporting table.",
                "tool": "add_table",
                "tool_args": {},
                "depends_on": [3],
            },
            {
                "id": 5,
                "description": "Render the finished document.",
                "tool": "render_docx",
                "tool_args": {},
                "depends_on": [3],
            },
        ],
    }


class FakeOllama:
    """Deterministic async Ollama replacement with inspectable prompt routing."""

    def __init__(self, responses: dict[str, str] | None = None) -> None:
        self.responses = responses or {}
        self.calls: list[tuple[str, str]] = []

    async def generate(self, model: str, prompt: str, **kwargs: Any) -> str:
        """Return a canned reply selected by prompt substring."""
        self.calls.append((model, prompt))
        for substring, reply in self.responses.items():
            if substring in prompt:
                return reply
        return self._default(model, prompt)

    async def list_models(self) -> list[str]:
        """Return all project-configured model names."""
        return ["mistral:latest", "qwen2.5-coder:3b", "qwen2.5-coder:7b"]

    async def health(self) -> bool:
        """Report the fake service as reachable."""
        return True

    def _default(self, model: str, prompt: str) -> str:
        """Return default planner, tool, writer, or reflector content."""
        if "Produce a document outline" in prompt:
            return OUTLINE_JSON
        if "Entity:" in prompt:
            return MOCK_DATA_JSON
        if "Original request:" in prompt:
            return REFLECTION_JSON
        if model == "mistral:latest":
            return SECTION_TEXT
        return json.dumps(_plan_payload())


@pytest.fixture
def mock_ollama() -> FakeOllama:
    """Provide a default offline Ollama replacement."""
    return FakeOllama()


@pytest.fixture
def valid_plan_json() -> str:
    """Provide a well-formed five-step planner response."""
    return json.dumps(_plan_payload())


@pytest.fixture
def outline_json() -> str:
    """Provide canned outline JSON."""
    return OUTLINE_JSON


@pytest.fixture
def mock_data_json() -> str:
    """Provide canned mock-data JSON."""
    return MOCK_DATA_JSON


@pytest.fixture
def section_text() -> str:
    """Provide canned document prose."""
    return SECTION_TEXT


@pytest.fixture
def tmp_output_dir(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Route application output and static-file serving to a temporary directory."""
    monkeypatch.setattr(settings, "output_dir", tmp_path)
    for route in app.routes:
        if getattr(route, "path", None) == "/files":
            monkeypatch.setattr(route.app, "directory", str(tmp_path))
            monkeypatch.setattr(route.app, "all_directories", [str(tmp_path)])
    return tmp_path


@pytest.fixture
def client(
    mock_ollama: FakeOllama,
    tmp_output_dir: Path,
) -> Generator[TestClient, None, None]:
    """Provide a FastAPI client with the Ollama dependency overridden."""
    del tmp_output_dir
    app.dependency_overrides[get_ollama_client] = lambda: mock_ollama
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
