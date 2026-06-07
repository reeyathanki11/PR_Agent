import subprocess


def ruff_node(state):

    result = subprocess.run(
        [
            "ruff",
            "check",
            "."
        ],
        capture_output=True,
        text=True
    )

    return {
        "ruff_output": result.stdout,
        "issues_found": bool(result.stdout.strip())
    }