from agents.base_agent import BaseAgent

from services.judge_service import JudgeService

from schemas.debate_transcript import DebateTranscript


class JudgeAgent(BaseAgent):

    def __init__(self):
        super().__init__("Judge")

    def run(self, state):

        print("\n========== JUDGE ==========\n")

        transcript = DebateTranscript(
            topic=state.topic,
            debate_plan=state.debate_plan,
            turns=state.debate_history
        )

        result = JudgeService.evaluate(transcript)

        state.judge_result = result

        print(result)

        return state