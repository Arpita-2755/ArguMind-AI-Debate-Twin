from agents.base_agent import BaseAgent
from services.memory_retrieval_service import MemoryRetrievalService
from services.memory_context_service import MemoryContextService


class MemoryAgent(BaseAgent):

    def __init__(self):
        super().__init__("Memory")

    def run(self, state):

        memories = MemoryRetrievalService.get_relevant_memories(
            user_id=state.metadata["user_id"],
            topic=state.topic,
        )

        context = MemoryContextService.build_context(
            memories
        )

        state.metadata["memory_context"] = context

        return state