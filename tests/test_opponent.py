from agents.opponent import OpponentAgent
from graph.state import DebateState
from graph.enums import DebatePhase
from schemas.debate_plan import DebatePlan
from services.debate_service import DebateService

plan = DebatePlan(
    topic="Should AI replace software engineers?",
    category="Technology",
    difficulty="Intermediate",
    strategy="Evidence Driven",
    ai_position="Against",
    rounds=5,
    opening_speaker="User"
)

state = DebateState(
    topic=plan.topic,
    user_stance="Support",
    ai_stance="Against",
    current_phase=DebatePhase.OPENING,
)

state.debate_plan = plan

state = DebateService.start_turn(
    state,
    "AI will write most code within a decade, so most engineers become unnecessary."
)

agent = OpponentAgent()

state = agent.run(state)

print(state.debate_history[-1].opponent_argument)