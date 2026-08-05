from pydantic import BaseModel


class ReflectionReport(BaseModel):

    strengths: list[str]

    improvements: list[str]

    advice: str