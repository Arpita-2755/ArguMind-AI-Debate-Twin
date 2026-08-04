from agents.moderator import ModeratorAgent
from graph.state import DebateState
from graph.enums import DebatePhase

state = DebateState(
    topic="Should AI replace software engineers?",
    user_stance="Support",
    ai_stance="Oppose",
    current_phase=DebatePhase.OPENING
)

moderator = ModeratorAgent()

updated_state = moderator.run(state)

print("\n========== STATE PLAN ==========\n")
print(updated_state.plan)