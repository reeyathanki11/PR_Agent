# agent/nodes/comment.py

import os
from github import Github
from agent.state import PRState


def comment_node(state: PRState) -> PRState:
    token     = os.environ.get("GITHUB_TOKEN", "")
    repo_name = os.environ.get("GITHUB_REPOSITORY", "")

    if not token or not repo_name:
        print("[COMMENT] Skipping — GITHUB_TOKEN or GITHUB_REPOSITORY not set.")
        return state

    try:
        g    = Github(token)
        repo = g.get_repo(repo_name)
        pr   = repo.get_pull(state["pr_number"])

        body = state.get("review_report", "No report generated.")

        pr.create_issue_comment(
            body + "\n\n---\n*Posted by AI PR Review Agent*"
        )
        print(f"[COMMENT] ✅ Comment posted on PR #{state['pr_number']}")

    except Exception as e:
        # Do NOT crash the whole agent — just log and move on
        print(f"[COMMENT] ⚠️  Could not post comment: {e}")
        print("[COMMENT]    Check workflow permissions: pull-requests: write")

    return state