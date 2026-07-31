from graph.enums import DebatePhase


class Orchestrator:

    def __init__(self):
        self.name = "ArguMind Orchestrator"

    def next_step(self, state):

        phase = state.current_phase

        if phase == DebatePhase.OPENING:
            return "moderator"

        elif phase == DebatePhase.REBUTTAL:
            return "opponent"

        elif phase == DebatePhase.REFLECTION:
            return "reflection"

        return None