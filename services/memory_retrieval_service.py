from schemas.reasoning_memory import (
    MemoryStatus,
    MemoryType,
    ReasoningMemory,
)

from db.repositories.reasoning_memory_repository import (
    ReasoningMemoryRepository,
)


class MemoryRetrievalService:

    @staticmethod
    def get_user_memories(
        user_id: str,
    ) -> list[ReasoningMemory]:

        return ReasoningMemoryRepository.get_by_user(user_id)

    @staticmethod
    def get_active_memories(
        user_id: str,
    ) -> list[ReasoningMemory]:

        return ReasoningMemoryRepository.get_active_by_user(user_id)

    @staticmethod
    def get_memories_by_type(
        user_id: str,
        memory_type: MemoryType,
    ) -> list[ReasoningMemory]:

        memories = (
            ReasoningMemoryRepository.get_active_by_user(user_id)
        )

        return [
            memory
            for memory in memories
            if memory.memory_type == memory_type
        ]

    @staticmethod
    def get_memories_for_topic(
        user_id: str,
        topic: str,
    ) -> list[ReasoningMemory]:

        memories = (
            ReasoningMemoryRepository.get_active_by_user(user_id)
        )

        topic_lower = topic.lower()

        return [
            memory
            for memory in memories
            if any(
                topic_lower in memory_topic.lower()
                or memory_topic.lower() in topic_lower
                for memory_topic in memory.topics
            )
        ]

    @staticmethod
    def get_relevant_memories(
        user_id: str,
        topic: str,
        memory_types: list[MemoryType] | None = None,
        min_confidence: float | None = None,
    ) -> list[ReasoningMemory]:

        memories = (
            ReasoningMemoryRepository.get_active_by_user(user_id)
        )

        topic_lower = topic.lower()

        relevant_memories = []

        for memory in memories:

            if (
                memory_types is not None
                and memory.memory_type not in memory_types
            ):
                continue

            if (
                min_confidence is not None
                and memory.confidence < min_confidence
            ):
                continue

            if not memory.topics:
                continue

            topic_match = any(
                topic_lower in memory_topic.lower()
                or memory_topic.lower() in topic_lower
                for memory_topic in memory.topics
            )

            if topic_match:
                relevant_memories.append(memory)

        return relevant_memories