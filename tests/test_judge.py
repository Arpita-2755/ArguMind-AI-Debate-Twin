from agents.judge import JudgeAgent

from graph.state import DebateState
from graph.enums import DebatePhase

from schemas.debate_plan import DebatePlan
from schemas.debate_turn import DebateTurn

state = DebateState(
    topic="Should AI replace software engineers?",
    user_stance="Support",
    ai_stance="Against",
    current_phase=DebatePhase.OPENING
)

state.debate_plan = DebatePlan(
    topic=state.topic,
    category="Technology",
    difficulty="Intermediate",
    strategy="Evidence Driven",
    ai_position="Against",
    rounds=3,
    opening_speaker="User"
)

state.debate_history.append(
    DebateTurn(
        round_number=1,
        phase="Opening",
        user_argument="AI can replace software engineers because it is faster.",
        opponent_argument="Software engineering is more than coding."
    )
)

judge = JudgeAgent()

updated_state = judge.run(state)

print("\n========== FINAL RESULT ==========\n")
print(updated_state.judge_result)