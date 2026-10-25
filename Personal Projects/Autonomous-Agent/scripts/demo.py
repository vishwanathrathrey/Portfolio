"""Run two end-to-end document-generation requests against the local API."""

import asyncio
import json
from pathlib import Path
from typing import Any

import httpx

STANDARD_REQUEST = (
    "Create a business proposal for a mid-sized logistics company adopting AI-based "
    "route optimization. Include executive summary, scope, timeline, pricing tiers, "
    "and risks."
)

COMPLEX_REQUEST = (
    "We need a project plan for our team retreat next quarter. Budget is tight but we "
    "want it to feel premium. Attendance is 'optional' but management wants 90%. "
    "We're not sure if it's 2 or 3 days. Also include risks and an agenda."
)

API_BASE_URL = "http://localhost:8000"
OUTPUT_DIR = Path("output")


async def _run_request(
    client: httpx.AsyncClient,
    label: str,
    request_text: str,
) -> None:
    response = await client.post("/agent", json={"request": request_text})
    response.raise_for_status()
    payload: dict[str, Any] = response.json()

    print(f"\n{label}")
    print("-" * len(label))
    print(f"Summary: {payload['summary']}")
    print(f"Doc Type: {payload['doc_type']}")
    print(f"Todos Executed: {payload['todos_executed']}")
    print(f"Time: {payload['elapsed_seconds']} seconds")
    assumptions = payload["plan"].get("assumptions", [])
    if assumptions:
        print(f"Assumptions: {json.dumps(assumptions)}")

    download_response = await client.get(payload["download_url"])
    download_response.raise_for_status()
    output_path = OUTPUT_DIR / Path(payload["download_url"]).name
    output_path.write_bytes(download_response.content)
    print(f"Downloaded: {output_path}")


async def run_demo() -> None:
    """Run standard and ambiguous document-generation requests end to end."""
    print("=" * 60)
    print("Autonomous Agent Demo")
    print("=" * 60)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    async with httpx.AsyncClient(base_url=API_BASE_URL, timeout=180.0) as client:
        await _run_request(client, "1. Standard logistics proposal", STANDARD_REQUEST)
        await _run_request(client, "2. Complex team-retreat project plan", COMPLEX_REQUEST)

    print("\nDemo complete! Check ./output/")


if __name__ == "__main__":
    asyncio.run(run_demo())
