from uuid import uuid4

from services.persistent_memory_service import (
    PersistentMemoryService,
)
from schemas.reasoning_fingerprint import ReasoningFingerprint
from db.repositories.reasoning_memory_repository import (
    ReasoningMemoryRepository,
)


def create_fingerprint() -> ReasoningFingerprint:

    return ReasoningFingerprint(
        reasoning_style=["Analytical"],
        strongest_reasoning_patterns=[
            "Causal reasoning"
        ],
        weakest_reasoning_patterns=[
            "Empirical reasoning"
        ],
        evidence_style=(
            "Relies primarily on conceptual evidence."
        ),
        argument_style=["Structured"],
        common_assumptions=[],
        fallacy_tendencies=[],
        reasoning_strengths=[
            "Logical structure"
        ],
        reasoning_weaknesses=[
            "Limited empirical grounding"
        ],
        overall_reasoning_score=8.5,
        profile_summary=(
            "Analytical thinker with strong "
            "logical structure."
        ),
    )


def test_persistent_memory():

    user_id = f"persistent-memory-test-user-{uuid4()}"

    fingerprint = create_fingerprint()

    first_memories = (
        PersistentMemoryService.store_fingerprint(
            fingerprint=fingerprint,
            user_id=user_id,
            source_debate_id="debate-1",
            topics=["AI"],
        )
    )

    assert len(first_memories) > 0

    stored_after_first = (
        ReasoningMemoryRepository.get_by_user(
            user_id
        )
    )

    assert len(stored_after_first) == len(
        first_memories
    )

    first_pattern = next(
        memory
        for memory in stored_after_first
        if memory.content
        == "Frequently demonstrates causal reasoning."
    )

    assert first_pattern.source_debate_count == 1

    second_memories = (
        PersistentMemoryService.store_fingerprint(
            fingerprint=fingerprint,
            user_id=user_id,
            source_debate_id="debate-2",
            topics=["Technology"],
        )
    )

    assert len(second_memories) == len(
        first_memories
    )

    stored_after_second = (
        ReasoningMemoryRepository.get_by_user(
            user_id
        )
    )

    # No duplicate memories should be created.
    assert len(stored_after_second) == len(
        stored_after_first
    )

    updated_pattern = next(
        memory
        for memory in stored_after_second
        if memory.content
        == "Frequently demonstrates causal reasoning."
    )

    assert updated_pattern.source_debate_count == 2

    assert "AI" in updated_pattern.topics
    assert "Technology" in updated_pattern.topics

def test_different_memories_remain_separate():

    user_id = f"memory-isolation-test-user-{uuid4()}"

    fingerprint = create_fingerprint()

    PersistentMemoryService.store_fingerprint(
        fingerprint=fingerprint,
        user_id=user_id,
        source_debate_id="debate-1",
        topics=["AI"],
    )

    stored = (
        ReasoningMemoryRepository.get_by_user(
            user_id
        )
    )

    contents = {
        memory.content
        for memory in stored
    }

    # These are intentionally different memories
    # generated from different fingerprint fields.
    assert (
        "Frequently demonstrates causal reasoning."
        in contents
    )

    assert (
        "Shows weakness in empirical reasoning."
        in contents
    )

    assert (
        "Logical structure"
        in contents
    )

if __name__ == "__main__":

    test_persistent_memory()
    test_different_memories_remain_separate()

    print(
        "Persistent memory test passed!"
    )