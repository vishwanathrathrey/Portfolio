"""Orchestrator is the single top-level flow.

It is intentionally simple: plan, execute, reflect at most once more, record
memory, return. All complexity is pushed down into the components it coordinates.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
import logging
from pathlib import Path
from time import perf_counter

from app.agent.executor import ExecutionState, Executor, RenderError
from app.agent.memory import SessionTurn, session_store
from app.agent.planner import plan
from app.agent.reflector import ReflectionResult, reflect
from app.config import settings
from app.llm.ollama_client import OllamaClient
from app.schemas import Plan
from app.tools import registry

logger = logging.getLogger(__name__)


@dataclass
class RunResult:
    """The complete result from one autonomous document-generation run."""

    plan: Plan
    state: ExecutionState
    reflection: ReflectionResult
    rendered_path: str
    summary: str
    elapsed_seconds: float


async def run_agent(
    request: str,
    ollama: OllamaClient,
    request_id: str,
    session_id: str,
) -> RunResult:
    """Plan, execute, reflect once, persist session context, and return results."""
    started_at = perf_counter()
    logger.info("[ORCHESTRATOR] Starting agent run for request: %s", request[:50])
    context = session_store.get_context(session_id)
    generated_plan = await plan(request, ollama, context)
    logger.info(
        "[PLANNER] Plan created: %s todos, doc_type=%s",
        len(generated_plan.todos),
        generated_plan.doc_type.value,
    )
    executor = Executor(
        registry=registry,
        ollama=ollama,
        output_dir=Path(settings.output_dir),
        request_id=request_id,
    )
    logger.info(
        "[EXECUTOR] Beginning execution of %s todos...",
        len(generated_plan.todos),
    )
    state = await executor.execute(generated_plan)
    logger.info("[REFLECTOR] Evaluating results...")
    reflection = await reflect(request, generated_plan, state.results, ollama)
    if not reflection.covered and reflection.followup_todos:
        state = await executor.execute_followups(
            generated_plan,
            reflection.followup_todos,
            state,
        )
    if state.rendered_path is None:
        raise RenderError("Plan completed without rendering — check planner invariants.")

    summary = _derive_summary(generated_plan, state)
    session_store.record(
        session_id,
        SessionTurn(
            request=request,
            summary=summary,
            doc_type=generated_plan.doc_type.value,
            created_at=datetime.now(timezone.utc),
        ),
    )
    result = RunResult(
        plan=generated_plan,
        state=state,
        reflection=reflection,
        rendered_path=state.rendered_path,
        summary=summary,
        elapsed_seconds=perf_counter() - started_at,
    )
    logger.info("[ORCHESTRATOR] Run complete. Rendered: %s", result.rendered_path)
    return result


def _derive_summary(plan: Plan, state: ExecutionState) -> str:
    """Build a concise human-readable summary for the completed run."""
    sentences = [
        f"Generated a {plan.doc_type.value.replace('_', ' ')} titled '{plan.title}'.",
        f"The document contains {len(state.document.sections)} rendered sections.",
    ]
    if state.errors:
        sentences.append(
            f"{len(state.errors)} todo(s) failed; affected content may require review."
        )
    else:
        sentences.append("All planned tool steps completed successfully.")
    return " ".join(sentences)
