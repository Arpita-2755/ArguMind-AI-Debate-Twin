from langgraph.graph import StateGraph, END

from graph.state import DebateState
from graph.nodes import moderator_node

print("Building graph...")

builder = StateGraph(DebateState)

builder.add_node("moderator", moderator_node)

builder.set_entry_point("moderator")

builder.add_edge("moderator", END)

graph = builder.compile()

print("Graph compiled.")