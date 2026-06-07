import os

from github import Github

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")

REPO = os.getenv("GITHUB_REPO")

github_client = Github(TOKEN)

repo = github_client.get_repo(REPO)