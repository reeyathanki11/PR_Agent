# agent/nodes/collect.py

import os
import difflib
from agent.tools.github_tools import get_pr_details, get_changed_files


def collect_node(state: dict) -> dict:
    pr_number = state["pr_number"]
    print(f"\n[COLLECT] Fetching PR #{pr_number} details...")

    try:
        pr    = get_pr_details(pr_number)
        files = get_changed_files(pr_number)
    except Exception as e:
        print(f"[COLLECT] ⚠️  GitHub API error: {e} — using empty defaults.")
        return {
            **state,
            "changed_files": [],
            "git_diff":      "",
            "file_contents": {},
        }

    # Read each changed file from disk into a dict
    file_contents = {}
    for path in files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                file_contents[path] = f.read()
        except FileNotFoundError:
            file_contents[path] = f"# {path} not found on disk"
        except Exception as e:
            file_contents[path] = f"# Could not read {path}: {e}"

    git_diff = _build_diff(file_contents)

    print(f"[COLLECT] Found {len(files)} changed file(s): {files}")
    print(f"[COLLECT] Diff size: {len(git_diff)} chars")

    return {
        **state,
        "pr_title":       pr.get("title", ""),
        "pr_author":      pr.get("user", {}).get("login", ""),
        "pr_description": pr.get("body") or "",
        "changed_files":  files,
        "git_diff":       git_diff,
        "file_contents":  file_contents,
    }


def _build_diff(file_contents: dict) -> str:
    lines = []
    for path, content in file_contents.items():
        if not path.endswith(".py"):
            continue
        lines.append(f"--- a/{path}\n+++ b/{path}")
        lines.append(content[:3000])   # cap per file to avoid token overflow
    return "\n".join(lines) if lines else "(no diff)"