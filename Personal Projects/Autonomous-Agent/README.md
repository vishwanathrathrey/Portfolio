# Autonomous Agent

## Overview

Autonomous Agent is a full-stack application that turns natural-language business requests into downloadable `.docx` deliverables. Its FastAPI service uses locally hosted Ollama models to plan a task, execute approved tools, reflect on intermediate results, and make a bounded correction pass before returning the document and execution summary.

The project demonstrates how an inspectable, multi-step agent workflow can combine LLM integration with deterministic validation, modular tooling, and a practical document-generation API.

## Recruiter Snapshot

This project demonstrates:

- Generative AI and local LLM integration
- Agent orchestration with planning, execution, and reflection
- Allowlisted tool calling and workflow automation
- REST API development with FastAPI
- Request validation and guardrails
- React frontend development
- Automated unit and API testing
- Docker-based deployment

## Technologies

| Category | Technologies |
|---|---|
| Language | Python, JavaScript |
| AI / LLM | Ollama, `qwen2.5-coder:7b`, `mistral:latest` |
| Backend | FastAPI, Pydantic, Uvicorn |
| Frontend | React, Vite |
| Document Generation | python-docx |
| Testing and Quality | Pytest, Ruff |
| Deployment | Docker, Docker Compose |

## Problem Statement

A single LLM response can miss requirements, make unsupported assumptions, or produce output that is difficult to verify. This project addresses those limitations by splitting a business request into ordered tasks, executing them through a scoped tool registry, and checking the intermediate result against the original request before rendering a document.

## Architecture Overview

The service separates API handling, agent orchestration, model access, tool execution, and document rendering. The planner produces a structured task list; the executor dispatches approved tools; the reflector checks coverage and can request one bounded follow-up pass. A renderer-independent document model feeds deterministic `.docx` generation.

```text
React client
    ↓
FastAPI request validation and guardrails
    ↓
Planner → Executor (allowlisted tools) → Reflector
    ↓                         ↑
    └── bounded correction pass
    ↓
Document model → DOCX renderer
    ↓
Downloadable document and execution summary
```

## Key Features

### Multi-step Agent Workflow

- Creates an ordered, machine-readable plan for each request.
- Executes tasks with local tools and shared document/model context.
- Reflects on intermediate work and performs one bounded correction pass.

### Guardrails and Reliability

- Applies deterministic checks to reject empty, oversized, suspicious, and clearly off-topic requests before a model call.
- Uses an allowlisted tool registry rather than dispatching arbitrary model-generated operations.
- Retries transient Ollama failures and provides reviewable tool fallbacks where partial documents remain useful.

### Document Generation and API

- Converts agent output into a structured document model and `.docx` file.
- Exposes health and document-generation endpoints through FastAPI.
- Returns a document download URL and execution summary.

### Full-Stack Demo

- Includes a React/Vite frontend and an end-to-end demo script with representative business requests.
- Supports local development and Docker-based API deployment.

## Setup and Usage

### Backend

1. Create and activate a virtual environment, then install dependencies:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Install Ollama and pull the configured models:

   ```bash
   ollama pull qwen2.5-coder:7b
   ollama pull mistral:latest
   ```

3. Copy `.env.example` to `.env`, then start Ollama and the API:

   ```bash
   copy .env.example .env
   ollama serve
   uvicorn app.main:app --reload
   ```

4. Run the end-to-end demo:

   ```bash
   python scripts/demo.py
   ```

### Frontend

Install the frontend dependencies and start the Vite development server:

```bash
cd frontend
npm install
npm run dev
```

### Docker

With Ollama available on the host and `.env` configured, set `OLLAMA_BASE_URL` in `.env` to `http://host.docker.internal:11434` and start the API container:

```bash
docker compose up --build
```

Generated documents are written to the local `output/` directory.

## API

### `POST /agent`

Request:

```json
{
  "request": "Prepare a business proposal for a new customer onboarding process"
}
```

The response includes a request ID, session ID, summary, document path, and download URL.

### `GET /health`

Returns the service health status. The root endpoint (`GET /`) provides a short API status message.

## Software Engineering Concepts Demonstrated

- Modular architecture and separation of concerns
- Structured LLM output and prompt engineering
- Deterministic validation around non-deterministic model behavior
- Bounded orchestration and tool permissions
- Renderer-independent document modeling
- Testable API, agent, and document-rendering components

## Project Structure

```text
app/
  agent/       Planner, executor, reflector, memory, and orchestration
  docmodel/    Renderer-independent document representation
  llm/         Ollama HTTP client and prompts
  tools/       Tool registry, content generation, and DOCX renderer
  utils/       Guardrails, JSON repair, and logging
  main.py      FastAPI routes and dependency wiring
frontend/      React/Vite user interface
scripts/       End-to-end demo and video script generation
tests/         Offline unit and API tests
```

## Technical Tradeoffs

- Local Ollama keeps inference on the developer's machine and avoids per-request hosted API costs.
- A strict tool registry and deterministic request checks constrain the actions the model can take.
- Separating the document model from API schemas allows document rendering to be tested independently.
- This initial version does not include a database, background job queue, authentication, or distributed execution.
