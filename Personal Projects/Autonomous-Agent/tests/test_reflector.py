import json

import pytest

from app.agent.reflector import reflect
from app.schemas import DocTypeEnum, Plan, Todo
from tests.conftest import FakeOllama


def _plan() -> Plan:
    return Plan(
        doc_type=DocTypeEnum.PROPOSAL,
        title="Test Proposal",
        todos=[Todo(id=1, description="Generate outline.", tool="generate_outline")],
    )


@pytest.mark.asyncio
async def test_reflect_covered_true() -> None:
    ollama = FakeOllama(
        {"Original request:": json.dumps({"covered": True, "gaps": [], "followup_todos": []})}
    )

    result = await reflect("Create a proposal.", _plan(), {1: "done"}, ollama)

    assert result.covered is True
    assert result.followup_todos == []


@pytest.mark.asyncio
async def test_reflect_emits_followups() -> None:
    ollama = FakeOllama(
        {
            "Original request:": json.dumps(
                {
                    "covered": False,
                    "gaps": ["Missing pricing details"],
                    "followup_todos": [
                        {
                            "description": "Write pricing details.",
                            "tool": "generate_section_content",
                            "tool_args": {"section_type": "pricing"},
                        }
                    ],
                }
            )
        }
    )

    result = await reflect("Create a proposal.", _plan(), {1: "done"}, ollama)

    assert result.covered is False
    assert [todo.id for todo in result.followup_todos] == [2]


@pytest.mark.asyncio
async def test_reflect_swallows_errors() -> None:
    class FailingOllama(FakeOllama):
        async def generate(self, model: str, prompt: str, **kwargs: object) -> str:
            raise RuntimeError("model unavailable")

    result = await reflect("Create a proposal.", _plan(), {1: "done"}, FailingOllama())

    assert result.covered is True
    assert "Reflection failed" in result.notes[0]
