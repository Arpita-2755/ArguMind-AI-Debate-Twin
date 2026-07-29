from enum import Enum


class DebatePhase(str, Enum):
    OPENING = "opening"

    REBUTTAL = "rebuttal"

    CROSS_EXAMINATION = "cross_examination"

    CLOSING = "closing"

    REFLECTION = "reflection"

    FINISHED = "finished"