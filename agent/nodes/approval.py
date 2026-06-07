def approval_node(state):

    if state["test_result"] != "PASS":

        return {
            "approved": False
        }

    if state["bandit_output"]:

        return {
            "approved": False
        }

    return {
        "approved": True
    }