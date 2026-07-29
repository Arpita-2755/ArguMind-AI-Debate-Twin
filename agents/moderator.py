from agents.base_agent import BaseAgent


class ModeratorAgent(BaseAgent):

    def __init__(self):
        super().__init__("Moderator")

    def run(self, state):
        print(f"{self.name} is planning the debate...")

        return state