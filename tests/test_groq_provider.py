from services.llm_service import LLMService
from services.providers.groq_provider import GroqProvider
from schemas.reasoning_profile import UserReasoningProfile


print("========================================")
print("       GROQ PROVIDER TEST")
print("========================================")


# --------------------------------------------------
# 1. Switch provider
# --------------------------------------------------

LLMService.set_provider(GroqProvider())

print("\nProvider:")
print(type(LLMService._provider).__name__)


# --------------------------------------------------
# 2. Test normal generation
# --------------------------------------------------

print("\nTesting normal generation...")

response = LLMService.generate(
    "Explain in 3 sentences why logical reasoning is important in a debate."
)

print("\nResponse:")
print(response)


# --------------------------------------------------
# 3. Test structured generation
# --------------------------------------------------

print("\nTesting structured generation...")

profile = LLMService.generate_structured(
    """
Create a simple reasoning profile for a hypothetical user.

The user is:
- analytical
- structured
- good at identifying assumptions
- sometimes weak with empirical evidence

Return the requested structured profile.
""",
    UserReasoningProfile
)


print("\nStructured response:")
print(profile)


# --------------------------------------------------
# 4. Assertions
# --------------------------------------------------

assert isinstance(response, str)
assert len(response.strip()) > 0

assert isinstance(
    profile,
    UserReasoningProfile
)

assert profile.debates_analyzed >= 0

print("\n========================================")
print("✅ GROQ PROVIDER TEST PASSED")
print("========================================")