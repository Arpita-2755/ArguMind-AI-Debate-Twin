from dataclasses import dataclass, field
from typing import List


@dataclass
class DebateRule:
    title: str
    description: str


@dataclass
class DebatePlan:
    topic: str
    user_position: str
    ai_position: str
    strategy: str
    rounds: int
    opening_speaker: str
    rules: List[DebateRule] = field(default_factory=list)