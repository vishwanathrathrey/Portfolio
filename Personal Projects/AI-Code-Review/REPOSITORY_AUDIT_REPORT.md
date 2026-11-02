# Repository Audit Report: AI Code Review

Scope: `Personal Projects/AI-Code-Review` plus the new workflow `.github/workflows/ai-code-review.yml`.
Constraint honoured throughout: **all AI inference uses local Ollama** (`qwen2.5-coder:7b` → `mistral`; `nomic-embed-text` reserved). No cloud AI provider is referenced anywhere in code, config or workflow (verified by grep and by a test).

## 1. Existing architecture (before)

A Flask `webhook_server.py` received a GitHub event, downloaded the changed files' `patch` text into `reviews/*.diff` (only `.py`), ran `review_engine` → `reviewer.review_patch` (one raw Ollama call per diff file) → `extract_json` → `normalize_review` → `parse_review` → keyword severity classifier → dedupe, wrote Markdown/HTML reports to `reports/`, posted **one generic PR comment** and e-mailed the HTML through Resend (recipient looked up in `config/users.json`). There was no persistence, no background processing and no CI trigger.

## 2. Issues identified

| # | Issue | Severity | Verified how |
|---|---|---|---|
| 1 | Default model `qwen2.5-coder:3b` is not installed locally (only `7b`, `mistral`, `nomic-embed-text`), so the old flow would 404 | High | `GET /api/tags` |
| 2 | PR files not paginated (GitHub default 30/page): PRs with >30 files silently truncated | High | code review; new pagination test |
| 3 | Reported line numbers were indexes inside the patch text (hunk headers included), the model saw un-numbered diffs, and the evidence validator was **disabled** (`reason = None`), so hallucinated findings passed | High | code review |
| 4 | Invalid/unparseable model JSON normalised to an *empty review*, so a failed review looked like "no issues" | High | code review; new tests |
| 5 | Review ran inside the HTTP request; GitHub's 10 s webhook timeout means deliveries fail while Ollama is still running | High | code review |
| 6 | `reopened` / `ready_for_review` ignored; drafts, closed PRs and forks not filtered; no duplicate protection (`synchronize` + retries re-review) | Medium | code review |
| 7 | Shared mutable `reviews/` and `reports/` directories: concurrent runs race; `a/b.py` and `a_b.py` collide; findings carried the diff file name instead of the repo path | Medium | code review |
| 8 | Diff pasted raw into the prompt: no prompt-injection defence | Medium | code review |
| 9 | HTML report/e-mail not escaped (model or source text could inject markup); e-mail errors crashed the handler; Resend key read at import | Medium | code review |
| 10 | No timeouts on Ollama calls, no health/model checks, no retry/fallback | Medium | code review |
| 11 | Flask debug server on `0.0.0.0` and unauthenticated webhook (fixed in the earlier session, superseded here) | High | code review |
| 12 | `users.json` read via a CWD-relative path; contains a personal e-mail address | Low | code review |

## 3. Bugs and loopholes fixed

All of the above except #12's committed address (left in place; it is the user's own data and is now only a fallback to `REVIEW_EMAIL_TO`). One further defect was found by the new tests while implementing: a PR whose only change is deleted lines completed with no explanatory limitation (the "nothing reviewable" check ran before chunking); fixed in `pipeline.py`.

## 4. Model selection and fallback (`app/providers.py`)

`ModelRouter` tries `OLLAMA_PRIMARY_MODEL` then `OLLAMA_FALLBACK_MODEL`. Per model: `/api/tags` health + installed-model check (never pulls), `format: json`, `(connect, read)` timeouts, bounded retries with exponential backoff for connection/5xx/invalid output, **no retry on timeouts**, then fallback. Missing/unreachable models are cached for the run. Both failing raises `AllModelsFailed`, the review is recorded `failed`, nothing is published, and a failure e-mail is sent. Model used is recorded in the PR review, e-mail and SQLite state.

## 5. GitHub automation (`.github/workflows/ai-code-review.yml`, `run_review.py`)

