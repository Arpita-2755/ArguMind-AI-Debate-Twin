from pydantic import BaseModel

from services.llm_router import LLMRouter

from services.llm_errors import (
    LLMAuthenticationError,
    LLMRateLimitError,
    LLMAccessError,
    LLMModelError,
    LLMConnectionError,
    LLMServerError,
)


class TestSchema(BaseModel):
    answer: str


class FailingProvider:

    def __init__(self, error):
        self.error = error

    def generate(self, prompt):
        raise self.error

    def generate_structured(self, prompt, schema):
        raise self.error


class SuccessfulProvider:

    def generate(self, prompt):
        return "SUCCESS"

    def generate_structured(self, prompt, schema):
        return schema(answer="SUCCESS")


# --------------------------------------------------
# RATE LIMIT → FALLBACK
# --------------------------------------------------

print("\n[1/8] Rate limit should fallback...")

router = LLMRouter([
    FailingProvider(
        LLMRateLimitError("rate limited")
    ),
    SuccessfulProvider(),
])

result = router.generate("test")

assert result == "SUCCESS"

print("✅ PASS")


# --------------------------------------------------
# ACCESS ERROR → FALLBACK
# --------------------------------------------------

print("\n[2/8] Access error should fallback...")

router = LLMRouter([
    FailingProvider(
        LLMAccessError("access denied")
    ),
    SuccessfulProvider(),
])

result = router.generate("test")

assert result == "SUCCESS"

print("✅ PASS")


# --------------------------------------------------
# MODEL ERROR → FALLBACK
# --------------------------------------------------

print("\n[3/8] Model error should fallback...")

router = LLMRouter([
    FailingProvider(
        LLMModelError("model unavailable")
    ),
    SuccessfulProvider(),
])

result = router.generate("test")

assert result == "SUCCESS"

print("✅ PASS")


# --------------------------------------------------
# CONNECTION ERROR → FALLBACK
# --------------------------------------------------

print("\n[4/8] Connection error should fallback...")

router = LLMRouter([
    FailingProvider(
        LLMConnectionError("connection failed")
    ),
    SuccessfulProvider(),
])

result = router.generate("test")

assert result == "SUCCESS"

print("✅ PASS")


# --------------------------------------------------
# SERVER ERROR → FALLBACK
# --------------------------------------------------

print("\n[5/8] Server error should fallback...")

router = LLMRouter([
    FailingProvider(
        LLMServerError("server failed")
    ),
    SuccessfulProvider(),
])

result = router.generate("test")

assert result == "SUCCESS"

print("✅ PASS")


# --------------------------------------------------
# AUTHENTICATION → NO FALLBACK
# --------------------------------------------------

print("\n[6/8] Authentication error should NOT fallback...")

router = LLMRouter([
    FailingProvider(
        LLMAuthenticationError("bad API key")
    ),
    SuccessfulProvider(),
])

try:

    router.generate("test")

    raise AssertionError(
        "Authentication error should have been raised."
    )

except LLMAuthenticationError:

    print("✅ PASS")


# --------------------------------------------------
# STRUCTURED FALLBACK
# --------------------------------------------------

print("\n[7/8] Structured generation should fallback...")

router = LLMRouter([
    FailingProvider(
        LLMRateLimitError("rate limited")
    ),
    SuccessfulProvider(),
])

result = router.generate_structured(
    "test",
    TestSchema
)

assert result.answer == "SUCCESS"

print("✅ PASS")


# --------------------------------------------------
# ALL PROVIDERS FAIL
# --------------------------------------------------

print("\n[8/8] All fallback providers failing...")

router = LLMRouter([
    FailingProvider(
        LLMRateLimitError("provider 1 failed")
    ),
    FailingProvider(
        LLMServerError("provider 2 failed")
    ),
])

try:

    router.generate("test")

    raise AssertionError(
        "Router should raise RuntimeError."
    )

except RuntimeError as error:

    assert "All LLM providers failed." in str(error)

    print("✅ PASS")


print("\n" + "=" * 50)
print("✅ ALL ROUTER ERROR POLICY TESTS PASSED")
print("=" * 50)