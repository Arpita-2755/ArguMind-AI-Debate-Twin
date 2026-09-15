from datetime import datetime
from uuid import uuid4

from db.repositories.reasoning_memory_repository import (
    ReasoningMemoryRepository,
)
from schemas.reasoning_memory import (
    MemoryStatus,
    MemoryType,
    ReasoningMemory,
)


def create_test_memory(
    user_id: str,
) -> ReasoningMemory:

    now = datetime.now()

    return ReasoningMemory(
        id=str(uuid4()),
        user_id=user_id,
        memory_type=MemoryType.REASONING_PATTERN,
        content="Frequently tests assumptions before reaching conclusions.",
        confidence=0.85,
        source_debate_id=str(uuid4()),
        source_debate_count=1,
        topics=["AI", "technology"],
        status=MemoryStatus.ACTIVE,
        created_at=now,
        updated_at=now,
    )


def test_create_and_read():

    user_id = f"test-user-{uuid4()}"

    memory = create_test_memory(user_id)

    created = ReasoningMemoryRepository.create(memory)

    assert created.id == memory.id
    assert created.user_id == user_id
    assert created.content == memory.content
    assert created.confidence == memory.confidence
    assert created.topics == memory.topics


def test_get_by_id():

    user_id = f"test-user-{uuid4()}"

    memory = create_test_memory(user_id)

    ReasoningMemoryRepository.create(memory)

    retrieved = ReasoningMemoryRepository.get_by_id(
        memory.id
    )

    assert retrieved is not None
    assert retrieved.id == memory.id
    assert retrieved.user_id == user_id


def test_get_by_user():

    user_id = f"test-user-{uuid4()}"

    memory1 = create_test_memory(user_id)
    memory2 = create_test_memory(user_id)

    ReasoningMemoryRepository.create(memory1)
    ReasoningMemoryRepository.create(memory2)

    memories = ReasoningMemoryRepository.get_by_user(
        user_id
    )

    assert len(memories) == 2


def test_get_active_by_user():

    user_id = f"test-user-{uuid4()}"

    active_memory = create_test_memory(user_id)

    deprecated_memory = create_test_memory(user_id)
    deprecated_memory.status = MemoryStatus.DEPRECATED

    ReasoningMemoryRepository.create(active_memory)
    ReasoningMemoryRepository.create(deprecated_memory)

    memories = (
        ReasoningMemoryRepository
        .get_active_by_user(user_id)
    )

    assert len(memories) == 1
    assert memories[0].id == active_memory.id


def test_update():

    user_id = f"test-user-{uuid4()}"

    memory = create_test_memory(user_id)

    ReasoningMemoryRepository.create(memory)

    memory.content = (
        "Frequently tests assumptions and "
        "actively challenges counterarguments."
    )

    memory.confidence = 0.95
    memory.source_debate_count = 3
    memory.topics.append("reasoning")

    updated = ReasoningMemoryRepository.update(
        memory
    )

    assert updated is not None
    assert updated.content == memory.content
    assert updated.confidence == 0.95
    assert updated.source_debate_count == 3
    assert "reasoning" in updated.topics

    retrieved = ReasoningMemoryRepository.get_by_id(
        memory.id
    )

    assert retrieved is not None
    assert retrieved.content == memory.content
    assert retrieved.confidence == 0.95

if __name__ == "__main__":

    test_create_and_read()
    test_get_by_id()
    test_get_by_user()
    test_get_active_by_user()

    print(
        "All Reasoning Memory Repository tests passed!"
    )