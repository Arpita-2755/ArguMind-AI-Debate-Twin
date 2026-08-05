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
print()

print("\n========== GENERATED PLAN ==========\n")

print(type(result))
history = result["debate_history"]

print()

print("========== DEBATE HISTORY ==========")

history = result["debate_history"]

print()

print("========== DEBATE ==========")

for turn in history:

    print()

    print(f"Round {turn.round_number}")

    print()

    print("User")

    print("-"*20)

    print(turn.user_argument)

    print()

    print("Opponent")

    print("-"*20)

    print(turn.opponent_argument)