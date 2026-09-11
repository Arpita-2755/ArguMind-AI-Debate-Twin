from langgraph.graph import StateGraph, END

from graph.state import DebateState
from graph.nodes import (
    moderator_node,
    opponent_node,
    judge_node
)


print("Building graph...")


# ==========================================
# MODERATOR GRAPH
# ==========================================

moderator_builder = StateGraph(DebateState)

moderator_builder.add_node(
    "moderator",
    moderator_node
)

moderator_builder.set_entry_point("moderator")

moderator_builder.add_edge(
    "moderator",
    END
)

moderator_graph = moderator_builder.compile()


# ==========================================
# OPPONENT GRAPH
# ==========================================

opponent_builder = StateGraph(DebateState)

opponent_builder.add_node(
    "opponent",
    opponent_node
)

opponent_builder.set_entry_point("opponent")

opponent_builder.add_edge(
    "opponent",
    END
)

opponent_graph = opponent_builder.compile()


# ==========================================
# JUDGE GRAPH
# ==========================================

judge_builder = StateGraph(DebateState)

judge_builder.add_node(
    "judge",
    judge_node
)

judge_builder.set_entry_point("judge")

judge_builder.add_edge(
    "judge",
    END
)

judge_graph = judge_builder.compile()


print("Graphs compiled.")