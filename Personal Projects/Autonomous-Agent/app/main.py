"""main.py is thin: validate -> run_agent -> shape response.

All business logic lives in app.agent; all model access lives behind the
OllamaClient dependency so tests can override it.
"""

import time
import uuid
import mimetypes
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.agent import run_agent, session_store
from app.config import ensure_output_dir, settings
from app.llm.ollama_client import OllamaClient, OllamaError, get_ollama_client
from app.schemas import AgentRequest, AgentResponse, ErrorResponse, HealthResponse
from app.utils.guardrails import GuardrailError, validate_request
from app.utils.logging import configure_logging, get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Prepare output storage and report Ollama availability at startup."""
    configure_logging()
    logging.getLogger("uvicorn.access").disabled = True
    ensure_output_dir()
    client = get_ollama_client()
    configured_models = {
        "planner": settings.model_planner,
        "writer": settings.model_writer,
        "reflector": settings.model_reflector,
    }
    try:
        available_models = await client.list_models()
    except OllamaError as error:
        logger.warning("ollama_unreachable", extra={"error": str(error)})
    else:
        missing_models = [
            model for model in configured_models.values() if model not in available_models
        ]
        if missing_models:
            logger.warning("ollama_models_missing", extra={"models": missing_models})
        else:
            logger.info("ollama_ready", extra={"models": available_models})
    yield


app = FastAPI(title="Autonomous Agent", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ensure_output_dir()
mimetypes.add_type(
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".docx",
)
app.mount("/files", StaticFiles(directory=settings.output_dir), name="files")


@app.get("/")
async def root() -> dict[str, str]:
    """Return a concise API readiness message."""
    return {
        "message": "Autonomous Agent API is running. POST to /agent to generate a document."
    }


@app.post(
    "/agent",
    response_model=AgentResponse,
    responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def post_agent(
    payload: AgentRequest,
    request: Request,
    ollama: OllamaClient = Depends(get_ollama_client),
) -> AgentResponse:
    """Validate and execute a document-generation request."""
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    started_at = time.perf_counter()
    log_extra = {"request_id": request_id}

    try:
        validate_request(payload.request)
    except GuardrailError as error:
        logger.warning(
            "guardrail_rejected",
            extra={**log_extra, "code": error.code},
        )
        raise HTTPException(
            status_code=422,
            detail={
                "error": error.code,
                "detail": error.detail,
                "request_id": request_id,
            },
        ) from error

    session_id = payload.session_id or session_store.new_session_id()
    try:
        result = await run_agent(
            request=payload.request,
            ollama=ollama,
            request_id=request_id,
            session_id=session_id,
        )
    except Exception as error:
        logger.exception("agent_run_failed", extra=log_extra)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "agent_run_failed",
                "detail": str(error),
                "request_id": request_id,
            },
        ) from error

    elapsed = time.perf_counter() - started_at
    doc_filename = Path(result.rendered_path).name
    response = AgentResponse(
        request_id=request_id,
        session_id=session_id,
        summary=result.summary,
        doc_type=result.plan.doc_type,
        title=result.plan.title,
        plan=result.plan,
        todos_executed=sum(
            todo.status.value == "done" for todo in result.plan.todos
        ),
        todos_failed=sum(
            todo.status.value == "failed" for todo in result.plan.todos
        ),
        reflection_notes=result.reflection.notes,
        doc_path=result.rendered_path,
        download_url=f"/files/{doc_filename}",
        elapsed_seconds=round(elapsed, 2),
    )
    logger.info(
        "agent_run_ok",
        extra={
            **log_extra,
            "doc_type": result.plan.doc_type.value,
            "elapsed": round(elapsed, 2),
        },
    )
    return response


@app.get("/health", response_model=HealthResponse)
async def health(
    ollama: OllamaClient = Depends(get_ollama_client),
) -> HealthResponse:
    """Report API health and the availability of configured Ollama models."""
    reachable = await ollama.health()
    available_models = await ollama.list_models() if reachable else []
    models = {
        "planner": settings.model_planner,
        "writer": settings.model_writer,
        "reflector": settings.model_reflector,
    }
    all_present = all(model in available_models for model in models.values())
    return HealthResponse(
        status="ok" if reachable and all_present else "degraded",
        ollama_reachable=reachable,
        models=models,
        available_models=available_models,
    )


@app.exception_handler(HTTPException)
async def http_exc_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Return project-standard JSON for HTTP exceptions."""
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "http_error", "detail": str(exc.detail)},
    )


@app.exception_handler(RequestValidationError)
async def request_validation_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Map request-length validation failures to the public guardrail contract."""
    del request
    errors = exc.errors()
    if any(error.get("type") == "string_too_short" for error in errors):
        return JSONResponse(
            status_code=422,
            content={
                "error": "request_too_short",
                "detail": "Request must contain at least 10 characters.",
            },
        )
    if any(error.get("type") == "string_too_long" for error in errors):
        return JSONResponse(
            status_code=422,
            content={
                "error": "request_too_long",
                "detail": f"Request must not exceed {settings.max_request_len} characters.",
            },
        )
    return JSONResponse(
        status_code=422,
        content={"error": "request_validation_error", "detail": errors},
    )
