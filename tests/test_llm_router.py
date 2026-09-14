from services.llm_router import LLMRouter
from services.providers.base import BaseLLMProvider
from services.llm_errors import LLMRateLimitError

# ========================================
# Fake providers
# ========================================

class FailingProvider(BaseLLMProvider):

    def generate(self, prompt: str) -> str:
        raise LLMRateLimitError("Provider unavailable")

    def generate_structured(self, prompt: str, schema):
        raise LLMRateLimitError("Provider unavailable")


class SuccessfulProvider(BaseLLMProvider):

    def generate(self, prompt: str) -> str:
        return "Successful response"

    def generate_structured(self, prompt: str, schema):
        return schema(
            reasoning_style=["Analytical"],
            strongest_reasoning_patterns=["Logical reasoning"],
            weakest_reasoning_patterns=["Empirical reasoning"],
            evidence_style="Deductive",
            argument_style=["Structured"],
            common_assumptions=["Test assumption"],
            fallacy_tendencies=[],
            reasoning_strengths=["Logical"],
            reasoning_weaknesses=["Limited evidence"],
            overall_reasoning_score=8.5,
            debates_analyzed=1,
            profile_summary="Test profile"
        )


# ========================================
# Test normal generation
# ========================================

print("=" * 50)
print("          LLM ROUTER TEST")
print("=" * 50)

print("\n[1/3] Testing fallback...")


router = LLMRouter(
    providers=[
        FailingProvider(),
        SuccessfulProvider()
    ]
)


response = router.generate(
    "Test prompt"
)

print("\nResponse:")
print(response)

assert response == "Successful response"

print("✅ Router successfully fell back")


# ========================================
# Test structured generation
# ========================================

print("\n[2/3] Testing structured fallback...")

from schemas.reasoning_profile import UserReasoningProfile


profile = router.generate_structured(
    "Generate test profile",
    UserReasoningProfile
)

print("\nProfile:")
print(profile)

assert isinstance(
    profile,
    UserReasoningProfile
)

print("✅ Structured fallback works")


# ========================================
# Test all providers failing
# ========================================

print("\n[3/3] Testing complete failure...")

router = LLMRouter(
    providers=[
        FailingProvider(),
        FailingProvider()
    ]
)


try:

    router.generate(
        "Test prompt"
    )

    assert False, (
        "Router should have raised RuntimeError"
    )

except RuntimeError as e:

    print("\nExpected error:")
    print(e)

    assert "All LLM providers failed" in str(e)

print("✅ Complete failure handled correctly")


print("\n" + "=" * 50)
print("✅ ALL LLM ROUTER TESTS PASSED")
print("=" * 50)