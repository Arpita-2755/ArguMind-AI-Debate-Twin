class DebateEngine:

    @staticmethod
    def is_first_round(state):
        return state.current_round == 1

    @staticmethod
    def is_final_round(state):
        return state.current_round >= state.debate_plan.rounds

    @staticmethod
    def next_round(state):
        state.current_round += 1
        return state