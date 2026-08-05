from pydantic import BaseModel

from schemas.debate_plan import DebatePlan
from schemas.debate_turn import DebateTurn


class DebateTranscript(BaseModel):

    topic: str

    debate_plan: DebatePlan

    turns: list[DebateTurn]