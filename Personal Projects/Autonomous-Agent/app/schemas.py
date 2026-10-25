"""API request and response models for the agent service."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DocTypeEnum(str, Enum):
    """Supported generated document types."""

    PROPOSAL = "proposal"
    MEETING_MINUTES = "meeting_minutes"
    PROJECT_PLAN = "project_plan"
    BUSINESS_REPORT = "business_report"
    TECHNICAL_DESIGN = "technical_design"
    SOP = "sop"
    PRODUCT_SPEC = "product_spec"


class TodoStatusEnum(str, Enum):
    """Lifecycle states for plan TODO items."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    FAILED = "failed"
    SKIPPED = "skipped"


class Todo(BaseModel):
    """A single planned agent action."""

    id: int
    description: str = Field(min_length=3, max_length=300)
    tool: str | None = None
    tool_args: dict[str, Any] = Field(default_factory=dict)
    depends_on: list[int] = Field(default_factory=list)
    status: TodoStatusEnum = TodoStatusEnum.PENDING
    result_summary: str | None = None
    error: str | None = None


class Plan(BaseModel):
    """An ordered, transparent plan for producing a document."""

    model_config = ConfigDict(extra="forbid")

    doc_type: DocTypeEnum
    title: str = Field(min_length=3, max_length=200)
    assumptions: list[str] = Field(default_factory=list)
    todos: list[Todo] = Field(min_length=1)


class AgentRequest(BaseModel):
    """The client request to generate a business document."""

    model_config = ConfigDict(extra="forbid")

    request: str = Field(min_length=10, max_length=4000)
    session_id: str | None = None


class AgentResponse(BaseModel):
    """The completed agent result returned to an API client."""

    request_id: str
    session_id: str
    summary: str
    doc_type: DocTypeEnum
    title: str
    plan: Plan
    todos_executed: int
    todos_failed: int
    reflection_notes: list[str] = Field(default_factory=list)
    doc_path: str
    download_url: str
    elapsed_seconds: float


class HealthResponse(BaseModel):
    """The service and Ollama availability status."""

    status: str
    ollama_reachable: bool
    models: dict[str, str]
    available_models: list[str] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    """A machine-readable API error response."""

    error: str
    detail: str
    request_id: str | None = None
