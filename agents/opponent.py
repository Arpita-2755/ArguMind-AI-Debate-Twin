from agents.base_agent import BaseAgent
from services.opponent_service import OpponentService
from services.debate_service import DebateService


class OpponentAgent(BaseAgent):

    def __init__(self):
        super().__init__("Opponent")

    def run(self, state):

        print("\n========== OPPONENT ==========\n")

        argument = OpponentService.generate_opening(
            state.debate_plan,
            state.user_stance
        )

        print(argument)

        state = DebateService.complete_turn(
            state,
            argument
        )

        return state