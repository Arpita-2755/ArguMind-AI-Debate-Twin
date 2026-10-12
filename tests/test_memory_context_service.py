from datetime import datetime
from uuid import uuid4

from schemas.reasoning_memory import (
    MemoryType,
    ReasoningMemory,
)
from services.memory_context_service import (
    MemoryContextService,
)


def create_memory(
    memory_type: MemoryType,
    content: str,
) -> ReasoningMemory:

    now = datetime.now()

    return ReasoningMemory(
        id=str(uuid4()),
        user_id="context-test-user",
        memory_type=memory_type,
        content=content,
        confidence=0.8,
        source_debate_id="debate-test",
        source_debate_count=1,
        topics=["AI"],
        created_at=now,
        updated_at=now,
    )


def test_empty_memories():

    context = MemoryContextService.build_context([])

    assert context == (
        "No prior reasoning memories are available."
    )


def test_memory_grouping():

    memories = [
        create_memory(
            MemoryType.REASONING_PATTERN,
            "Frequently demonstrates causal reasoning.",
        ),
        create_memory(
            MemoryType.STRENGTH,
            "Demonstrates strong logical structure.",
        ),
        create_memory(
            MemoryType.WEAKNESS,
            "Shows weakness in empirical reasoning.",
        ),
    ]

    context = MemoryContextService.build_context(memories)

    assert "USER REASONING CONTEXT" in context

    assert (
        "Known reasoning patterns:" in context
    )

    assert (
        "Frequently demonstrates causal reasoning."
        in context
    )

    assert "Known strengths:" in context

    assert (
        "Demonstrates strong logical structure."
        in context
    )

    assert "Known weaknesses:" in context

    assert (
        "Shows weakness in empirical reasoning."
        in context
    )


def test_all_memory_types():

    memories = [
        create_memory(
            MemoryType.REASONING_PATTERN,
            "Causal reasoning",
        ),
        create_memory(
            MemoryType.STRENGTH,
            "Logical structure",
        ),
        create_memory(
            MemoryType.WEAKNESS,
            "Limited empirical evidence",
        ),
        create_memory(
            MemoryType.EVIDENCE_HABIT,
            "Relies on conceptual evidence",
        ),
        create_memory(
            MemoryType.ASSUMPTION,
            "Assumes technology adoption is rapid",
        ),
        create_memory(
            MemoryType.FALLACY_TENDENCY,
            "Occasional overgeneralization",
        ),
        create_memory(
            MemoryType.PREFERENCE,
            "Prefers technical examples",
        ),
    ]

    context = MemoryContextService.build_context(memories)

    assert "Known reasoning patterns:" in context
    assert "Known strengths:" in context
    assert "Known weaknesses:" in context
    assert "Evidence habits:" in context
    assert "Common assumptions:" in context
    assert "Fallacy tendencies:" in context
    assert "Known preferences:" in context


def test_personalization_guidelines():

    memories = [
        create_memory(
            MemoryType.STRENGTH,
            "Strong logical structure",
        )
    ]

    context = MemoryContextService.build_context(memories)

    assert "PERSONALIZATION GUIDELINES:" in context

    assert (
        "Treat these as tendencies, not absolute facts."
        in context
    )

    assert (
        "Use them only when relevant to the current debate."
        in context
    )

    assert (
        "Do not mention or expose these memories to the user"
        in context
    )

    assert (
        "Do not assume a remembered weakness will appear"
        in context
    )


def test_multiple_memories_same_type():

    memories = [
        create_memory(
            MemoryType.REASONING_PATTERN,
            "Causal reasoning",
        ),
        create_memory(
            MemoryType.REASONING_PATTERN,
            "Assumption testing",
        ),
    ]

    context = MemoryContextService.build_context(memories)

    assert "Causal reasoning" in context
    assert "Assumption testing" in context

    assert context.count("- Causal reasoning") == 1
    assert context.count("- Assumption testing") == 1


if __name__ == "__main__":

    test_empty_memories()
    test_memory_grouping()
    test_all_memory_types()
    test_personalization_guidelines()
    test_multiple_memories_same_type()

    print("Memory context service tests passed!")