from agents.base_agent import BaseAgent
from services.opponent_service import OpponentService
from services.debate_service import DebateService


class OpponentAgent(BaseAgent):

    def __init__(self):
        super().__init__("Opponent")

    def run(self, state):

        print("\n========== OPPONENT ==========\n")

        # Generate AI opening argument
        argument = OpponentService.generate_opening(
            state.debate_plan,
            state.user_stance
        )

        print(argument)

        # Store the debate turn
        state = DebateService.add_turn(
            state=state,
            user_argument="",
            opponent_argument=argument
        )

        return state