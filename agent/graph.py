from langgraph.graph import (
    StateGraph,
    END
)

from agent.state import PRState

from agent.nodes.collect import (
    collect_node
)

from agent.nodes.review import (
    review_node
)

from agent.nodes.comment import (
    comment_node
)

builder = StateGraph(PRState)

# Nodes
builder.add_node(
    "collect",
    collect_node
)

builder.add_node(
    "review",
    review_node
)

builder.add_node(
    "comment",
    comment_node
)

# Entry Point
builder.set_entry_point(
    "collect"
)

# Flow
builder.add_edge(
    "collect",
    "review"
)

builder.add_edge(
    "review",
    "comment"
)

builder.add_edge(
    "comment",
    END
)

# Compile Graph
graph = builder.compile()