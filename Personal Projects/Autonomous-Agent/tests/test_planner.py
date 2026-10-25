import json

import pytest

from app.agent.planner import PlanValidationError, plan
from tests.conftest import FakeOllama


@pytest.mark.asyncio
async def test_plan_happy_path(valid_plan_json: str) -> None:
    generated_plan = await plan(
        "Prepare a customer onboarding proposal.",
        FakeOllama({"Business request:": valid_plan_json}),
    )

    assert len(generated_plan.todos) == 5
    assert generated_plan.todos[0].tool == "generate_outline"
    assert generated_plan.todos[-1].tool == "render_docx"


@pytest.mark.asyncio
async def test_plan_repairs_missing_outline(valid_plan_json: str) -> None:
    payload = json.loads(valid_plan_json)
    payload["todos"] = payload["todos"][1:]

    generated_plan = await plan(
        "Prepare a customer onboarding proposal.",
        FakeOllama({"Business request:": json.dumps(payload)}),
    )

    assert generated_plan.todos[0].tool == "generate_outline"


@pytest.mark.asyncio
async def test_plan_repairs_missing_render(valid_plan_json: str) -> None:
    payload = json.loads(valid_plan_json)
    payload["todos"] = payload["todos"][:-1]

    generated_plan = await plan(
        "Prepare a customer onboarding proposal.",
        FakeOllama({"Business request:": json.dumps(payload)}),
    )

    assert generated_plan.todos[-1].tool == "render_docx"


@pytest.mark.asyncio
async def test_plan_renumbers_ids(valid_plan_json: str) -> None:
    payload = json.loads(valid_plan_json)
    for todo, identifier in zip(payload["todos"], [5, 8, 9, 11, 14], strict=True):
        todo["id"] = identifier
        todo["depends_on"] = []

    generated_plan = await plan(
        "Prepare a customer onboarding proposal.",
        FakeOllama({"Business request:": json.dumps(payload)}),
    )

    assert [todo.id for todo in generated_plan.todos] == [1, 2, 3, 4, 5]


@pytest.mark.asyncio
async def test_plan_retries_once_on_validation_error(valid_plan_json: str) -> None:
    class RetryingOllama(FakeOllama):
        async def generate(self, model: str, prompt: str, **kwargs: object) -> str:
            self.calls.append((model, prompt))
            return "{}" if len(self.calls) == 1 else valid_plan_json

    ollama = RetryingOllama()
    generated_plan = await plan("Prepare a customer onboarding proposal.", ollama)

    assert generated_plan.title == "Customer Onboarding Proposal"
    assert len(ollama.calls) == 2


@pytest.mark.asyncio
async def test_plan_raises_after_two_failures() -> None:
    class FailingOllama(FakeOllama):
        async def generate(self, model: str, prompt: str, **kwargs: object) -> str:
            self.calls.append((model, prompt))
            return "[]"

    with pytest.raises(PlanValidationError):
        await plan("Prepare a customer onboarding proposal.", FailingOllama())
