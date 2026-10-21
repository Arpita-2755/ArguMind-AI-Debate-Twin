from uuid import uuid4

from agents.base_agent import BaseAgent
from services.persistent_memory_service import PersistentMemoryService


class MemoryUpdateAgent(BaseAgent):

    def __init__(self):
        super().__init__("Memory Update")

    def run(self, state):

        debate_id = state.metadata.setdefault(
            "debate_id",
            f"debate-{uuid4()}"
        )

        stored_memories = PersistentMemoryService.store_fingerprint(
            fingerprint=state.metadata["reasoning_fingerprint"],
            user_id=state.metadata["user_id"],
            source_debate_id=debate_id,
            topics=[state.topic],
        )

        state.metadata["stored_memory_count"] = len(
            stored_memories
        )

        return state
