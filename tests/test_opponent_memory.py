from datetime import datetime
from uuid import uuid4

from db.repositories.reasoning_memory_repository import (
    ReasoningMemoryRepository,
)
from graph.builder import memory_graph, opponent_graph
from graph.enums import DebatePhase
from graph.state import DebateState
from prompts.opponent_prompt import build_opponent_prompt
from schemas.debate_plan import DebatePlan
from schemas.reasoning_memory import MemoryType, ReasoningMemory
from services.debate_service import DebateService
from services.llm_service import LLMService
from services.memory_context_service import MemoryContextService
from services.providers.base import BaseLLMProvider


# ========================================
# Fakes and fixtures (no API calls)
# ========================================

class RecordingProvider(BaseLLMProvider):

    def __init__(self):
        self.prompts = []

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return "Fake opponent reply."

    def generate_structured(self, prompt: str, schema):
        raise NotImplementedError


WEAKNESS = "Rarely supports claims with concrete data or statistics."

MEMORY_HEADING = "WHAT YOU KNOW ABOUT THIS USER FROM PAST DEBATES"


plan = DebatePlan(
    topic="Should AI replace software engineers?",
    category="Technology",
    difficulty="Intermediate",
    strategy="Evidence Driven",
    ai_position="Oppose",
    rounds=3,
    opening_speaker="User"
)


def create_memory(user_id, memory_type, content):

    now = datetime.now()

    return ReasoningMemory(
        id=str(uuid4()),
        user_id=user_id,
        memory_type=memory_type,
        content=content,
        confidence=0.8,
        source_debate_id=f"debate-{uuid4()}",
        source_debate_count=1,
        topics=["AI"],
        created_at=now,
        updated_at=now,
    )


def new_state(user_id):

    state = DebateState(
        topic=plan.topic,
        user_stance="Support",
        ai_stance="Oppose",
        current_phase=DebatePhase.OPENING,
    )

    state.metadata["user_id"] = user_id

    return state


def run_opponent(state, user_argument):

    state.debate_plan = plan

    state = DebateService.start_turn(state, user_argument)

    result = opponent_graph.invoke(state)

    return DebateState(**result)


print("=" * 50)
print("     OPPONENT MEMORY TEST")
print("=" * 50)


# ========================================
# Prompt
# ========================================

print("\n[1/4] Testing prompt with and without memory...")

with_memory = build_opponent_prompt(
    plan,
    "AI writes most code already.",
    [],
    f"USER REASONING CONTEXT\n\nKnown weaknesses:\n- {WEAKNESS}"
)

assert MEMORY_HEADING in with_memory
assert WEAKNESS in with_memory
assert "at most one" in with_memory

for empty in (None, "", MemoryContextService.NO_MEMORY_CONTEXT):

    prompt = build_opponent_prompt(
        plan,
        "AI writes most code already.",
        [],
        empty
    )

    assert MEMORY_HEADING not in prompt

print("✅ Memory section only appears when there are memories")


# ========================================
# Old call signature still works
# ========================================

print("\n[2/4] Testing prompt without memory argument...")

prompt = build_opponent_prompt(plan, "AI writes most code already.")

assert MEMORY_HEADING not in prompt

print("✅ Existing callers are unaffected")


# ========================================
# Debate 1 teaches, debate 2 uses it
# ========================================

print("\n[3/4] Testing stored memory reaches the Opponent...")

provider = RecordingProvider()

LLMService.set_provider(provider)

user_id = f"opponent-memory-test-{uuid4()}"

ReasoningMemoryRepository.create(
    create_memory(user_id, MemoryType.WEAKNESS, WEAKNESS)
)

state = new_state(user_id)

state = DebateState(**memory_graph.invoke(state))

assert WEAKNESS in state.metadata["memory_context"]

state = run_opponent(state, "AI will write most code within a decade.")

assert state.debate_history[-1].opponent_argument == "Fake opponent reply."

opponent_prompt = provider.prompts[-1]

assert MEMORY_HEADING in opponent_prompt
assert WEAKNESS in opponent_prompt

print("✅ Weakness from PostgreSQL reached the Opponent prompt")


# ========================================
# New user has no memory
# ========================================

print("\n[4/4] Testing a user with no memories...")

state = new_state(f"opponent-memory-new-user-{uuid4()}")

state = DebateState(**memory_graph.invoke(state))

assert (
    state.metadata["memory_context"]
    == MemoryContextService.NO_MEMORY_CONTEXT
)

state = run_opponent(state, "AI will write most code within a decade.")

assert MEMORY_HEADING not in provider.prompts[-1]

print("✅ No memory section for a new user")


print("\n" + "=" * 50)
print("✅ ALL OPPONENT MEMORY TESTS PASSED")
print("=" * 50)
