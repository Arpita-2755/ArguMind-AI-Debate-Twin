from pydantic import BaseModel
from typing import List


class ReflectionResult(BaseModel):
    reasoning_patterns: List[str]
    strengths: List[str]
    weaknesses: List[str]
    assumptions: List[str]
    fallacies: List[str]
    evidence_usage: str
    overall_reasoning_quality: float
    summary: str