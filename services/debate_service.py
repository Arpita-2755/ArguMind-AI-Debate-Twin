from schemas.debate_turn import DebateTurn


class DebateService:

    @staticmethod
    def start_turn(state, user_argument):

        turn = DebateTurn(
            round_number=state.current_round,
            phase=state.current_phase.value,
            user_argument=user_argument,
            opponent_argument=""
        )

        state.debate_history.append(turn)

        return state

    @staticmethod
    def complete_turn(state, opponent_argument):

        state.debate_history[-1].opponent_argument = opponent_argument

        return state