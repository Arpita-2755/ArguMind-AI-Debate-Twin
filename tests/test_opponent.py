from agents.opponent import OpponentAgent
from graph.state import DebateState
from graph.enums import DebatePhase
from schemas.debate_plan import DebatePlan

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

state.plan = plan

agent = OpponentAgent()

agent.run(state)