from datetime import datetime

from schemas.reasoning_memory import (
    MemoryStatus,
    MemoryType,
    ReasoningMemory,
)
from services.memory_consolidation_service import (
    MemoryConsolidationService,
)


def create_memory(
    content: str,
    confidence: float = 0.7,
    debate_count: int = 1,
    topics: list[str] | None = None,
    user_id: str = "user_001",
    memory_type: MemoryType = MemoryType.REASONING_PATTERN,
):

    now = datetime.now()

    return ReasoningMemory(
        id="memory_001",
        user_id=user_id,
        memory_type=memory_type,
        content=content,
        confidence=confidence,
        source_debate_id="debate_001",
        source_debate_count=debate_count,
        topics=topics or [],
        status=MemoryStatus.ACTIVE,
        created_at=now,
        updated_at=now,
    )


def test_new_memory_is_created_when_no_match_exists():

    new_memory = create_memory(
        "Uses causal reasoning."
    )

    result = MemoryConsolidationService.consolidate(
        new_memory,
        [],
    )

    assert result is new_memory


def test_matching_memory_is_consolidated():

    existing_memory = create_memory(
        "Uses causal reasoning.",
        confidence=0.7,
        debate_count=1,
    )

    new_memory = create_memory(
        "uses   causal   reasoning.",
        confidence=0.8,
        debate_count=1,
    )

    result = MemoryConsolidationService.consolidate(
        new_memory,
        [existing_memory],
    )

    assert result is existing_memory
    assert result.source_debate_count == 2
    assert result.confidence == 0.78


def test_topics_are_merged():

    existing_memory = create_memory(
        "Uses causal reasoning.",
        topics=["AI"],
    )

    new_memory = create_memory(
        "Uses causal reasoning.",
        topics=["technology"],
    )

    result = MemoryConsolidationService.consolidate(
        new_memory,
        [existing_memory],
    )

    assert set(result.topics) == {
        "AI",
        "technology",
    }


def test_different_users_do_not_match():

    existing_memory = create_memory(
        "Uses causal reasoning.",
        user_id="user_001",
    )

    new_memory = create_memory(
        "Uses causal reasoning.",
        user_id="user_002",
    )

    result = MemoryConsolidationService.consolidate(
        new_memory,
        [existing_memory],
    )

    assert result is new_memory


def test_different_memory_types_do_not_match():

    existing_memory = create_memory(
        "Uses causal reasoning.",
        memory_type=MemoryType.STRENGTH,
    )

    new_memory = create_memory(
        "Uses causal reasoning.",
        memory_type=MemoryType.WEAKNESS,
    )

    result = MemoryConsolidationService.consolidate(
        new_memory,
        [existing_memory],
    )

    assert result is new_memory


def test_deprecated_memory_does_not_match():

    existing_memory = create_memory(
        "Uses causal reasoning.",
    )

    existing_memory.status = MemoryStatus.DEPRECATED

    new_memory = create_memory(
        "Uses causal reasoning.",
    )

    result = MemoryConsolidationService.consolidate(
        new_memory,
        [existing_memory],
    )

    assert result is new_memory


if __name__ == "__main__":
    test_new_memory_is_created_when_no_match_exists()
    test_matching_memory_is_consolidated()
    test_topics_are_merged()
    test_different_users_do_not_match()
    test_different_memory_types_do_not_match()
    test_deprecated_memory_does_not_match()

    print("All Memory Consolidation Service tests passed!")