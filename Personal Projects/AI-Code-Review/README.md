# AI Code Review System

An automated, AI-powered platform that analyzes GitHub pull request diffs to detect bugs, security vulnerabilities, and code quality issues. The system validates findings against code evidence and generates comprehensive review reports in multiple formats.

Currently, reviews are triggered through a Flask REST API endpoint and tested using Postman. The architecture is designed to be **webhook-ready**, enabling seamless future integration with GitHub Pull Request events.

---

# Features

- API-based review triggering through a Flask REST endpoint
- Pull request diff extraction and parsing
- AI-powered code analysis using Large Language Models (LLMs)
- Review normalization into structured formats
- Finding extraction and parsing
- Evidence-based validation against actual code changes
- Security vulnerability scanning
- Severity and confidence classification
- Duplicate finding detection and removal
- Review statistics generation
- Multi-format reporting (Markdown, HTML, Text)
- Email notification support
- GitHub-ready review comment generation
- Webhook-ready architecture for future GitHub integration

---

# Architecture

The system follows a sequential pipeline architecture that processes code diffs through multiple stages of analysis, validation, and reporting.

## Workflow

```text
API Request (Postman)
        │
        ▼
    Flask API
        │
        ▼
 Diff Extraction
        │
        ▼
   AI Reviewer
        │
        ▼
Review Normalization
        │
        ▼
  Finding Parser
        │
        ▼
Evidence Validator
        │
        ▼
 Security Scanner
        │
        ▼
  Deduplication
        │
        ▼
Severity & Confidence Classification
        │
        ▼
  Report Builder
        │
        ▼
Markdown / HTML Reports
        │
        ▼
 Email Notification
```

## Workflow Explanation

1. A review request is submitted through the Flask API.
2. The system downloads the GitHub Pull Request diff.
3. The AI Reviewer analyzes only the modified code.
4. Raw AI output is normalized into a structured format.
5. Findings are parsed into actionable review items.
6. Findings are validated against the actual code diff.
7. A dedicated security scanner searches for common vulnerability patterns.
8. Duplicate findings are removed.
9. Findings are classified by severity and confidence levels.
10. Reports are generated in Markdown, HTML, and text formats.
11. An email notification containing the review results is sent to stakeholders.

The architecture is intentionally designed to support future GitHub webhook integration with minimal changes.

---

# Tech Stack

| Category | Technology |
|-----------|------------|
| Backend | Python, Flask |
| AI | OpenAI API |
| Source Control | GitHub REST API |
| Notifications | SMTP (`smtplib`) |
| Reporting | Markdown, HTML, JSON |
| Testing | Postman |

---

# Project Structure

```
AI-Code-Review/
│
├── app/
│   ├── review_engine.py
│   ├── review_parser.py
│   ├── evidence_validator.py
│   ├── security_scanner.py
│   ├── report_builder.py
│   ├── markdown_reporter.py
│   ├── html_reporter.py
│   ├── report_statistics.py
│   ├── review_comment_generator.py
│   └── ...
│
├── reports/
│   ├── review_report.md
│   └── review_comments.txt
│
├── reviews/
│
├── webhook_server.py
│
└── README.md
```

## Directory Overview

### `app/`
Contains the core review pipeline including:

- Review orchestration
- AI finding parsing
- Evidence validation
- Security analysis
- Report generation
- Statistics calculation
- Comment generation

### `reports/`
Stores generated review artifacts such as:

- Markdown reports
- HTML reports
- Review comments
- Summary outputs

### `reviews/`
Temporary storage location for downloaded GitHub Pull Request diff files.

### `webhook_server.py`
Flask application entry point that exposes the review API and can be extended for GitHub webhook support.

---

# API Usage

The review process is initiated through a REST API endpoint.

## Endpoint

```http
POST /review
```

## Request Body

```json
{
  "repository": "sample-repo",
  "pull_request": 42,
  "diff_url": "https://github.com/org/repo/pull/42.diff"
}
```

## Response

```json
{
  "status": "success",
  "message": "Review initiated",
  "review_id": "rev_20240101_123456"
}
```

---

# Postman Workflow

1. Create a POST request:

```text
http://localhost:5000/review
```

2. Set the header:

```text
Content-Type: application/json
```

3. Provide the request payload.

4. Submit the request.

5. The system downloads the PR diff, performs analysis, generates reports, and sends the review via email.

---

# Example Finding

```text
[Critical] Division by Zero

File: bad_example.py
Line: 24

Description:
The code performs a division operation without validating that the divisor is non-zero. This can cause a runtime exception.

Recommendation:
Validate the divisor before performing the division to prevent a ZeroDivisionError at runtime.

Confidence: High
```

---

# Example End-to-End Workflow

1. Developer submits a review request through Postman.
2. Flask API receives the request.
3. GitHub Pull Request diff is downloaded.
4. AI Reviewer analyzes the modified code.
5. Findings are parsed and normalized.
6. Evidence Validator verifies findings against code changes.
7. Security Scanner detects known vulnerability patterns.
8. Duplicate findings are removed.
9. Severity and confidence levels are assigned.
10. Markdown, HTML, and text reports are generated.
11. Email notifications are sent to configured recipients.

---

# Key Learnings

## 1. AI Output Normalization

LLM responses can be inconsistent and difficult to process directly. A normalization layer was implemented to convert AI-generated reviews into a consistent JSON schema that downstream services can reliably consume.

### Benefits

- Consistent processing
- Easier validation
- Reduced parsing failures
- Improved report generation

---

## 2. Evidence-Based Validation

AI-generated findings may contain false positives.

Each finding is validated against the actual code diff before being included in the final report.

### Benefits

- Reduced noise
- Increased trust
- More actionable findings
- Improved review quality

---

## 3. Security-First Design

A dedicated Security Scanner complements AI analysis.

### Coverage

- OWASP Top 10 patterns
- CWE vulnerability categories
- Unsafe coding practices
- Common misconfigurations

This layered approach improves overall vulnerability detection.

---

## 4. Duplicate Detection Challenges

Multiple analysis stages may generate similar findings.

The deduplication engine compares:

- File paths
- Line numbers
- Finding categories
- Semantic similarity

This prevents clutter while preserving unique issues.

---

## 5. Pipeline Architecture Benefits

The sequential pipeline design provides:

- Clear separation of concerns
- Easier testing
- Improved maintainability
- Simpler debugging
- Independent component evolution

---

## 6. Severity Classification Complexity

Severity assignment combines:

- Vulnerability category
- Code context
- Potential impact
- AI confidence scores

Levels include:

- Critical
- High
- Medium
- Low

---

## 7. Report Generation Flexibility

Report generation is abstracted from presentation layers.

Supported formats:

- Markdown
- HTML
- Plain Text

This design allows future expansion without modifying core review logic.

---

# Future Enhancements

## GitHub Integration

- GitHub Webhook support
- GitHub Checks API integration
- Inline Pull Request comments

## Analysis Improvements

- Multi-language support
- Custom rule engine
- Auto-fix suggestions
- Improved severity classification

## Platform Features

- Historical review analytics
- Review dashboard
- Team collaboration features
- CI/CD integration
- GitHub Action packaging

---

# About

This project was developed as a personal initiative to explore automated, scalable code review using AI.

The platform demonstrates practical application of:

- AI-assisted code analysis
- REST API design
- Pipeline-based architectures
- Security scanning
- Automated reporting

The source code is not publicly available due to project size and proprietary configuration requirements.

---

# Contact

For questions, collaboration opportunities, or demonstrations, please reach out through GitHub or the contact information available on my portfolio.