from agent.prompts.review import (
    REVIEW_PROMPT
)

from agent.tools.llm_tools import (
    ask_llm
)


def review_node(state):

    prompt = REVIEW_PROMPT.format(
        code=state["file_contents"]
    )

    report = ask_llm(prompt)

    return {
        "review_report": report
    }