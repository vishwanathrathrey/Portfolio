"""Mock business-data generation with deterministic fallbacks."""

from typing import Any

from app.config import settings
from app.llm.ollama_client import OllamaClient, OllamaError
from app.llm.prompts import mock_data_system_prompt, mock_data_user_prompt
from app.tools.registry import ToolRegistry, ToolSpec
from app.utils.json_repair import JSONRepairError, safe_parse

_FALLBACK_DATA: dict[str, dict[str, Any]] = {
    "budget": {
        "currency": "USD",
        "total": 50000,
        "contingency_percent": 10,
        "period": "12 months",
    },
    "timeline": {
        "duration_weeks": 12,
        "phases": ["Discovery", "Implementation", "Validation", "Launch"],
    },
    "pricing": {
        "currency": "USD",
        "implementation_fee": 15000,
        "monthly_fee": 2500,
        "contract_term_months": 12,
    },
    "kpis": {
        "adoption_target_percent": 80,
        "cycle_time_reduction_percent": 20,
        "customer_satisfaction_target": 4.5,
    },
    "risks": {
        "items": [
            "Stakeholder availability",
            "Data quality",
            "Scope changes",
        ]
    },
}


async def mock_data_provider(
    entity: str,
    context: str,
    ollama: OllamaClient,
) -> dict[str, Any]:
    """Generate mock data or return deterministic data when generation fails."""
    try:
        response = await ollama.generate(
            model=settings.model_planner,
            prompt=mock_data_user_prompt(entity=entity, context=context),
            system=mock_data_system_prompt(),
            format_json=True,
        )
        parsed = safe_parse(response, dict)
        if not isinstance(parsed.get("entities"), dict):
            raise JSONRepairError("Mock data response must include an entities object.")
        return parsed
    except (JSONRepairError, OllamaError):
        return {"entities": {entity: _fallback_for(entity)}}


def _fallback_for(entity: str) -> dict[str, Any]:
    return _FALLBACK_DATA.get(
        entity.lower(),
        {
            "summary": "Baseline business data is unavailable; validate details with stakeholders.",
            "context": "General planning assumption",
        },
    )


def register_tool(registry: ToolRegistry) -> None:
    """Register the mock-data provider tool."""
    registry.register(
        ToolSpec(
            name="mock_data_provider",
            description="Generate plausible mock business data for a section.",
            args_schema={
                "entity": "str",
                "context": "str",
                "ollama": "OllamaClient",
            },
            handler=mock_data_provider,
        )
    )
