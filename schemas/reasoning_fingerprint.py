from pydantic import BaseModel
from typing import List


class ReasoningFingerprint(BaseModel):

    reasoning_style: List[str]

    strongest_reasoning_patterns: List[str]

    weakest_reasoning_patterns: List[str]

    evidence_style: str

    argument_style: List[str]

    common_assumptions: List[str]

    fallacy_tendencies: List[str]

    reasoning_strengths: List[str]

    reasoning_weaknesses: List[str]

    overall_reasoning_score: float

    profile_summary: str