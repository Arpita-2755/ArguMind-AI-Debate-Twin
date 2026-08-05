from agents.base_agent import BaseAgent
from services.moderator_service import ModeratorService


class ModeratorAgent(BaseAgent):

    def __init__(self):
        super().__init__("Moderator")

    def run(self, state):

        plan = ModeratorService.create_plan(state.topic)

        print("\n========== MODERATOR ==========\n")
        print(plan)

        state.debate_plan = plan

        return state