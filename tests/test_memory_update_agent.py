from uuid import uuid4

from db.repositories.reasoning_memory_repository import (
    ReasoningMemoryRepository,
)
from graph.builder import (
    memory_graph,
    memory_update_graph,
    opponent_graph,
)
from graph.enums import DebatePhase
from graph.state import DebateState
from schemas.debate_plan import DebatePlan
from schemas.reasoning_fingerprint import ReasoningFingerprint
from services.debate_service import DebateService
from services.llm_service import LLMService
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


TOPIC = "Should AI replace software engineers?"

WEAKNESS = "Relies on anecdotes instead of data"


def create_fingerprint() -> ReasoningFingerprint:

    return ReasoningFingerprint(
        reasoning_style=["Analytical"],
        strongest_reasoning_patterns=["Causal reasoning"],
        weakest_reasoning_patterns=["Empirical reasoning"],
        evidence_style="Mostly hypothetical examples.",
        argument_style=["Structured"],
        common_assumptions=["Technology trends continue linearly"],
        fallacy_tendencies=[],
        reasoning_strengths=["Clear structure"],
        reasoning_weaknesses=[WEAKNESS],
        overall_reasoning_score=7.5,
        profile_summary="Structured but light on evidence.",
    )


def new_state(user_id):

    state = DebateState(
        topic=TOPIC,
        user_stance="Support",
        ai_stance="Oppose",
        current_phase=DebatePhase.OPENING,
    )

    state.metadata["user_id"] = user_id

    return state


def finish_debate(user_id):
    """Simulate the end of a debate: the analyzer has produced a fingerprint."""

    state = new_state(user_id)

    state.metadata["reasoning_fingerprint"] = create_fingerprint()

    return DebateState(**memory_update_graph.invoke(state))


print("=" * 50)
print("     MEMORY UPDATE AGENT TEST")
print("=" * 50)

user_id = f"memory-update-test-{uuid4()}"


# ========================================
# Debate 1 saves memories
# ========================================

print("\n[1/3] Testing memories are saved after debate 1...")

state = finish_debate(user_id)

stored = ReasoningMemoryRepository.get_by_user(user_id)

assert state.metadata["stored_memory_count"] == len(stored) > 0
assert state.metadata["debate_id"].startswith("debate-")
assert any(memory.content == WEAKNESS for memory in stored)
assert all(memory.topics == [TOPIC] for memory in stored)

print(f"✅ Saved {len(stored)} memories")


# ========================================
# Debate 2 uses them
# ========================================

print("\n[2/3] Testing debate 2's Opponent sees debate 1's memories...")

provider = RecordingProvider()

LLMService.set_provider(provider)

state = new_state(user_id)

state = DebateState(**memory_graph.invoke(state))

state.debate_plan = DebatePlan(
    topic=TOPIC,
    category="Technology",
    difficulty="Intermediate",
    strategy="Evidence Driven",
    ai_position="Oppose",
    rounds=3,
    opening_speaker="User"
)

state = DebateService.start_turn(
    state,
    "Everyone I know uses AI to code now."
)

state = DebateState(**opponent_graph.invoke(state))

assert WEAKNESS in provider.prompts[-1]

print("✅ Weakness from debate 1 reached the Opponent in debate 2")


# ========================================
# Repeat debates consolidate, not duplicate
# ========================================

print("\n[3/3] Testing a repeated fingerprint is consolidated...")

finish_debate(user_id)

stored_again = ReasoningMemoryRepository.get_by_user(user_id)

assert len(stored_again) == len(stored)

weakness = next(
    memory for memory in stored_again
    if memory.content == WEAKNESS
)

assert weakness.source_debate_count == 2

print("✅ No duplicates; debate count went up to 2")


print("\n" + "=" * 50)
print("✅ ALL MEMORY UPDATE AGENT TESTS PASSED")
print("=" * 50)
