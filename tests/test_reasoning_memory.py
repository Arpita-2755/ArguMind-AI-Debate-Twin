from datetime import datetime

from schemas.reasoning_memory import (
    MemoryStatus,
    MemoryType,
    ReasoningMemory,
)


def test_valid_reasoning_memory():
    memory = ReasoningMemory(
        id="memory_001",
        user_id="user_001",
        memory_type=MemoryType.REASONING_PATTERN,
        content="Frequently structures arguments around cause and consequence.",
        confidence=0.82,
        source_debate_id="debate_001",
        source_debate_count=3,
        topics=["AI", "technology"],
        status=MemoryStatus.ACTIVE,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    assert memory.id == "memory_001"
    assert memory.user_id == "user_001"
    assert memory.memory_type == MemoryType.REASONING_PATTERN
    assert memory.confidence == 0.82
    assert memory.source_debate_count == 3
    assert memory.status == MemoryStatus.ACTIVE


def test_default_values():
    memory = ReasoningMemory(
        id="memory_002",
        user_id="user_001",
        memory_type=MemoryType.STRENGTH,
        content="Uses structured reasoning.",
        confidence=0.75,
        source_debate_id="debate_002",
        source_debate_count=1,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    assert memory.topics == []
    assert memory.status == MemoryStatus.ACTIVE


def test_invalid_confidence():
    try:
        ReasoningMemory(
            id="memory_003",
            user_id="user_001",
            memory_type=MemoryType.WEAKNESS,
            content="Weak empirical grounding.",
            confidence=1.5,
            source_debate_id="debate_003",
            source_debate_count=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        assert False, "Expected validation error"

    except ValueError:
        pass


def test_invalid_debate_count():
    try:
        ReasoningMemory(
            id="memory_004",
            user_id="user_001",
            memory_type=MemoryType.ASSUMPTION,
            content="Assumes technology adoption is inevitable.",
            confidence=0.6,
            source_debate_id="debate_004",
            source_debate_count=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        assert False, "Expected validation error"

    except ValueError:
        pass


def test_memory_status():
    memory = ReasoningMemory(
        id="memory_005",
        user_id="user_001",
        memory_type=MemoryType.EVIDENCE_HABIT,
        content="Prefers conceptual evidence.",
        confidence=0.7,
        source_debate_id="debate_005",
        source_debate_count=2,
        status=MemoryStatus.DEPRECATED,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    assert memory.status == MemoryStatus.DEPRECATED


if __name__ == "__main__":
    test_valid_reasoning_memory()
    test_default_values()
    test_invalid_confidence()
    test_invalid_debate_count()
    test_memory_status()

    print("All Reasoning Memory schema tests passed!")