from agent.tools.github_tools import repo


def merge_node(state):

    if not state["approved"]:

        print("PR not approved")

        return {}

    pr = repo.get_pull(
        state["pr_number"]
    )

    pr.merge()

    print(
        f"PR #{state['pr_number']} merged"
    )

    return {}