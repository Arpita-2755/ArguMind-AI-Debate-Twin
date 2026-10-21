from types import SimpleNamespace

import httpx
from openai import APITimeoutError
from pydantic import BaseModel

from services.llm_errors import (
    LLMConnectionError,
    LLMResponseError,
)
from services.llm_router import LLMRouter
from services.providers.nvidia_provider import NVIDIAProvider
from schemas.debate_plan import DebatePlan


# ========================================
# Fakes (no API calls)
# ========================================

class FakeCompletions:

    def __init__(self, content=None, error=None):
        self.content = content
        self.error = error

    def create(self, **kwargs):

        if self.error:
            raise self.error

        message = SimpleNamespace(content=self.content)

        return SimpleNamespace(
            choices=[SimpleNamespace(message=message)]
        )


def fake_nvidia(content=None, error=None):

    provider = NVIDIAProvider.__new__(NVIDIAProvider)

    provider.client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=FakeCompletions(content, error)
        )
    )

    return provider


class Answer(BaseModel):
    answer: str


class SuccessfulProvider:

    def generate(self, prompt):
        return "Fallback provider answered."

    def generate_structured(self, prompt, schema):
        return schema(answer="Fallback provider answered.")


def expect_response_error(provider, schema=Answer):

    try:
        provider.generate_structured("test", schema)
    except LLMResponseError as error:
        print(f"LLMResponseError: {str(error)[:80]}")
        return

    raise AssertionError("Expected LLMResponseError")


print("=" * 50)
print("     NVIDIA RESPONSE ERROR TEST")
print("=" * 50)


# ========================================
# Valid JSON wrapped in extra text
# ========================================

print("\n[1/7] Testing valid JSON inside extra text...")

provider = fake_nvidia(
    'Here you go:\n```json\n{"answer": "ok"}\n```'
)

result = provider.generate_structured("test", Answer)

assert result.answer == "ok"

print("✅ JSON extracted and validated")


# ========================================
# Empty response
# ========================================

print("\n[2/7] Testing empty structured response...")

expect_response_error(fake_nvidia(""))

print("✅ Empty response translated")


# ========================================
# Truncated JSON (the 22,000-line failure)
# ========================================

print("\n[3/7] Testing truncated JSON...")

expect_response_error(
    fake_nvidia('{"answer": "ok", "extra": [1, 2')
)

expect_response_error(
    fake_nvidia('{"answer": "ok" "broken": }')
)

print("✅ Malformed JSON translated")


# ========================================
# JSON that fails schema validation
# ========================================

print("\n[4/7] Testing schema validation failure...")

expect_response_error(
    fake_nvidia('{"topic": "AI"}'),
    DebatePlan
)

print("✅ Validation error translated")


# ========================================
# Empty plain-text response
# ========================================

print("\n[5/7] Testing empty text response...")

try:
    fake_nvidia(None).generate("test")
    raise AssertionError("Expected LLMResponseError")
except LLMResponseError as error:
    print(f"LLMResponseError: {error}")

print("✅ Empty text response translated")


# ========================================
# Timeout
# ========================================

print("\n[6/7] Testing request timeout...")

timeout = APITimeoutError(
    request=httpx.Request("POST", "https://example.invalid")
)

try:
    fake_nvidia(error=timeout).generate_structured("test", Answer)
    raise AssertionError("Expected LLMConnectionError")
except LLMConnectionError as error:
    print(f"LLMConnectionError: {error}")

print("✅ Timeout translated")


# ========================================
# Router falls back on bad output
# ========================================

print("\n[7/7] Testing router fallback on bad NVIDIA output...")

router = LLMRouter([
    fake_nvidia('{"answer": '),
    SuccessfulProvider(),
])

result = router.generate_structured("test", Answer)

assert result.answer == "Fallback provider answered."

print("✅ Router fell back to the next provider")


print("\n" + "=" * 50)
print("✅ ALL NVIDIA RESPONSE ERROR TESTS PASSED")
print("=" * 50)
