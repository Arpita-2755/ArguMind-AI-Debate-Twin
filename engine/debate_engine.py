from schemas.debate_turn import DebateTurn


class DebateEngine:

    TOTAL_ROUNDS = 3

    @staticmethod
    def next_round(state):

        state.current_round += 1

        return state

    @staticmethod
    def debate_finished(state):

        return state.current_round > DebateEngine.TOTAL_ROUNDS

    @staticmethod
    def add_user_argument(state, argument):

        turn = DebateTurn(
            round_number=state.current_round,
            phase=state.current_phase.value,
            user_argument=argument,
            opponent_argument=""
        )

        state.debate_history.append(turn)

        return state