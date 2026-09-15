from datetime import datetime
from uuid import uuid4

from schemas.reasoning_fingerprint import ReasoningFingerprint
from schemas.reasoning_memory import (
    MemoryType,
    ReasoningMemory,
)


class ReasoningMemoryService:

    @staticmethod
    def _create_memory(
        user_id: str,
        memory_type: MemoryType,
        content: str,
        source_debate_id: str,
        confidence: float,
        source_debate_count: int = 1,
        topics: list[str] | None = None,
    ) -> ReasoningMemory:

        now = datetime.now()

        return ReasoningMemory(
            id=str(uuid4()),
            user_id=user_id,
            memory_type=memory_type,
            content=content,
            confidence=confidence,
            source_debate_id=source_debate_id,
            source_debate_count=source_debate_count,
            topics=topics or [],
            created_at=now,
            updated_at=now,
        )

    @classmethod
    def from_fingerprint(
        cls,
        fingerprint: ReasoningFingerprint,
        user_id: str,
        source_debate_id: str,
        topics: list[str] | None = None,
    ) -> list[ReasoningMemory]:

        memories = []

        # Strong reasoning patterns
        for pattern in fingerprint.strongest_reasoning_patterns:
            memories.append(
                cls._create_memory(
                    user_id=user_id,
                    memory_type=MemoryType.REASONING_PATTERN,
                    content=f"Frequently demonstrates {pattern.lower()}.",
                    source_debate_id=source_debate_id,
                    confidence=0.7,
                    topics=topics,
                )
            )

        # Weak reasoning patterns
        for pattern in fingerprint.weakest_reasoning_patterns:
            memories.append(
                cls._create_memory(
                    user_id=user_id,
                    memory_type=MemoryType.WEAKNESS,
                    content=f"Shows weakness in {pattern.lower()}.",
                    source_debate_id=source_debate_id,
                    confidence=0.7,
                    topics=topics,
                )
            )

        # Evidence style
        if fingerprint.evidence_style:
            memories.append(
                cls._create_memory(
                    user_id=user_id,
                    memory_type=MemoryType.EVIDENCE_HABIT,
                    content=fingerprint.evidence_style,
                    source_debate_id=source_debate_id,
                    confidence=0.65,
                    topics=topics,
                )
            )

        # Common assumptions
        for assumption in fingerprint.common_assumptions:
            memories.append(
                cls._create_memory(
                    user_id=user_id,
                    memory_type=MemoryType.ASSUMPTION,
                    content=assumption,
                    source_debate_id=source_debate_id,
                    confidence=0.6,
                    topics=topics,
                )
            )

        # Fallacy tendencies
        for fallacy in fingerprint.fallacy_tendencies:
            memories.append(
                cls._create_memory(
                    user_id=user_id,
                    memory_type=MemoryType.FALLACY_TENDENCY,
                    content=fallacy,
                    source_debate_id=source_debate_id,
                    confidence=0.6,
                    topics=topics,
                )
            )

        # Reasoning strengths
        for strength in fingerprint.reasoning_strengths:
            memories.append(
                cls._create_memory(
                    user_id=user_id,
                    memory_type=MemoryType.STRENGTH,
                    content=strength,
                    source_debate_id=source_debate_id,
                    confidence=0.7,
                    topics=topics,
                )
            )

        # Reasoning weaknesses
        for weakness in fingerprint.reasoning_weaknesses:
            memories.append(
                cls._create_memory(
                    user_id=user_id,
                    memory_type=MemoryType.WEAKNESS,
                    content=weakness,
                    source_debate_id=source_debate_id,
                    confidence=0.7,
                    topics=topics,
                )
            )

        return memories