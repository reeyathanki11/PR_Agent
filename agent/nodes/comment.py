import os
import requests


def comment_node(state: dict) -> dict:
    token     = os.environ.get("GITHUB_TOKEN", "")
    repo      = os.environ.get("GITHUB_REPOSITORY", "")
    pr_number = state.get("pr_number")

    if not token or not repo or not pr_number:
        print("[COMMENT] Missing token/repo/pr_number — skipping.")
        return state

    body = state.get("review_report", "Agent completed.")
    body = f"{body}\n\n---\n*Posted by AI PR Review Agent*"

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization":        f"Bearer {token}",
        "Accept":               "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    try:
        r = requests.post(url, headers=headers, json={"body": body}, timeout=15)
        if r.status_code == 201:
            print(f"[COMMENT] ✅ Posted on PR #{pr_number}")
        else:
            print(f"[COMMENT] ⚠️  {r.status_code}: {r.json().get('message', r.text[:200])}")
    except Exception as e:
        print(f"[COMMENT] ❌ {e}")

    return state