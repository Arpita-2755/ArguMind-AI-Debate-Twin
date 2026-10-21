from datetime import datetime
from uuid import uuid4

from schemas.reasoning_fingerprint import ReasoningFingerprint
from schemas.reasoning_memory import (
    MemoryType,
    ReasoningMemory,
)


class ReasoningMemoryService:

    @staticmethod
    def _clean_content(text: str) -> str:
        """
        Store the analyzer's own wording. It is often a full
        sentence, so wrapping it in a template ("Shows weakness
        in ...") produced broken text. The memory type already
        says what kind of observation it is.
        """

        text = " ".join(text.split())

        return text[:1].upper() + text[1:]

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

        # (fingerprint items, memory type, starting confidence)
        sources = [
            (fingerprint.strongest_reasoning_patterns, MemoryType.REASONING_PATTERN, 0.7),
            (fingerprint.weakest_reasoning_patterns, MemoryType.WEAKNESS, 0.7),
            ([fingerprint.evidence_style], MemoryType.EVIDENCE_HABIT, 0.65),
            (fingerprint.common_assumptions, MemoryType.ASSUMPTION, 0.6),
            (fingerprint.fallacy_tendencies, MemoryType.FALLACY_TENDENCY, 0.6),
            (fingerprint.reasoning_strengths, MemoryType.STRENGTH, 0.7),
            (fingerprint.reasoning_weaknesses, MemoryType.WEAKNESS, 0.7),
        ]

        memories = []

        for items, memory_type, confidence in sources:

            for item in items:

                content = cls._clean_content(item or "")

                if not content:
                    continue

                memories.append(
                    cls._create_memory(
                        user_id=user_id,
                        memory_type=memory_type,
                        content=content,
                        source_debate_id=source_debate_id,
                        confidence=confidence,
                        topics=topics,
                    )
                )

        return memories
