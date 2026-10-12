from uuid import uuid4

from agents.memory_agent import MemoryAgent
from db.repositories.reasoning_memory_repository import (
    ReasoningMemoryRepository,
)
from graph.enums import DebatePhase
from graph.state import DebateState
from schemas.reasoning_memory import (
    MemoryType,
    ReasoningMemory,
)


def create_memory(
    user_id: str,
    memory_type: MemoryType,
    content: str,
    topics: list[str],
    confidence: float = 0.8,
):

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


def test_memory_agent():

    user_id = f"memory-agent-test-{uuid4()}"

    memory = create_memory(
        user_id=user_id,
        memory_type=MemoryType.REASONING_PATTERN,
        content="Frequently demonstrates causal reasoning.",
        topics=["AI"],
    )

    ReasoningMemoryRepository.create(memory)

    state = DebateState(
        topic="Should AI replace software engineers?",
        user_stance="Support",
        ai_stance="Oppose",
        current_phase=DebatePhase.OPENING,
    )

    state.metadata["user_id"] = user_id

    agent = MemoryAgent()

    updated_state = agent.run(state)

    assert "memory_context" in updated_state.metadata

    context = updated_state.metadata["memory_context"]

    assert "USER REASONING CONTEXT" in context

    assert "Known reasoning patterns:" in context

    assert (
        "Frequently demonstrates causal reasoning."
        in context
    )


if __name__ == "__main__":

    test_memory_agent()

    print("Memory agent test passed!")