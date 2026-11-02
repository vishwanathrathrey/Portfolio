"""CLI entry point: review one pull request with the local Ollama models.

In GitHub Actions the PR is read from the event payload (GITHUB_EVENT_PATH).
Locally:  python run_review.py --repo owner/name --pr 12 [--force]

Exit codes: 0 completed/skipped/duplicate, 1 review failed, 2 review completed
but the e-mail could not be delivered."""
from __future__ import annotations

import argparse
import json
import os
import sys

from app.config import load_settings
from app.github_api import GitHubClient, GitHubError
from app.logging_utils import setup_logging
from app.notifier import EmailNotifier
from app.pipeline import ReviewPipeline
from app.providers import build_router
from app.state import ReviewStore

HANDLED_ACTIONS = {"opened", "synchronize", "reopened", "ready_for_review"}


def pr_from_event(path: str):
    with open(path, encoding="utf-8") as fh:
        event = json.load(fh)
    action = event.get("action")
    if action not in HANDLED_ACTIONS:
        return None, f"ignoring pull_request action '{action}'"
    return (event["repository"]["full_name"], int(event["pull_request"]["number"])), ""


def build_pipeline(settings) -> ReviewPipeline:
    github = GitHubClient(settings.github_token, settings.github_api_url)
    return ReviewPipeline(settings, github, build_router(settings),
                          ReviewStore(settings.state_db), EmailNotifier(settings))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", help="owner/name")
    parser.add_argument("--pr", type=int, help="pull request number")
    parser.add_argument("--force", action="store_true", help="re-review even if this commit was reviewed")
    args = parser.parse_args(argv)

    settings = load_settings()
    setup_logging(settings)

    if args.repo and args.pr:
        target = (args.repo, args.pr)
    elif os.environ.get("GITHUB_EVENT_PATH"):
        target, reason = pr_from_event(os.environ["GITHUB_EVENT_PATH"])
        if target is None:
            print(reason)
            return 0
    else:
        parser.error("provide --repo and --pr, or run inside GitHub Actions")

    try:
        result = build_pipeline(settings).run(target[0], target[1], force=args.force)
    except GitHubError as exc:
        print(f"configuration error: {exc}", file=sys.stderr)
        return 1

    print(f"{result.ctx.repo}#{result.ctx.number}: {result.status}"
          + (f" - {result.error}" if result.error else "")
          + (f" ({'; '.join(result.notes)})" if result.notes else ""))
    if result.status == "failed":
        return 1
    if result.status == "completed" and not result.email_delivered:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
