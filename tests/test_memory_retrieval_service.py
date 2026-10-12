from uuid import uuid4

from db.repositories.reasoning_memory_repository import (
    ReasoningMemoryRepository,
)
from schemas.reasoning_memory import (
    MemoryType,
    ReasoningMemory,
)
from services.memory_retrieval_service import (
    MemoryRetrievalService,
)
from schemas.reasoning_memory import (
    MemoryStatus,
    MemoryType,
    ReasoningMemory,
)

def create_memory(
    user_id: str,
    memory_type: MemoryType,
    content: str,
    topics: list[str],
    confidence: float = 0.8,
) -> ReasoningMemory:

    from datetime import datetime

    now = datetime.now()

    return ReasoningMemory(
        id=str(uuid4()),
        user_id=user_id,
        memory_type=memory_type,
        content=content,
        confidence=confidence,
        source_debate_id=f"debate-{uuid4()}",
        source_debate_count=1,
        topics=topics,
        created_at=now,
        updated_at=now,
    )


def setup_memories(user_id: str):

    memories = [
        create_memory(
            user_id,
            MemoryType.REASONING_PATTERN,
            "Frequently demonstrates causal reasoning.",
            ["AI", "Technology"],
            0.9,
        ),
        create_memory(
            user_id,
            MemoryType.WEAKNESS,
            "Shows weakness in empirical reasoning.",
            ["AI"],
            0.7,
        ),
        create_memory(
            user_id,
            MemoryType.STRENGTH,
            "Demonstrates strong logical structure.",
            ["Technology"],
            0.85,
        ),
    ]

    for memory in memories:
        ReasoningMemoryRepository.create(memory)

    return memories


def test_get_user_memories():

    user_id = f"retrieval-test-{uuid4()}"

    expected = setup_memories(user_id)

    memories = MemoryRetrievalService.get_user_memories(user_id)

    assert len(memories) == len(expected)


def test_get_active_memories():

    user_id = f"active-test-{uuid4()}"

    setup_memories(user_id)

    memories = MemoryRetrievalService.get_active_memories(user_id)

    assert len(memories) == 3
    assert all(
        memory.status.value == "active"
        for memory in memories
    )


def test_get_memories_by_type():

    user_id = f"type-test-{uuid4()}"

    setup_memories(user_id)

    memories = MemoryRetrievalService.get_memories_by_type(
        user_id=user_id,
        memory_type=MemoryType.WEAKNESS,
    )

    assert len(memories) == 1
    assert memories[0].memory_type == MemoryType.WEAKNESS


def test_get_memories_for_topic():

    user_id = f"topic-test-{uuid4()}"

    setup_memories(user_id)

    memories = MemoryRetrievalService.get_memories_for_topic(
        user_id=user_id,
        topic="AI",
    )

    assert len(memories) == 2

    contents = {
        memory.content
        for memory in memories
    }

    assert "Frequently demonstrates causal reasoning." in contents
    assert "Shows weakness in empirical reasoning." in contents


def test_get_relevant_memories():

    user_id = f"relevant-test-{uuid4()}"

    setup_memories(user_id)

    memories = MemoryRetrievalService.get_relevant_memories(
        user_id=user_id,
        topic="AI",
    )

    assert len(memories) == 2


def test_relevant_memories_with_type_filter():

    user_id = f"type-filter-test-{uuid4()}"

    setup_memories(user_id)

    memories = MemoryRetrievalService.get_relevant_memories(
        user_id=user_id,
        topic="AI",
        memory_types=[MemoryType.WEAKNESS],
    )

    assert len(memories) == 1
    assert memories[0].memory_type == MemoryType.WEAKNESS


def test_relevant_memories_with_confidence_filter():

    user_id = f"confidence-test-{uuid4()}"

    setup_memories(user_id)

    memories = MemoryRetrievalService.get_relevant_memories(
        user_id=user_id,
        topic="AI",
        min_confidence=0.8,
    )

    assert len(memories) == 1
    assert memories[0].confidence >= 0.8

def test_deprecated_memories_are_not_retrieved():

    user_id = f"deprecated-test-{uuid4()}"

    active_memory = create_memory(
        user_id,
        MemoryType.REASONING_PATTERN,
        "Frequently demonstrates causal reasoning.",
        ["AI"],
    )

    deprecated_memory = create_memory(
        user_id,
        MemoryType.WEAKNESS,
        "Old reasoning weakness.",
        ["AI"],
    )

    deprecated_memory.status = MemoryStatus.DEPRECATED

    ReasoningMemoryRepository.create(active_memory)
    ReasoningMemoryRepository.create(deprecated_memory)

    active_memories = MemoryRetrievalService.get_active_memories(
        user_id
    )

    assert len(active_memories) == 1
    assert active_memories[0].content == (
        "Frequently demonstrates causal reasoning."
    )

    relevant_memories = (
        MemoryRetrievalService.get_relevant_memories(
            user_id=user_id,
            topic="AI",
        )
    )

    assert len(relevant_memories) == 1
    assert relevant_memories[0].content == (
        "Frequently demonstrates causal reasoning."
    )

if __name__ == "__main__":

    test_get_user_memories()
    test_get_active_memories()
    test_get_memories_by_type()
    test_get_memories_for_topic()
    test_get_relevant_memories()
    test_relevant_memories_with_type_filter()
    test_relevant_memories_with_confidence_filter()
    test_deprecated_memories_are_not_retrieved()

    print("Memory retrieval service tests passed!")