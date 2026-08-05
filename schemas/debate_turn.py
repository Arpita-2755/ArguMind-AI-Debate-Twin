from pydantic import BaseModel


class DebateTurn(BaseModel):

    round_number: int

    phase: str

    user_argument: str = ""

    opponent_argument: str = ""