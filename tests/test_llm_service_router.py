from pydantic import BaseModel

from services.llm_service import LLMService
from services.llm_router import LLMRouter
from services.llm_errors import LLMRateLimitError


class TestSchema(BaseModel):
    answer: str


class FailingProvider:

    def generate(self, prompt):
        raise LLMRateLimitError("Provider rate limited.")

    def generate_structured(self, prompt, schema):
        raise LLMRateLimitError("Provider rate limited.")


class SuccessfulProvider:

    def generate(self, prompt):
        return "Router integration works."

    def generate_structured(self, prompt, schema):
        return schema(
            answer="Structured router integration works."
        )


print("=" * 55)
print("       LLM SERVICE + ROUTER INTEGRATION TEST")
print("=" * 55)


# --------------------------------------------------
# NORMAL GENERATION
# --------------------------------------------------

print("\n[1/3] Testing normal generation through LLMService...")

router = LLMRouter([
    SuccessfulProvider()
])

LLMService.set_router(router)

result = LLMService.generate("Test prompt")

assert result == "Router integration works."

print("✅ Normal generation passed")


# --------------------------------------------------
# STRUCTURED GENERATION
# --------------------------------------------------

print("\n[2/3] Testing structured generation...")

result = LLMService.generate_structured(
    "Test prompt",
    TestSchema
)

assert isinstance(result, TestSchema)
assert result.answer == "Structured router integration works."

print("✅ Structured generation passed")


# --------------------------------------------------
# FALLBACK
# --------------------------------------------------

print("\n[3/3] Testing router fallback through LLMService...")

router = LLMRouter([
    FailingProvider(),
    SuccessfulProvider()
])

LLMService.set_router(router)

result = LLMService.generate(
    "Test fallback"
)

assert result == "Router integration works."

print("✅ Fallback through LLMService passed")


print("\n" + "=" * 55)
print("✅ ALL LLM SERVICE ROUTER TESTS PASSED")
print("=" * 55)