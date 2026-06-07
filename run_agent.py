import json
import os

from agent.graph import graph

event_path = os.getenv(
    "GITHUB_EVENT_PATH"
)

with open(event_path) as f:

    event = json.load(f)

pr_number = event[
    "pull_request"
]["number"]

graph.invoke(
    {
        "pr_number": pr_number
    }
)