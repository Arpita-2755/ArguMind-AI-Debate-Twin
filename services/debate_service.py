from schemas.debate_turn import DebateTurn


class DebateService:

    @staticmethod
    def add_turn(
        state,
        user_argument,
        opponent_argument
    ):

        turn = DebateTurn(

            round_number=state.current_round,

            phase=state.current_phase.value,

            user_argument=user_argument,

            opponent_argument=opponent_argument

        )

        state.debate_history.append(turn)

        return state