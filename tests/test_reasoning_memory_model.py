from datetime import datetime

from db.models.reasoning_memory import (
    Base,
    ReasoningMemoryModel,
)


def test_reasoning_memory_model():

    memory = ReasoningMemoryModel(
        id="memory_001",
        user_id="user_001",
        memory_type="reasoning_pattern",
        content="Frequently uses causal reasoning.",
        confidence=0.82,
        source_debate_id="debate_001",
        source_debate_count=3,
        topics='["AI", "technology"]',
        status="active",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    assert memory.id == "memory_001"
    assert memory.user_id == "user_001"
    assert memory.memory_type == "reasoning_pattern"
    assert memory.confidence == 0.82
    assert memory.source_debate_count == 3
    assert memory.status == "active"


def test_table_name():

    assert ReasoningMemoryModel.__tablename__ == "reasoning_memories"


def test_primary_key():

    primary_keys = [
        column.name
        for column in ReasoningMemoryModel.__table__.primary_key.columns
    ]

    assert primary_keys == ["id"]


def test_required_columns():

    columns = ReasoningMemoryModel.__table__.columns

    assert columns["user_id"].nullable is False
    assert columns["content"].nullable is False
    assert columns["confidence"].nullable is False
    assert columns["memory_type"].nullable is False
    assert columns["status"].nullable is False


def test_base_metadata_contains_table():

    assert "reasoning_memories" in Base.metadata.tables


if __name__ == "__main__":
    test_reasoning_memory_model()
    test_table_name()
    test_primary_key()
    test_required_columns()
    test_base_metadata_contains_table()

    print("All Reasoning Memory database model tests passed!")