# agent/nodes/collect.py

import os
import difflib
from agent.tools.github_tools import get_pr_details, get_changed_files


def collect_node(state: dict) -> dict:
    pr_number = state["pr_number"]

    print(f"\n[COLLECT] Fetching PR #{pr_number} details...")

    try:
        pr      = get_pr_details(pr_number)
        files   = get_changed_files(pr_number)
    except Exception as e:
        print(f"[COLLECT] ⚠️  GitHub API error: {e} — using state defaults.")
        return state

    git_diff = _build_diff(files)

    return {
        **state,
        "pr_title":       pr.get("title", ""),
        "pr_author":      pr.get("user", {}).get("login", ""),
        "pr_description": pr.get("body") or "",
        "changed_files":  files,
        "git_diff":       git_diff,
    }


def _build_diff(files: list) -> str:
    """Read changed files from disk and produce a unified diff."""
    lines = []
    for path in files:
        if not path.endswith(".py"):
            continue
        try:
            with open(path) as f:
                content = f.readlines()
            lines.append(f"--- a/{path}\n+++ b/{path}\n")
            lines.extend(content[:80])   # first 80 lines as context
        except FileNotFoundError:
            lines.append(f"# {path} not found on disk\n")
    return "".join(lines) if lines else "(no diff)"