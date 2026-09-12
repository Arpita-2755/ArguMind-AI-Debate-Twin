from graph.builder import (moderator_graph, opponent_graph, judge_graph, reflection_graph)
from graph.state import DebateState
from graph.enums import DebatePhase
from services.debate_service import DebateService


print("Creating state...")


state = DebateState(
    topic="Should AI replace software engineers?",
    user_stance="Support",
    ai_stance="Oppose",
    current_phase=DebatePhase.OPENING,
)


# ==========================================
# MODERATOR
# ==========================================

print("\nInvoking moderator...\n")

result = moderator_graph.invoke(state)

state = DebateState(**result)


print("\n========== GENERATED PLAN ==========\n")
print(state.debate_plan)


# ==========================================
# TEST MODE
# ==========================================

state.debate_plan.rounds = 3

print(
    f"\nTEST MODE: Running "
    f"{state.debate_plan.rounds} rounds."
)


# ==========================================
# DEBATE LOOP
# ==========================================

while True:

    print(
        f"\n\n================ ROUND "
        f"{state.current_round} / "
        f"{state.debate_plan.rounds} "
        f"================\n"
    )


    # --------------------------------------
    # USER
    # --------------------------------------

    user_argument = input("Your argument: ")


    # --------------------------------------
    # STORE USER TURN
    # --------------------------------------

    state = DebateService.start_turn(
        state,
        user_argument
    )


    # --------------------------------------
    # OPPONENT
    # --------------------------------------

    result = opponent_graph.invoke(state)

    state = DebateState(**result)


    print("\n========== OPPONENT ==========\n")

    print(
        state.debate_history[-1].opponent_argument
    )


    # --------------------------------------
    # CHECK FINAL ROUND
    # --------------------------------------

    if state.current_round >= state.debate_plan.rounds:

        break


    # --------------------------------------
    # NEXT ROUND
    # --------------------------------------

    state.current_round += 1
# ==========================================
# JUDGE
# ==========================================

print("\n\nInvoking judge...\n")

result = judge_graph.invoke(state)

state = DebateState(**result)


print("\n========== JUDGE RESULT ==========\n")

print(state.judge_result)

# REFLECTION

print("\n\nInvoking reflection...\n")

result = reflection_graph.invoke(state)

state = DebateState(**result)

print("\n========== REFLECTION ==========\n")

print(state.metadata["reflection"])
# ==========================================
# DEBATE FINISHED
# ==========================================

print(
    "\n\n========== DEBATE FINISHED ==========\n"
)

print(
    f"Total rounds: "
    f"{len(state.debate_history)}"
)


# ==========================================
# FULL TRANSCRIPT
# ==========================================

print(
    "\n========== FULL TRANSCRIPT ==========\n"
)


for turn in state.debate_history:

    print(
        f"\nROUND {turn.round_number}"
    )

    print("-" * 50)

    print("\nUSER:")

    print(turn.user_argument)

    print("\nOPPONENT:")

    print(turn.opponent_argument)