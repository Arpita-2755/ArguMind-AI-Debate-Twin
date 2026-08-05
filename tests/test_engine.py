from engine.debate_engine import DebateEngine
from graph.state import DebateState
from graph.enums import DebatePhase

state = DebateState(
    topic="AI",
    user_stance="Support",
    ai_stance="Against",
    current_phase=DebatePhase.OPENING
)

print(state.current_round)

state = DebateEngine.next_round(state)

print(state.current_round)

print(DebateEngine.debate_finished(state))