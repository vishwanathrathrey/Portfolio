# AI Code Review (local Ollama, automatic on every pull request)

Every time a pull request is opened or updated, a GitHub Action running **on your own machine** reads the PR diff through the GitHub API, reviews it with **locally hosted Ollama models**, posts a review with inline comments on the PR, and e-mails you a detailed report through Resend.

* **All AI inference is local**: `qwen2.5-coder:7b` (primary), `mistral` (fallback). No Claude, OpenAI, Gemini or any cloud AI API is used or configurable. Models are never downloaded automatically.
* Ollama is never exposed to the internet: the runner talks to `http://localhost:11434`.
* PR code is never executed. Only the diff text is read.

---

## How a PR automatically triggers a local Ollama review

```text
 You open / push to a PR
          │  pull_request: opened | synchronize | reopened | ready_for_review
          ▼
 GitHub Actions  (.github/workflows/ai-code-review.yml)
          │  job is queued for runner label "ai-review"
          ▼
 Self-hosted runner on YOUR PC  ── checks out the BASE commit only (never PR code)
          │  python run_review.py
          ▼
 GitHub REST API: PR metadata + all changed files (paginated)
          │  filter → chunk (numbered lines) → prompt (diff fenced as untrusted)
          ▼
 Ollama @ localhost:11434   qwen2.5-coder:7b ──fails/times out/invalid──▶ mistral
          │  strict JSON validation, findings only on real added lines
          ▼
 ┌────────────────────┬──────────────────────────┐
 │ GitHub PR review   │ Resend e-mail (HTML+text) │   (independent of each other)
 │ summary + inline   │ report or failure notice  │
 └────────────────────┴──────────────────────────┘
          SQLite state (~/.ai-code-review/state.db): one row per PR + commit SHA
```

Why a self-hosted runner and not a webhook: your models live on your PC, and a GitHub-hosted runner cannot reach `localhost`. A webhook would need a public tunnel to your machine (an exposed endpoint, and GitHub does not auto-retry failed deliveries). With a self-hosted runner the connection is outbound-only, GitHub queues the job while the PC is off, and no secret or tunnel is needed.

**If the PC is off:** the job waits in the queue and runs when the runner comes back (GitHub fails a queued job that finds no runner after 24 h; re-run it from the Actions tab). A newer push to the same PR cancels the older pending run, so only the latest commit is reviewed.

`webhook_server.py` remains as an **optional alternative** trigger that shares the same pipeline (see below). Use one trigger, not both.

---

## What a review contains

Each finding has: file, changed-line reference, severity (critical/high/medium/low), category, title, explanation, why it matters, suggested fix and confidence.

* Line numbers are **real file line numbers**: the model sees every diff line prefixed with its number, and a finding is accepted only if it points at an *added* line. Anything else is discarded and counted under "limitations".
* Hard-coded secrets are also found by a deterministic scanner (the secret value is never copied into reports).
* Output is schema-validated. Invalid or empty-by-error model output is **never** treated as "no issues": it is retried (bounded), then the fallback model is tried, then the review is marked **failed**.
* Large PRs are split per file and per size-bounded chunk; deleted/binary/lock/generated/unsupported files, files over the configured limits, and truncated lines are all listed in the report. Nothing is skipped silently.

---

## Setup

