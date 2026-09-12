from services.llm_service import LLMService
from services.providers.groq_provider import GroqProvider

from schemas.debate_plan import DebatePlan
from schemas.judge_result import JudgeResult
from schemas.reflection import ReflectionResult
from schemas.reasoning_fingerprint import ReasoningFingerprint
from schemas.reasoning_profile import UserReasoningProfile


print("========================================")
print("      GROQ ARGUMIND SCHEMA TEST")
print("========================================")


LLMService.set_provider(GroqProvider())


# --------------------------------------------------
# 1. DebatePlan
# --------------------------------------------------

print("\n[1/5] Testing DebatePlan...")

debate_plan = LLMService.generate_structured(
    """
Create a debate plan for:

Topic:
Should artificial intelligence replace most software engineers?

AI stance:
Oppose

Return a concise valid debate plan.
""",
    DebatePlan
)

print(debate_plan)

assert isinstance(debate_plan, DebatePlan)
assert debate_plan.ai_position == "Oppose"


# --------------------------------------------------
# 2. JudgeResult
# --------------------------------------------------

print("\n[2/5] Testing JudgeResult...")

judge_result = LLMService.generate_structured(
    """
Evaluate this hypothetical debate performance.

The user gave structured arguments with strong logical reasoning
but limited empirical evidence.

Return an objective judge result.
""",
    JudgeResult
)

print(judge_result)

assert isinstance(judge_result, JudgeResult)

assert 0 <= judge_result.logic_score <= 10
assert 0 <= judge_result.evidence_score <= 10
assert 0 <= judge_result.clarity_score <= 10
assert 0 <= judge_result.persuasion_score <= 10


# --------------------------------------------------
# 3. ReflectionResult
# --------------------------------------------------

print("\n[3/5] Testing ReflectionResult...")

reflection = LLMService.generate_structured(
    """
Analyze the following hypothetical USER reasoning:

The user argues that AI will increase software productivity,
reduce development costs, and therefore increase the amount of
software produced. They use causal reasoning and analogies but
provide little empirical evidence.

Analyze the user's reasoning only.
""",
    ReflectionResult
)

print(reflection)

assert isinstance(reflection, ReflectionResult)
assert 0 <= reflection.overall_reasoning_quality <= 10


# --------------------------------------------------
# 4. ReasoningFingerprint
# --------------------------------------------------

print("\n[4/5] Testing ReasoningFingerprint...")

fingerprint = LLMService.generate_structured(
    """
Create a reasoning fingerprint from this reflection:

Reasoning patterns:
- causal reasoning
- assumption testing
- analogy

Strengths:
- logical structure
- conceptual clarity

Weaknesses:
- limited empirical evidence

Evidence usage:
Mostly theoretical and hypothetical.

Overall reasoning quality:
8.5
""",
    ReasoningFingerprint
)

print(fingerprint)

assert isinstance(
    fingerprint,
    ReasoningFingerprint
)

assert 0 <= fingerprint.overall_reasoning_score <= 10


# --------------------------------------------------
# 5. UserReasoningProfile
# --------------------------------------------------

print("\n[5/5] Testing UserReasoningProfile...")

profile = LLMService.generate_structured(
    """
Build an evolving reasoning profile from this single fingerprint.

The user is:
- analytical
- structured
- causal
- strong at assumption testing
- weaker with empirical evidence

Return a reusable reasoning profile.
""",
    UserReasoningProfile
)

print(profile)

assert isinstance(
    profile,
    UserReasoningProfile
)

assert profile.debates_analyzed >= 0


# --------------------------------------------------
# Final result
# --------------------------------------------------

print("\n========================================")
print("✅ ALL ARGUMIND GROQ SCHEMA TESTS PASSED")
print("========================================")