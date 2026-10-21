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

        # Filled once by the memory graph before the debate starts.
        memory_context = state.metadata.get("memory_context")

        argument = OpponentService.generate_response(
            state.debate_plan,
            current_turn.user_argument,
            previous_history,
            memory_context
        )

        state = DebateService.complete_turn(
            state,
            argument
        )

        return state