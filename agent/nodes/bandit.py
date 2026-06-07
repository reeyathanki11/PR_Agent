import subprocess


def bandit_node(state):

    result = subprocess.run(
        [
            "bandit",
            "-r",
            "."
        ],
        capture_output=True,
        text=True
    )

    return {
        "bandit_output": result.stdout
    }