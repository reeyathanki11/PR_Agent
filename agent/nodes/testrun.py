import subprocess


def testrun_node(state):

    result = subprocess.run(
        [
            "pytest"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:

        return {
            "test_result": "PASS"
        }

    return {
        "test_result": "FAIL",
        "retry_count":
            state["retry_count"] + 1
    }