from agents.base_agent import BaseAgent
from services.opponent_service import OpponentService


class OpponentAgent(BaseAgent):

    def __init__(self):
        super().__init__("Opponent")

    def run(self, state):

        print("\n========== OPPONENT ==========\n")

        argument = OpponentService.generate_opening(
            state.plan,
            state.user_stance
        )

        print(argument)

        state.metadata["opening_argument"] = argument

        return state