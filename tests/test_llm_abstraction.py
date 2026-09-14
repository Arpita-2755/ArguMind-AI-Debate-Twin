from services.llm_service import LLMService
from services.providers.base import BaseLLMProvider


class FakeProvider(BaseLLMProvider):

    def generate(self, prompt: str) -> str:

        return f"FAKE RESPONSE: {prompt}"


    def generate_structured(self, prompt: str, schema):

        return schema(
            reasoning_style=["Analytical"],
            strongest_reasoning_patterns=["Causal reasoning"],
            weakest_reasoning_patterns=["Empirical reasoning"],
            evidence_style="Mostly deductive",
            argument_style=["Structured"],
            common_assumptions=["Test assumption"],
            fallacy_tendencies=[],
            reasoning_strengths=["Logical"],
            reasoning_weaknesses=["Limited evidence"],
            overall_reasoning_score=8.5,
            debates_analyzed=1,
            profile_summary="Test profile"
        )


print("Testing LLM abstraction...")


LLMService.set_provider(FakeProvider())


response = LLMService.generate(
    "Hello"
)

print("\nGenerate response:")
print(response)


from schemas.reasoning_profile import UserReasoningProfile


profile = LLMService.generate_structured(
    "Generate profile",
    UserReasoningProfile
)

print("\nStructured response:")
print(profile)


print("Current router:")
print(type(LLMService._router).__name__)

print("Active provider:")
print(type(LLMService._router.providers[0]).__name__)


assert response == "FAKE RESPONSE: Hello"

assert isinstance(
    profile,
    UserReasoningProfile
)

assert type(
    LLMService._router.providers[0]
).__name__ == "FakeProvider"


print("\n✅ LLM abstraction works!")