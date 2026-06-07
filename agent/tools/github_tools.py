# agent/tools/github_tools.py

import os
import requests


def _headers():
    token = os.environ.get("GITHUB_TOKEN", "")
    return {
        "Authorization":        f"Bearer {token}",
        "Accept":               "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _repo():
    """Read repo name lazily at call time, not at import time."""
    repo = os.environ.get("GITHUB_REPOSITORY") or os.environ.get("GITHUB_REPO")
    if not repo:
        raise ValueError("GITHUB_REPOSITORY env var is not set.")
    return repo


def get_pr_details(pr_number: int) -> dict:
    url = f"https://api.github.com/repos/{_repo()}/pulls/{pr_number}"
    r = requests.get(url, headers=_headers(), timeout=15)
    r.raise_for_status()
    return r.json()


def get_changed_files(pr_number: int) -> list:
    url = f"https://api.github.com/repos/{_repo()}/pulls/{pr_number}/files"
    r = requests.get(url, headers=_headers(), timeout=15)
    r.raise_for_status()
    return [f["filename"] for f in r.json()]


def post_comment(pr_number: int, body: str):
    url = f"https://api.github.com/repos/{_repo()}/issues/{pr_number}/comments"
    r = requests.post(url, headers=_headers(), json={"body": body}, timeout=15)
    if r.status_code == 201:
        print(f"[GITHUB] ✅ Comment posted on PR #{pr_number}")
    else:
        print(f"[GITHUB] ⚠️  {r.status_code}: {r.json().get('message', r.text[:200])}")


def merge_pr(pr_number: int, title: str):
    url = f"https://api.github.com/repos/{_repo()}/pulls/{pr_number}/merge"
    r = requests.put(
        url,
        headers=_headers(),
        json={"commit_title": title, "merge_method": "squash"},
        timeout=15,
    )
    if r.status_code == 200:
        print(f"[GITHUB] ✅ PR #{pr_number} merged.")
    else:
        print(f"[GITHUB] ⚠️  Merge failed {r.status_code}: {r.json().get('message', '')}")