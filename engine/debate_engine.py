class DebateEngine:

    TOTAL_ROUNDS = 3

    @staticmethod
    def next_round(state):

        state.current_round += 1

        return state

    @staticmethod
    def debate_finished(state):

        return state.current_round > DebateEngine.TOTAL_ROUNDS