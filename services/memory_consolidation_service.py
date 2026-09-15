from datetime import datetime

from schemas.reasoning_memory import ReasoningMemory


class MemoryConsolidationService:

    @staticmethod
    def _normalize_content(content: str) -> str:
        return " ".join(content.lower().split())

    @classmethod
    def find_matching_memory(
        cls,
        new_memory: ReasoningMemory,
        existing_memories: list[ReasoningMemory],
    ) -> ReasoningMemory | None:

        normalized_new = cls._normalize_content(new_memory.content)

        for memory in existing_memories:
            if memory.user_id != new_memory.user_id:
                continue

            if memory.memory_type != new_memory.memory_type:
                continue

            if memory.status.value != "active":
                continue

            normalized_existing = cls._normalize_content(memory.content)

            if normalized_existing == normalized_new:
                return memory

        return None

    @classmethod
    def consolidate(
        cls,
        new_memory: ReasoningMemory,
        existing_memories: list[ReasoningMemory],
    ) -> ReasoningMemory:

        matching_memory = cls.find_matching_memory(
            new_memory,
            existing_memories,
        )

        if matching_memory is None:
            return new_memory

        matching_memory.source_debate_count += (
            new_memory.source_debate_count
        )

        matching_memory.confidence = min(
            1.0,
            matching_memory.confidence
            + (new_memory.confidence * 0.1),
        )

        existing_topics = set(matching_memory.topics)
        new_topics = set(new_memory.topics)

        matching_memory.topics = list(
            existing_topics | new_topics
        )

        matching_memory.updated_at = datetime.now()

        return matching_memory