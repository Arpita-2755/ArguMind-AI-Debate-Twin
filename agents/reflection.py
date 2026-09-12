from agents.base_agent import BaseAgent
from services.reflection_service import ReflectionService
from schemas.debate_transcript import DebateTranscript


class ReflectionAgent(BaseAgent):

    def __init__(self):
        super().__init__("Reflection")

    def run(self, state):

        transcript = DebateTranscript(
            topic=state.topic,
            debate_plan=state.debate_plan,
            turns=state.debate_history
        )

        result = ReflectionService.analyze(
            transcript,
            state.judge_result
        )

        state.metadata["reflection"] = result

        return state