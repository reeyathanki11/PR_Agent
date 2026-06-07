from agent.tools.github_tools import repo


def comment_node(state):

    pr = repo.get_pull(
        state["pr_number"]
    )

    comment = f"""
# 🤖 AI PR Review

Files Reviewed:

{chr(10).join(state['changed_files'])}

---

{state['review_report']}
"""

    pr.create_issue_comment(
        comment
    )

    print(
        "Comment posted successfully"
    )

    return {}