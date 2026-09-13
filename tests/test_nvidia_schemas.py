from services.providers.nvidia_provider import NVIDIAProvider

from schemas.debate_plan import DebatePlan
from schemas.judge_result import JudgeResult
from schemas.reflection import ReflectionResult
from schemas.reasoning_fingerprint import ReasoningFingerprint
from schemas.reasoning_profile import UserReasoningProfile


print("=" * 40)
print("     NVIDIA ARGUMIND SCHEMA TEST")
print("=" * 40)


provider = NVIDIAProvider()


# ----------------------------------------
# 1. DebatePlan
# ----------------------------------------

print("\n[1/5] Testing DebatePlan...")

debate_plan = provider.generate_structured(
    """
Create a debate plan for:

Topic:
Should artificial intelligence replace most software engineers?

AI Stance:
Oppose

Create a realistic debate plan.
Use exactly 5 rounds.
""",
    DebatePlan
)

print(debate_plan)

assert isinstance(debate_plan, DebatePlan)


# ----------------------------------------
# 2. JudgeResult
# ----------------------------------------

print("\n[2/5] Testing JudgeResult...")

judge_result = provider.generate_structured(
    """
Evaluate this hypothetical debate performance:

The user presented a structured argument with clear
reasoning and several counterarguments, but provided
little empirical evidence.

Return a realistic objective debate evaluation.
Scores must be between 0 and 10.
""",
    JudgeResult
)

print(judge_result)

assert isinstance(judge_result, JudgeResult)


# ----------------------------------------
# 3. ReflectionResult
# ----------------------------------------

print("\n[3/5] Testing ReflectionResult...")

reflection = provider.generate_structured(
    """
Analyze the following hypothetical USER reasoning:

The user argues that AI will increase software
engineering productivity because repetitive coding
tasks can be automated. They distinguish between
automation of implementation and the continued need
for human judgment.

Identify the user's reasoning patterns, strengths,
weaknesses, assumptions, fallacies, and evidence usage.
""",
    ReflectionResult
)

print(reflection)

assert isinstance(reflection, ReflectionResult)


# ----------------------------------------
# 4. ReasoningFingerprint
# ----------------------------------------

print("\n[4/5] Testing ReasoningFingerprint...")

fingerprint = provider.generate_structured(
    """
Create a reasoning fingerprint from this reflection:

The user tends to use causal reasoning, structured
arguments, assumption testing, and conceptual analogies.
They are logically strong but frequently rely on
hypothetical reasoning rather than empirical evidence.

Identify recurring reasoning characteristics.
""",
    ReasoningFingerprint
)

print(fingerprint)

assert isinstance(
    fingerprint,
    ReasoningFingerprint
)


# ----------------------------------------
# 5. UserReasoningProfile
# ----------------------------------------

print("\n[5/5] Testing UserReasoningProfile...")

profile = provider.generate_structured(
    """
Create an example long-term reasoning profile for a
user who has been analyzed across multiple debates.

The user tends to be analytical, structured, and
counterargument-driven.

They are strong at logical reasoning and assumption
testing but sometimes rely too heavily on theoretical
reasoning instead of empirical evidence.

Use debates_analyzed = 3.
""",
    UserReasoningProfile
)

print(profile)

assert isinstance(
    profile,
    UserReasoningProfile
)

assert profile.debates_analyzed == 3


print("\n" + "=" * 40)
print("✅ ALL NVIDIA ARGUMIND SCHEMA TESTS PASSED")
print("=" * 40)