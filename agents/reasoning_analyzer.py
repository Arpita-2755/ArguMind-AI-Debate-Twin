from agents.base_agent import BaseAgent
from services.reasoning_analyzer_service import ReasoningAnalyzerService


class ReasoningAnalyzerAgent(BaseAgent):

    def __init__(self):
        super().__init__("Reasoning Analyzer")

    def run(self, state):

        reflection = state.metadata["reflection"]

        result = ReasoningAnalyzerService.analyze(
            reflection
        )

        state.metadata["reasoning_fingerprint"] = result

        return state