Chosen architecture: **GitHub Actions + self-hosted runner on the Ollama machine** (outbound-only, no exposed endpoint, jobs queue while the PC is off, concurrency group per PR so only the latest commit is reviewed). Triggers: `opened`, `synchronize`, `reopened`, `ready_for_review`. Job refuses forks and drafts, checks out only the *base* commit, uses a least-privilege token (`contents: read`, `pull-requests: write`). `webhook_server.py` is kept as an optional alternative (HMAC-verified, 202 + single background worker, delivery-id dedupe, 503 without a secret) sharing the same pipeline. The pipeline identifies repo, PR number, branches, head SHA; fetches all files with pagination; and dedupes per (repo, PR, SHA) through an atomic SQLite claim with bounded retry of failed reviews and stale-run recovery.

## 6. E-mail (`app/notifier.py`)

HTML + plain-text report with all required fields and limitations; failure e-mails for all-models-failed, GitHub errors and unexpected errors; everything HTML-escaped; Resend errors caught, redacted and returned (never raised); at most one report and one failure e-mail per commit; on delivery failure the run exits 2 and a re-run resends only the e-mail (the report is stored in the state DB).

## 7. Security improvements

Webhook HMAC verification and fail-closed on missing secret; fork/draft/closed/allow-list filtering; untrusted-input prompt fencing with random boundary and exclusion of PR title/body from prompts; findings accepted only on real added lines; schema-validated output; secrets redacted from logs/errors and never echoed in findings; no execution of PR code (diff text only, base-commit checkout); debug server off by default and bound to localhost; review is always `COMMENT`.

## 8. Files

**Created:** `.github/workflows/ai-code-review.yml`, `.env.example`, `run_review.py`, `pytest.ini`, `REPOSITORY_AUDIT_REPORT.md`, `app/{config,logging_utils,diff_utils,review_schema,providers,github_api,github_publisher,notifier,state,report_model,pipeline}.py`, `tests/{helpers,test_diff_and_schema,test_providers,test_github_state_notify,test_pipeline,test_webhook_and_cli}.py`.
**Changed:** `webhook_server.py` (rewritten), `app/ollama_client.py` (env-driven model/URL, timeout), `app/security_scanner.py` (added `scan_added_lines`), `app/models.py` (optional fields), `app/user_registry.py` (path fix), `README.md`, `tests/test_core.py` (superseded webhook tests removed).
**Removed:** nothing. The legacy file-based modules remain for manual use and are documented as superseded.

## 9. Tests executed

`python -m pytest -q` → **99 passed** (≈1 s, no network, no credentials; GitHub/Ollama/Resend mocked). Also passes with `-W error::ResourceWarning`.

Real-environment checks run against the local Ollama (GitHub and e-mail faked):
* `qwen2.5-coder:7b` reviewed a sample file in 109 s and reported `eval` (line 5), SQL injection (line 7) and division by zero (line 8), all with correct file line numbers.
* With the primary model deliberately set to a non-installed model, the router logged the skip and fell back to `mistral` (75 s), which produced a valid finding.

## 10. Deployment and configuration

See README "Setup": install the runner with label `ai-review` as a service, add `RESEND_API_KEY` and `REVIEW_EMAIL_TO` repository secrets, require approval for outside-collaborator workflows, and merge the workflow to the default branch.

## 11. Remaining manual setup (not performed, requires your accounts/machine)

1. Register the self-hosted runner and add the two secrets.
2. Merge the workflow to the default branch before expecting automatic reviews (the job checks out the base commit).
3. Verify a Resend sender domain if you want a sender other than the shared test address (the default `aireviewer@resend.dev` was preserved from the original code and could not be verified).

## 12. Not verified / known limitations

* **Not run for real:** the GitHub Actions workflow on a runner, calls to the real GitHub API, publishing an actual PR review, and sending a real Resend e-mail. These are covered by mocked tests only; the first live PR is the real acceptance test. The workflow YAML parses and has the intended triggers/condition.
* 7B local models give advisory, imperfect reviews; per-chunk review cannot see cross-file context.
* Review time is hardware-bound (75-109 s for tiny files here); very large PRs take proportionally longer (the job timeout is 60 min).
* Self-hosted runners on public repositories carry inherent risk; mitigations are listed in the README. If you add collaborators, make the repository private or isolate the runner.
* State is per machine (`~/.ai-code-review/state.db`).
* `nomic-embed-text` is configured but unused: the current design needs no embeddings.
