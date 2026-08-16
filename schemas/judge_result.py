from pydantic import BaseModel


class JudgeResult(BaseModel):

    winner: str

    logic_score: float

    evidence_score: float

    clarity_score: float

    persuasion_score: float

    strengths: list[str]

    weaknesses: list[str]

    summary: str