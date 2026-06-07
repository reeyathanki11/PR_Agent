from agent.tools.llm_tools import ask_llm


def autofix_node(state):

    prompt = f"""
Fix all Ruff issues.

Fix all Bandit issues.

Keep business logic unchanged.

Return ONLY Python code.

Code:

{state['file_contents']}
"""

    fixed_code = ask_llm(prompt)

    file_path = state["changed_files"][0]

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(fixed_code)

    return {}