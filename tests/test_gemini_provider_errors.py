from types import SimpleNamespace

import httpx
from google.genai import errors as genai_errors
from pydantic import BaseModel

from services.llm_errors import (
    LLMAuthenticationError,
    LLMRateLimitError,
    LLMModelError,
    LLMConnectionError,
    LLMServerError,
    LLMResponseError,
)
from services.llm_router import LLMRouter
from services.providers.gemini_provider import GeminiProvider
from schemas.debate_plan import DebatePlan


# ========================================
# Fakes (no API calls)
# ========================================

class FakeModels:

    def __init__(self, text=None, error=None):
        self.text = text
        self.error = error

    def generate_content(self, **kwargs):

        if self.error:
            raise self.error

        return SimpleNamespace(text=self.text)


def fake_gemini(text=None, error=None):

    provider = GeminiProvider()

    provider.client = SimpleNamespace(
        models=FakeModels(text, error)
    )

    return provider


def api_error(error_class, code, status, message):

    return error_class(
        code,
        {
            "error": {
                "code": code,
                "status": status,
                "message": message,
            }
        }
    )


class Answer(BaseModel):
    answer: str


class SuccessfulProvider:

    def generate(self, prompt):
        return "Fallback provider answered."

    def generate_structured(self, prompt, schema):
        return schema(answer="Fallback provider answered.")


def expect(error_type, call):

    try:
        call()
    except error_type as error:
        print(f"{error_type.__name__}: {str(error)[:80]}")
        return

    raise AssertionError(f"Expected {error_type.__name__}")


print("=" * 50)
print("     GEMINI PROVIDER ERROR TEST")
print("=" * 50)


# ========================================
# Structured output
# ========================================

print("\n[1/8] Testing valid JSON in a code fence...")

result = fake_gemini(
    '```json\n{"answer": "ok"}\n```'
).generate_structured("test", Answer)

assert result.answer == "ok"

print("✅ JSON extracted and validated")


print("\n[2/8] Testing JSON missing schema fields...")

expect(
    LLMResponseError,
    lambda: fake_gemini('{"topic": "AI"}').generate_structured(
        "test",
        DebatePlan
    )
)

print("✅ Validation error translated")


print("\n[3/8] Testing malformed and empty responses...")

expect(
    LLMResponseError,
    lambda: fake_gemini('{"answer": "ok" "x": }').generate_structured(
        "test",
        Answer
    )
)

expect(
    LLMResponseError,
    lambda: fake_gemini(None).generate_structured("test", Answer)
)

expect(
    LLMResponseError,
    lambda: fake_gemini("").generate("test")
)

print("✅ Malformed and empty responses translated")


# ========================================
# API errors
# ========================================

print("\n[4/8] Testing rate limit (429)...")

expect(
    LLMRateLimitError,
    lambda: fake_gemini(
        error=api_error(
            genai_errors.ClientError,
            429,
            "RESOURCE_EXHAUSTED",
            "Quota exceeded"
        )
    ).generate("test")
)

print("✅ Rate limit translated")


print("\n[5/8] Testing invalid API key (400)...")

expect(
    LLMAuthenticationError,
    lambda: fake_gemini(
        error=api_error(
            genai_errors.ClientError,
            400,
            "INVALID_ARGUMENT",
            "API key not valid. Please pass a valid API key."
        )
    ).generate("test")
)

print("✅ Authentication error translated")


print("\n[6/8] Testing unknown model (404) and overload (503)...")

expect(
    LLMModelError,
    lambda: fake_gemini(
        error=api_error(
            genai_errors.ClientError,
            404,
            "NOT_FOUND",
            "Model not found"
        )
    ).generate_structured("test", Answer)
)

expect(
    LLMServerError,
    lambda: fake_gemini(
        error=api_error(
            genai_errors.ServerError,
            503,
            "UNAVAILABLE",
            "The model is overloaded"
        )
    ).generate_structured("test", Answer)
)

print("✅ Model and server errors translated")


print("\n[7/8] Testing timeout...")

expect(
    LLMConnectionError,
    lambda: fake_gemini(
        error=httpx.ReadTimeout("timed out")
    ).generate("test")
)

print("✅ Timeout translated")


# ========================================
# Router fallback
# ========================================

print("\n[8/8] Testing router fallback on bad Gemini output...")

router = LLMRouter([
    fake_gemini('{"topic": "AI"}'),
    SuccessfulProvider(),
])

result = router.generate_structured("test", Answer)

assert result.answer == "Fallback provider answered."

print("✅ Router fell back to the next provider")


print("\n" + "=" * 50)
print("✅ ALL GEMINI PROVIDER ERROR TESTS PASSED")
print("=" * 50)
