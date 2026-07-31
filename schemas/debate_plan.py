from pydantic import BaseModel, Field


class DebatePlan(BaseModel):

    topic: str

    category: str

    difficulty: str

    strategy: str

    ai_position: str

    rounds: int = Field(default=5)

    opening_speaker: str = Field(default="User")