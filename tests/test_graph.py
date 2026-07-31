from graph.builder import graph
from graph.state import DebateState
from graph.enums import DebatePhase

print("Creating state...")

state = DebateState(
    topic="Should AI replace software engineers?",
    user_stance="Support",
    ai_stance="Oppose",
    current_phase=DebatePhase.OPENING,
)

print("Invoking graph...")

result = graph.invoke(state)

print("Graph finished.")
print(result)