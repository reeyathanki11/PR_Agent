import subprocess


def black_node(state):

    subprocess.run(
        [
            "black",
            "."
        ]
    )

    return {}