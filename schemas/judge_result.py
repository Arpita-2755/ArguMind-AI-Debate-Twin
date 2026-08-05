from pydantic import BaseModel


class JudgeResult(BaseModel):

    winner: str

    summary: str

    strengths: list[str]

    weaknesses: list[str]