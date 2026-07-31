from enum import Enum


class DebatePhase(str, Enum):

    INITIALIZATION = "initialization"

    OPENING = "opening"

    REBUTTAL = "rebuttal"

    CROSS_EXAMINATION = "cross_examination"

    CLOSING = "closing"

    JUDGING = "judging"

    COGNITIVE_ANALYSIS = "cognitive_analysis"

    REFLECTION = "reflection"

    FINISHED = "finished"