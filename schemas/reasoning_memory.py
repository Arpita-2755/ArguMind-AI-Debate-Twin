from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class MemoryType(str, Enum):
    STRENGTH = "strength"
    WEAKNESS = "weakness"
    REASONING_PATTERN = "reasoning_pattern"
    EVIDENCE_HABIT = "evidence_habit"
    ASSUMPTION = "assumption"
    FALLACY_TENDENCY = "fallacy_tendency"
    PREFERENCE = "preference"


class MemoryStatus(str, Enum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"


class ReasoningMemory(BaseModel):
    id: str
    user_id: str

    memory_type: MemoryType
    content: str

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )

    source_debate_id: str
    source_debate_count: int = Field(
        ge=1
    )

    topics: List[str] = Field(
        default_factory=list
    )

    status: MemoryStatus = MemoryStatus.ACTIVE

    created_at: datetime
    updated_at: datetime