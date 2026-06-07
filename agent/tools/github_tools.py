import os
from github import Github

TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    raise ValueError(
        "GITHUB_TOKEN not found. Check repository secret AI_GITHUB_TOKEN."
    )

REPO = os.getenv("GITHUB_REPO")

if not REPO:
    raise ValueError(
        "GITHUB_REPO not found."
    )

github_client = Github(TOKEN)

repo = github_client.get_repo(REPO)