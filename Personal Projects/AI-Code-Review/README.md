# AI-Powered Code Review Assistant

## Overview

AI-Powered Code Review Assistant is a Generative AI application that automates GitHub Pull Request reviews using a locally hosted Large Language Model (LLM) through Ollama.

The system retrieves pull request changes, performs AI-driven code analysis, validates findings, generates structured review reports, and publishes actionable feedback.

This project demonstrates the practical application of Generative AI within the Software Development Lifecycle (SDLC) while emphasizing software architecture, API integration, validation pipelines, testing, and maintainable system design.

---

## Recruiter Snapshot

### This project demonstrates:

- Generative AI & LLM Integration
- Prompt Engineering
- GitHub API Integration
- REST API Development
- Software Architecture & Design
- AI Output Validation
- Security Scanning
- Automated Report Generation
- Testing & Quality Engineering
- Workflow Automation

---

## Technologies

| Category | Technologies |
|-----------|-------------|
| Language | Python |
| AI / LLM | Ollama |
| Backend | Flask |
| APIs | GitHub REST API, Resend API |
| Reporting | Markdown, HTML |
| Testing | Pytest, unittest.mock |
| Configuration | JSON |
| Version Control | GitHub |

---

## Problem Statement

Code reviews are critical for maintaining software quality, but manual reviews can become time-consuming and inconsistent.

This project explores how Large Language Models can assist developers by automatically analyzing pull request changes and generating structured review feedback while applying validation and filtering mechanisms to improve reliability.

---

## Architecture Overview

The application follows a modular architecture with clear separation of responsibilities.

### Core Components

#### GitHub Integration

- Fetch Pull Request metadata
- Retrieve changed files and diffs
- Publish review comments

#### AI Review Engine

- Generate prompts from code changes
- Send code patches to Ollama
- Receive AI-generated review findings

#### Validation Pipeline

- Parse AI responses
- Normalize output
- Validate evidence against code changes
- Remove low-confidence findings
- Classify severity levels

#### Reporting Layer

- Generate HTML reports
- Generate Markdown reports
- Produce review statistics

#### Notification Layer

- Email review summaries using Resend API
- Post review comments directly to GitHub

---

## Current Workflow

The project currently operates through a development workflow triggered manually using Postman.

```text
Postman
    ↓
Flask API
    ↓
GitHub API
    ↓
Pull Request Diff
    ↓
Ollama LLM
    ↓
Review Validation Pipeline
    ↓
HTML / Markdown Reports
    ↓
GitHub Comments & Email Notifications
```

### Review Flow

1. Trigger review through Postman.
2. Fetch Pull Request details and diffs from GitHub.
3. Send code changes to Ollama.
4. Generate AI review findings.
5. Validate and normalize findings.
6. Perform security scanning.
7. Generate reports.
8. Publish results to GitHub and email notifications.

---

## Key Features

### AI-Powered Review Generation

- Automated code analysis using Ollama
- Prompt-based review generation
- Structured review findings

### Validation & Quality Controls

- JSON output validation
- Evidence verification
- Duplicate finding removal
- Severity classification
- Review normalization

### Security Analysis

- Hardcoded secret detection
- Security-focused review checks

### Reporting

- Markdown reports
- HTML reports
- Review statistics

### Integrations

- GitHub API
- Ollama
- Resend Email API

---

## Software Engineering Concepts Demonstrated

### Architecture & Design

- Modular Architecture
- Separation of Concerns
- Dependency Injection
- Single Responsibility Principle
- Service-Oriented Design

### Backend Development

- REST APIs
- Flask Applications
- API Integrations
- Workflow Orchestration

### Testing

- Unit Testing
- Integration Testing
- Mocking External Services

### AI Engineering

- LLM Integration
- Prompt Engineering
- Output Validation
- AI Reliability Controls

---

## Key Learnings

- Integrating LLMs into production-style workflows requires strong validation mechanisms.
- AI-generated outputs must be normalized and verified before automated usage.
- Combining deterministic validation with AI analysis improves review quality.
- Modular architectures significantly improve maintainability and testability.
- Generative AI can augment software engineering workflows while still requiring quality controls.

---

## Future Enhancements

- Enable automatic GitHub Webhook triggering
- Support OpenAI, Gemini, and Anthropic models
- Dockerized deployment
- CI/CD integration
- Review history tracking
- Multi-repository support
- Analytics dashboard

---

## Repository Structure

```text
AI-Code-Review
│
├── app/
│   ├── github_client.py
│   ├── ollama_client.py
│   ├── review_engine.py
│   ├── reviewer.py
│   ├── security_scanner.py
│   ├── evidence_validator.py
│   └── ...
│
├── config/
├── webhook_server.py
├── generate_report.py
├── requirements.txt
└── README.md
```

---

## Why This Project Matters

This project combines:

- Generative AI
- Software Architecture
- API Development
- Security Analysis
- Testing
- Workflow Automation

into a practical end-to-end system that demonstrates how AI can be integrated into real-world software engineering processes.