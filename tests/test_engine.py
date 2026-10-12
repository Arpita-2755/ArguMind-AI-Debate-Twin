from engine.debate_engine import DebateEngine
from graph.state import DebateState
from graph.enums import DebatePhase
from schemas.debate_plan import DebatePlan

state = DebateState(
    topic="AI",
    user_stance="Support",
    ai_stance="Against",
    current_phase=DebatePhase.OPENING
)

state.debate_plan = DebatePlan(
    topic="AI",
    category="Technology",
    difficulty="Intermediate",
    strategy="Evidence Driven",
    ai_position="Against",
    rounds=2,
    opening_speaker="User"
)

print(state.current_round)

state = DebateEngine.next_round(state)

print(state.current_round)

print(DebateEngine.is_final_round(state))