from agents.base_agent import BaseAgent
from services.opponent_service import OpponentService
from services.debate_service import DebateService


class OpponentAgent(BaseAgent):

    def __init__(self):
        super().__init__("Opponent")

    def run(self, state):

        current_turn = state.debate_history[-1]

        # Previous turns only.
        previous_history = state.debate_history[:-1]

        argument = OpponentService.generate_response(
            state.debate_plan,
            current_turn.user_argument,
            previous_history
        )

        state = DebateService.complete_turn(
            state,
            argument
        )

        return state