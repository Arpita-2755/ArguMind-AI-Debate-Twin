import json

from sqlalchemy import select

from db.database import SessionLocal
from db.models.reasoning_memory import ReasoningMemoryModel
from schemas.reasoning_memory import (
    MemoryStatus,
    MemoryType,
    ReasoningMemory,
)


class ReasoningMemoryRepository:

    @staticmethod
    def _to_schema(
        model: ReasoningMemoryModel,
    ) -> ReasoningMemory:

        return ReasoningMemory(
            id=model.id,
            user_id=model.user_id,
            memory_type=MemoryType(model.memory_type),
            content=model.content,
            confidence=model.confidence,
            source_debate_id=model.source_debate_id,
            source_debate_count=model.source_debate_count,
            topics=json.loads(model.topics),
            status=MemoryStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_model(
        memory: ReasoningMemory,
    ) -> ReasoningMemoryModel:

        return ReasoningMemoryModel(
            id=memory.id,
            user_id=memory.user_id,
            memory_type=memory.memory_type.value,
            content=memory.content,
            confidence=memory.confidence,
            source_debate_id=memory.source_debate_id,
            source_debate_count=memory.source_debate_count,
            topics=json.dumps(memory.topics),
            status=memory.status.value,
            created_at=memory.created_at,
            updated_at=memory.updated_at,
        )

    @classmethod
    def create(
        cls,
        memory: ReasoningMemory,
    ) -> ReasoningMemory:

        with SessionLocal() as session:

            model = cls._to_model(memory)

            session.add(model)
            session.commit()
            session.refresh(model)

            return cls._to_schema(model)

    @classmethod
    def get_by_id(
        cls,
        memory_id: str,
    ) -> ReasoningMemory | None:

        with SessionLocal() as session:

            statement = select(
                ReasoningMemoryModel
            ).where(
                ReasoningMemoryModel.id == memory_id
            )

            model = session.scalar(statement)

            if model is None:
                return None

            return cls._to_schema(model)

    @classmethod
    def get_by_user(
        cls,
        user_id: str,
    ) -> list[ReasoningMemory]:

        with SessionLocal() as session:

            statement = select(
                ReasoningMemoryModel
            ).where(
                ReasoningMemoryModel.user_id == user_id
            )

            models = session.scalars(statement).all()

            return [
                cls._to_schema(model)
                for model in models
            ]

    @classmethod
    def get_active_by_user(
        cls,
        user_id: str,
    ) -> list[ReasoningMemory]:

        with SessionLocal() as session:

            statement = select(
                ReasoningMemoryModel
            ).where(
                ReasoningMemoryModel.user_id == user_id,
                ReasoningMemoryModel.status == MemoryStatus.ACTIVE.value,
            )

            models = session.scalars(statement).all()

            return [
                cls._to_schema(model)
                for model in models
            ]
    @classmethod
    def update(
        cls,
        memory: ReasoningMemory,
    ) -> ReasoningMemory | None:

        with SessionLocal() as session:

            model = session.get(
                ReasoningMemoryModel,
                memory.id,
            )

            if model is None:
                return None

            model.user_id = memory.user_id
            model.memory_type = memory.memory_type.value
            model.content = memory.content
            model.confidence = memory.confidence
            model.source_debate_id = memory.source_debate_id
            model.source_debate_count = memory.source_debate_count
            model.topics = json.dumps(memory.topics)
            model.status = memory.status.value
            model.created_at = memory.created_at
            model.updated_at = memory.updated_at

            session.commit()
            session.refresh(model)

            return cls._to_schema(model)