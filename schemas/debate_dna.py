from dataclasses import dataclass, field
from typing import List


@dataclass
class DebateDNA:

    reasoning_style: str = ""

    evidence_usage: str = ""

    confidence_level: str = ""

    adaptability_score: float = 0.0

    argument_complexity: str = ""

    topic_expertise: dict = field(default_factory=dict)

    common_biases: List[str] = field(default_factory=list)

    strengths: List[str] = field(default_factory=list)

    weaknesses: List[str] = field(default_factory=list)