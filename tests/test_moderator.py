from agents.moderator import ModeratorAgent
from graph.enums import DebatePhase
from graph.state import DebateState

state = DebateState(
    topic="Should AI replace software engineers?",
    user_stance="Support",
    ai_stance="Oppose",
    current_phase=DebatePhase.OPENING,
)

moderator = ModeratorAgent()

updated_state = moderator.run(state)

print(updated_state)