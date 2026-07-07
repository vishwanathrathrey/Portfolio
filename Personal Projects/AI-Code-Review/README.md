# AI-Powered Code Review Assistant

## Overview

This project implements an AI-powered code review assistant that automates the process of reviewing GitHub pull requests. The system listens for pull request events via a webhook, fetches the code changes, analyzes them using a local Large Language Model (LLM) via Ollama, and posts formatted review comments back to the pull request. The entire application is designed as a modular, event-driven system, showcasing best practices in software engineering, including dependency injection, clear separation of concerns, and comprehensive testing.

## Recruiter Snapshot

This project demonstrates:
- **End-to-End System Design:** Competency in designing and building a complete, event-driven application, from webhook ingestion to external API interaction (GitHub, Ollama) and back.
- **LLM/Generative AI Integration:** Practical experience in integrating a Large Language Model (Ollama) to perform a core business logic task (code review), including prompt engineering and output parsing.
- **Software Engineering Best Practices:** Strong adherence to modern software engineering principles, including a modular architecture with clear separation of concerns, dependency injection for loose coupling, and a focus on testability.
- **Robust Testing Strategy:** A comprehensive testing suite with high coverage, including unit tests for individual components and integration tests for key workflows, demonstrating a commitment to code quality and reliability.
- **API and Webhook Integration:** Proficiency in building a web server (Flask) to handle incoming webhooks and interacting with external REST APIs (GitHub API) for a real-world integration scenario.

## Features

- **Webhook-driven:** Listens for GitHub pull request events (`opened`, `reopened`, `synchronize`).
- **AI-Powered Analysis:** Uses a local LLM (via Ollama) to analyze code diffs and generate review suggestions.
- **Automated Commenting:** Posts review comments directly to the relevant lines in the GitHub pull request.
- **Configurable:** Easily configured via a `config.ini` file for different models, prompts, and GitHub settings.
- **Modular and Testable:** Built with a clean, modular architecture that is easy to maintain and test.

## Architecture

The system is composed of several key modules, each with a distinct responsibility:

1.  **`webhook_server.py` (Entry Point):**
    - A Flask-based web server that exposes a `/webhook` endpoint.
    - Receives and validates incoming GitHub webhook payloads.
    - Parses the pull request data and triggers the core processing logic.

2.  **`pr_service.py` (Orchestrator):**
    - The central service that orchestrates the entire code review process.
    - Fetches the pull request diff, invokes the AI analysis, formats the comments, and posts the review to GitHub.

3.  **`ollama_client.py` (LLM Interaction):**
    - A client for interacting with the Ollama API.
    - Sends the code diff and a system prompt to the LLM and retrieves the AI-generated review.

4.  **`github_client.py` (GitHub API Interaction):**
    - A client for interacting with the GitHub REST API.
    - Handles fetching pull request diffs and posting review comments.

5.  **`review_comment_generator.py` & `comment_formatter.py` (Output Processing):**
    - Responsible for parsing the raw JSON output from the LLM and formatting it into review comments that the GitHub API can accept.

6.  **Dependency Injection:**
    - The system makes extensive use of dependency injection. Services like `PRService` are initialized with client instances (`OllamaClient`, `GithubClient`), which makes the components loosely coupled and highly testable.

## Project Workflow

1.  A developer opens or updates a pull request on a configured GitHub repository.
2.  GitHub sends a webhook payload to the running Flask server.
3.  The `webhook_server` receives the payload, validates it, and passes the PR data to the `PRService`.
4.  `PRService` uses the `GithubClient` to fetch the `.diff` file for the pull request.
5.  The diff content is sent to the `OllamaClient`, which queries the local LLM for a code review.
6.  The LLM returns a JSON object containing review suggestions.
7.  The `review_comment_generator` parses this JSON.
8.  `PRService` uses the `GithubClient` again to post the formatted comments to the pull request.

## Techniques and Concepts Applied

| Technique | Application |
|---|---|
| **Webhook Integration** | Using a Flask server to receive and process real-time events from GitHub. |
| **LLM Integration** | Interacting with the Ollama API to leverage a local LLM for code analysis. |
| **REST API Consumption** | Making authenticated requests to the GitHub API to fetch data and post comments. |
| **Modular Architecture** | Structuring the code into independent, single-responsibility modules (clients, services, parsers). |
| **Dependency Injection** | Decoupling components by passing dependencies (like clients) during initialization. |
| **Unit & Integration Testing** | Using `pytest` and `unittest.mock` to create a comprehensive test suite with high coverage. |
| **Configuration Management** | Using `configparser` to manage application settings in an external file. |

## Key Learnings

- **Importance of Modular Design:** The modular architecture was critical for managing complexity and enabling effective testing. Each component could be developed and tested in isolation.
- **Challenges of LLM Output Parsing:** Reliably parsing the output from an LLM requires robust error handling and a flexible parsing strategy, as the format can sometimes be inconsistent.
- **Testing External Integrations:** Using mock objects (`unittest.mock`) is an essential technique for testing components that interact with external APIs, allowing for fast and reliable tests without making real network requests.

## Future Work

- **Support for More LLMs:** Abstract the LLM client further to support other models and APIs (e.g., OpenAI, Anthropic).
- **Advanced Prompt Engineering:** Implement more sophisticated prompt engineering techniques to improve the quality and relevance of the AI-generated reviews.
- **Batching and Caching:** Introduce caching for diffs and batching for comments to improve performance and handle rate limits more gracefully.
- **Interactive Feedback Loop:** Allow users to provide feedback on review comments to fine-tune the AI model over time.

## Repository Structure

```
AI-Code-Review/
├── app/                    # Core application logic
├── config/                 # Configuration files
├── tests/                  # Unit and integration tests
├── generate_report.py      # Script to generate test coverage reports
├── requirements.txt        # Python dependencies
└── webhook_server.py       # Flask server entry point
```

## Notes
- This project is a personal endeavor to explore the practical application of LLMs in the software development lifecycle. It demonstrates a strong understanding of modern software architecture and GenAI integration.