### 1. Prerequisites
* Python 3.10+ (tested on 3.12), Git
* [Ollama](https://ollama.com/download) running locally, with the models already pulled:
  ```bash
  ollama list        # must show qwen2.5-coder:7b and mistral (nomic-embed-text is reserved, not used)
  ```
  The reviewer **never** runs `ollama pull`. If a model is missing it logs that and moves on.
* A Resend account and API key: https://resend.com

### 2. Python environment
```bash
cd "Personal Projects/AI-Code-Review"
python -m venv .venv
.venv\Scripts\activate            # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env            # Linux/macOS: cp .env.example .env  (then fill it in; never commit it)
```

### 3. Try it locally on a real PR
```bash
python run_review.py --repo owner/name --pr 12          # add --force to re-review the same commit
```
`GITHUB_TOKEN` in `.env` must be a fine-grained token limited to the repo: *Pull requests: read/write*, *Contents: read*.

### 4. Turn on automatic triggering (GitHub Actions + self-hosted runner)
1. **Add a runner** on the machine that runs Ollama: repo → *Settings → Actions → Runners → New self-hosted runner*. Follow the commands for your OS, give it the extra label **`ai-review`**, and install it as a **service** so it survives reboots (Windows: answer *Y* to "run as a service").
2. The runner needs `python` and `git` on its PATH.
3. **Secrets** (*Settings → Secrets and variables → Actions*): `RESEND_API_KEY`, `REVIEW_EMAIL_TO`. (`GITHUB_TOKEN` is provided by GitHub with only `contents: read` and `pull-requests: write`.)
4. **Fork safety** (*Settings → Actions → General*): set *Fork pull request workflows from outside collaborators* to **Require approval for all outside collaborators**. The workflow additionally refuses to run for forks and drafts.
5. **Merge the workflow to your default branch first.** The job checks out the PR's *base* commit (so a PR can never change the code that reviews it), which means the very first PR that adds this workflow cannot review itself. Every PR after that is reviewed automatically.

Note: GitHub recommends against self-hosted runners on **public** repositories because workflow code from forks can run on them. The mitigations above (no fork runs, outside-collaborator approval, base-commit checkout, least-privilege token) cover this for a single-contributor repository, but if you ever add collaborators, make the repo private or move the runner to an isolated VM.

### Optional: webhook instead of Actions
```bash
# .env: GITHUB_WEBHOOK_SECRET=<random string>
python webhook_server.py        # binds to 127.0.0.1:5000
```
Expose `/webhook` only through a secured tunnel, add a GitHub webhook (content type `application/json`, same secret, event *Pull requests*). Deliveries are authenticated by HMAC-SHA256, acknowledged immediately (`202`) and processed one at a time. The server returns `503` if no secret is configured. Do not enable both triggers.

---

## Model selection and fallback

| Order | Model (env var) | Used when |
|---|---|---|
| 1 | `qwen2.5-coder:7b` (`OLLAMA_PRIMARY_MODEL`) | always tried first |
| 2 | `mistral` (`OLLAMA_FALLBACK_MODEL`) | primary missing, Ollama error, generation timeout, or invalid output after bounded retries |
| – | `nomic-embed-text` (`OLLAMA_EMBEDDING_MODEL`) | reserved for embeddings; this project does not need them, so it is never called |

Before inference the server's `/api/tags` is checked and the model must be installed. Connection errors/5xx and invalid output are retried `OLLAMA_MAX_RETRIES` times (default 1) with exponential backoff; timeouts are not retried on the same model. If both models fail the review is recorded as **failed**, nothing is published to the PR, and a failure e-mail is sent. The model used is recorded in the PR review, e-mail and state database.

## E-mail (Resend)

Sent after every completed review (HTML + plain text, all content HTML-escaped): repository, PR number/title/URL, author, branches, commit SHA, completion time, models, summary, findings grouped critical → low with file:line and suggested fixes, and the review limitations. Failure e-mails are sent when Ollama/both models fail, the GitHub API fails, or processing crashes. E-mail is independent of GitHub publishing; if publishing fails the e-mail still goes out and mentions it. If e-mail delivery fails the run exits with code 2 (visible in Actions), the state records it, and re-running the workflow resends **only** the e-mail. One e-mail per commit.

`REVIEW_EMAIL_FROM` defaults to `aireviewer@resend.dev`; Resend's shared test sender only delivers to your own Resend account address, so verify a domain for any other recipient.

## Configuration

All settings are environment variables (see [.env.example](.env.example)):

| Variable | Default | Purpose |
|---|---|---|
| `GITHUB_TOKEN` | – | GitHub API access (provided by Actions) |
| `GITHUB_WEBHOOK_SECRET` | – | Webhook HMAC secret (webhook mode only) |
| `ALLOWED_REPOS` | any | Optional comma-separated allow-list |
| `PUBLISH_GITHUB_REVIEW` / `MAX_INLINE_COMMENTS` | `true` / `25` | PR review publishing |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server |
| `OLLAMA_PRIMARY_MODEL` / `OLLAMA_FALLBACK_MODEL` / `OLLAMA_EMBEDDING_MODEL` | `qwen2.5-coder:7b` / `mistral` / `nomic-embed-text` | Models |
| `OLLAMA_CONNECT_TIMEOUT` / `OLLAMA_GENERATE_TIMEOUT` | `5` / `600` s | Timeouts |
| `OLLAMA_MAX_RETRIES` / `OLLAMA_RETRY_BACKOFF` | `1` / `2` | Retry policy |
| `OLLAMA_NUM_CTX` / `OLLAMA_TEMPERATURE` | `8192` / `0.1` | Generation parameters |
| `MAX_CHUNK_CHARS` / `MAX_FILES` / `MAX_TOTAL_CHARS` | `6000` / `50` / `120000` | Diff limits |
| `RESEND_API_KEY`, `REVIEW_EMAIL_TO`, `REVIEW_EMAIL_FROM` | – | E-mail |
| `AI_REVIEW_STATE_DB` | `~/.ai-code-review/state.db` | Review state / dedupe |
| `APP_ENV`, `LOG_LEVEL` | `development`, `INFO` | Runtime |

## Security

* Webhook mode verifies `X-Hub-Signature-256` (constant-time) and refuses to run without a secret; Actions mode needs no inbound endpoint.
* Reviews are skipped for forks, drafts, closed PRs and repositories outside `ALLOWED_REPOS`.
* Repository content is untrusted: the diff is fenced by a random per-call boundary and the model is told to treat it as data; PR titles, descriptions and commit messages are never put in the prompt; findings must point at real added lines; output is schema-validated; nothing from a PR is executed.
* Tokens and API keys are read from the environment, redacted from logs and error messages, and never put in e-mail.
* The GitHub token needs only `pull-requests: write` and `contents: read`. The review is always a `COMMENT`; it never approves, requests changes, or merges.
* The Flask debugger is off by default and the webhook binds to `127.0.0.1`.

## Testing

```bash
pip install pytest
python -m pytest -q
```
Runs `tests/` only. GitHub, Ollama and Resend are mocked; no credentials are needed. Covered: PR event handling, signature validation, duplicate-event/commit prevention, pagination, large PRs, model selection, primary failure, fallback, both models down, invalid output, schema validation, prompt-injection safeguards, e-mail delivery and failure, duplicate notifications, GitHub review publishing, retry/timeout behaviour and the end-to-end workflow. The `test_*.py` files in the project root are the original manual smoke scripts (some call live services) and are not part of the automated run. `app/bad_example.py` is an intentionally insecure fixture.

## Troubleshooting

| Symptom | Check |
|---|---|
| Job stays "Queued" | Runner offline or missing the `ai-review` label; start the runner service. |
| `All local Ollama models failed` e-mail | Is Ollama running? `ollama list` must show both models. The e-mail lists each model's reason. |
| `model '…' is not installed locally` | Pull it yourself (`ollama pull …`); the tool never downloads models. |
| Generation timeouts on big PRs | Raise `OLLAMA_GENERATE_TIMEOUT` or lower `MAX_CHUNK_CHARS`. |
| Nothing happens on a PR | Draft, fork, or the workflow is not on the default branch yet. |
| Review not re-run for a commit | By design (dedupe). Use `python run_review.py --repo … --pr … --force`. |
| Email not delivered | `RESEND_API_KEY`/`REVIEW_EMAIL_TO` set? Sender domain verified? Re-run the workflow to resend. |
| GitHub review has no inline comments | Findings outside the diff are listed in the summary instead; a rejected inline batch falls back to a summary-only review. |

## Known limitations

* A 7B local model produces useful but imperfect reviews; treat output as advisory. Expect false negatives and occasional false positives.
* Reviews are per file/chunk and do not see the rest of the repository, so cross-file issues can be missed.
* Review speed depends on your hardware (a one-file review took 1-2 minutes in testing).
* Only source files with a known suffix are reviewed (`diff_utils.REVIEWABLE_SUFFIXES`); files GitHub returns without a patch (binary or very large diffs) are reported as skipped.
* Review state lives on the runner machine; if it is wiped, commits may be reviewed again.
* The original file-based flow (`generate_report.py`, `review_engine.py`, `report_service.py`, …) is kept for manual local use but is superseded by `app/pipeline.py`.

## Project structure

```text
AI-Code-Review/
├── run_review.py            # CLI / Actions entry point
├── webhook_server.py        # optional webhook trigger (same pipeline)
├── app/
│   ├── pipeline.py          # orchestration, dedupe, delivery, failure handling
│   ├── providers.py         # Ollama providers, health checks, fallback router
│   ├── review_schema.py     # prompt + strict output validation
│   ├── diff_utils.py        # patch parsing, file filtering, chunking
│   ├── github_api.py        # paginated, retrying GitHub client
│   ├── github_publisher.py  # PR review + inline comments
│   ├── notifier.py          # Resend HTML/text e-mail
│   ├── state.py             # SQLite duplicate prevention / status
│   ├── config.py, logging_utils.py, report_model.py
│   └── (legacy modules for the manual file-based flow)
├── tests/                   # offline test suite
└── .env.example
```
The workflow lives at the repository root: `.github/workflows/ai-code-review.yml`.
