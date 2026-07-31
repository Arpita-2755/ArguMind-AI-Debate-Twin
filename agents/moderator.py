from agents.base_agent import BaseAgent
from services.moderator_service import ModeratorService


class ModeratorAgent(BaseAgent):

    def __init__(self):
        super().__init__("Moderator")

    def run(self, state):

        analysis = ModeratorService.analyze_topic(state.topic)

        print("\n========== MODERATOR ==========\n")
        print(analysis)

        return state