from services.memory_consolidation_service import (
    MemoryConsolidationService,
)
from services.reasoning_memory_service import (
    ReasoningMemoryService,
)
from db.repositories.reasoning_memory_repository import (
    ReasoningMemoryRepository,
)
from schemas.reasoning_fingerprint import ReasoningFingerprint
from schemas.reasoning_memory import ReasoningMemory


class PersistentMemoryService:

    @classmethod
    def store_fingerprint(
        cls,
        fingerprint: ReasoningFingerprint,
        user_id: str,
        source_debate_id: str,
        topics: list[str] | None = None,
    ) -> list[ReasoningMemory]:

        new_memories = (
            ReasoningMemoryService.from_fingerprint(
                fingerprint=fingerprint,
                user_id=user_id,
                source_debate_id=source_debate_id,
                topics=topics,
            )
        )

        existing_memories = (
            ReasoningMemoryRepository.get_active_by_user(
                user_id
            )
        )

        persisted_memories = []

        for new_memory in new_memories:

            consolidated = (
                MemoryConsolidationService.consolidate(
                    new_memory=new_memory,
                    existing_memories=existing_memories,
                )
            )

            if consolidated.id == new_memory.id:
                persisted = (
                    ReasoningMemoryRepository.create(
                        consolidated
                    )
                )

                existing_memories.append(persisted)

            else:
                persisted = (
                    ReasoningMemoryRepository.update(
                        consolidated
                    )
                )

            if persisted is not None:
                persisted_memories.append(persisted)

        return persisted_memories