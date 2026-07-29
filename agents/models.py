from dataclasses import dataclass
from typing import List


@dataclass
class DebatePlan:

    topic: str

    user_position: str

    ai_position: str

    strategy: str

    rounds: int

    opening_speaker: str

    rules: List[str]