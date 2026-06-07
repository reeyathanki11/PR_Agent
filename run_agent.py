# run_agent.py

import json
import os
import sys

from agent.graph import graph


def main():
    # ── Read the GitHub event payload ────────────────────────
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path:
        print("ERROR: GITHUB_EVENT_PATH is not set.")
        sys.exit(1)

    if not os.path.exists(event_path):
        print(f"ERROR: Event file not found at {event_path}")
        sys.exit(1)

    with open(event_path) as f:
        event = json.load(f)

    # ── Extract PR number safely ──────────────────────────────
    pull_request = event.get("pull_request")
    if not pull_request:
        print("INFO: No pull_request key in event. Not a PR event — skipping.")
        sys.exit(0)                   # exit 0 = not an error, just skip

    pr_number = pull_request.get("number")
    if not pr_number:
        print("ERROR: pull_request.number missing from event payload.")
        sys.exit(1)

    repo_full_name = os.environ.get(
        "GITHUB_REPOSITORY",
        event.get("repository", {}).get("full_name", "unknown/unknown")
    )
    base_branch = pull_request.get("base", {}).get("ref", "main")
    head_branch = pull_request.get("head", {}).get("ref", "")

    print(f"[run_agent] PR #{pr_number} on {repo_full_name}  ({head_branch} → {base_branch})")

    # ── Build initial state ───────────────────────────────────
    initial_state = {
        "pr_number":          pr_number,
        "repo_full_name":     repo_full_name,
        "base_branch":        base_branch,
        "head_branch":        head_branch,
        "pr_title":           pull_request.get("title", ""),
        "pr_author":          pull_request.get("user", {}).get("login", "unknown"),
        "pr_description":     pull_request.get("body", "") or "",
        "changed_files":      [],
        "git_diff":           "",
        "black_issues":       [],
        "ruff_issues":        [],
        "bandit_issues":      [],
        "llm_review_issues":  [],
        "security_issues":    [],
        "autofix_applied":    False,
        "autofix_log":        [],
        "generated_tests":    "",
        "pytest_output":      "",
        "pytest_passed":      False,
        "pytest_retry_count": 0,
        "docs_generated":     "",
        "review_report":      "",
        "severity_counts":    {},
        "confidence_score":   0.0,
        "approval_status":    "pending",
        "block_reason":       None,
        "should_block":       False,
        "retry_count":        0,
    }

    # ── Run the graph ─────────────────────────────────────────
    try:
        result = graph.invoke(initial_state)
        print(f"\n[run_agent] ✅ Agent completed.")
        print(f"            Confidence : {result.get('confidence_score', 0) * 100:.0f}%")
        print(f"            Tests pass : {result.get('pytest_passed', False)}")
        print(f"            Approval   : {result.get('approval_status', 'pending')}")
    except Exception as e:
        print(f"\n[run_agent] ❌ Agent failed: {e}")
        raise


if __name__ == "__main__":
    main()