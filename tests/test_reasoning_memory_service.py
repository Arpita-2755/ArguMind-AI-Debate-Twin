from services.reasoning_memory_service import ReasoningMemoryService
from schemas.reasoning_fingerprint import ReasoningFingerprint
from schemas.reasoning_memory import MemoryType


def create_test_fingerprint():
    return ReasoningFingerprint(
        reasoning_style=[
            "Analytical",
            "Causal",
        ],
        strongest_reasoning_patterns=[
            "Causal reasoning",
            "Assumption testing",
        ],
        weakest_reasoning_patterns=[
            "Empirical reasoning",
        ],
        evidence_style=(
            "Primarily relies on deductive and conceptual evidence."
        ),
        argument_style=[
            "Structured",
            "Counterargument-driven",
        ],
        common_assumptions=[
            "Assumes systemic factors reliably determine outcomes."
        ],
        fallacy_tendencies=[
            "Occasional overgeneralization."
        ],
        reasoning_strengths=[
            "Logical structure",
            "Conceptual clarity",
        ],
        reasoning_weaknesses=[
            "Limited empirical grounding",
        ],
        overall_reasoning_score=8.5,
        profile_summary=(
            "The user is analytical and causal in their reasoning."
        ),
    )


def test_memory_creation():
    fingerprint = create_test_fingerprint()

    memories = ReasoningMemoryService.from_fingerprint(
        fingerprint=fingerprint,
        user_id="user_001",
        source_debate_id="debate_001",
        topics=["AI"],
    )

    assert len(memories) > 0


def test_memory_types():
    fingerprint = create_test_fingerprint()

    memories = ReasoningMemoryService.from_fingerprint(
        fingerprint=fingerprint,
        user_id="user_001",
        source_debate_id="debate_001",
        topics=["AI"],
    )

    memory_types = {memory.memory_type for memory in memories}

    assert MemoryType.REASONING_PATTERN in memory_types
    assert MemoryType.WEAKNESS in memory_types
    assert MemoryType.EVIDENCE_HABIT in memory_types
    assert MemoryType.ASSUMPTION in memory_types
    assert MemoryType.FALLACY_TENDENCY in memory_types
    assert MemoryType.STRENGTH in memory_types


def test_memory_metadata():
    fingerprint = create_test_fingerprint()

    memories = ReasoningMemoryService.from_fingerprint(
        fingerprint=fingerprint,
        user_id="user_001",
        source_debate_id="debate_123",
        topics=["AI", "technology"],
    )

    for memory in memories:
        assert memory.user_id == "user_001"
        assert memory.source_debate_id == "debate_123"
        assert memory.source_debate_count == 1
        assert memory.topics == ["AI", "technology"]
        assert 0.0 <= memory.confidence <= 1.0


def test_memory_content():
    fingerprint = create_test_fingerprint()

    memories = ReasoningMemoryService.from_fingerprint(
        fingerprint=fingerprint,
        user_id="user_001",
        source_debate_id="debate_001",
    )

    contents = [memory.content for memory in memories]

    assert any("causal reasoning" in content.lower() for content in contents)
    assert any(
        "empirical reasoning" in content.lower()
        for content in contents
    )


if __name__ == "__main__":
    test_memory_creation()
    test_memory_types()
    test_memory_metadata()
    test_memory_content()

    print("All Reasoning Memory Service tests passed!")