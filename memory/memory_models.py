from dataclasses import dataclass, field
from typing import List


@dataclass
class DebateSession:

    topic: str

    user_stance: str

    ai_stance: str

    winner: str

    logic_score: float

    evidence_score: float

    clarity_score: float

    persuasion_score: float

    strengths: List[str] = field(default_factory=list)

    weaknesses: List[str] = field(default_factory=list)

    fallacies: List[str] = field(default_factory=list)

    summary: str = ""

@dataclass
class UserDebateProfile:

    favorite_topics: List[str] = field(default_factory=list)

    favorite_personas: List[str] = field(default_factory=list)

    strengths: List[str] = field(default_factory=list)

    weaknesses: List[str] = field(default_factory=list)

    common_fallacies: List[str] = field(default_factory=list)

    average_logic_score: float = 0.0

    average_evidence_score: float = 0.0

    total_debates: int = 0