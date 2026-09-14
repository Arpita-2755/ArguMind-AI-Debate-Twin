from groq import (
    AuthenticationError as GroqAuthenticationError,
    RateLimitError as GroqRateLimitError,
)

from openai import (
    AuthenticationError as OpenAIAuthenticationError,
    RateLimitError as OpenAIRateLimitError,
)

from services.providers.groq_provider import GroqProvider
from services.providers.nvidia_provider import NVIDIAProvider

from services.llm_errors import (
    LLMAuthenticationError,
    LLMRateLimitError,
)
class FakeRequest:
    pass
class FakeResponse:
    def __init__(self, status_code):
        self.request = FakeRequest()
        self.status_code = status_code
        self.headers = {}

print("=" * 50)
print("       PROVIDER ERROR TRANSLATION TEST")
print("=" * 50)


# ========================================
# Groq authentication error
# ========================================

print("\n[1/4] Testing Groq authentication error...")

error = GroqAuthenticationError(
    "Invalid API key",
    response=FakeResponse(401),
    body=None
)

translated = GroqProvider._translate_error(error)

print(type(translated).__name__)
print(translated)

assert isinstance(
    translated,
    LLMAuthenticationError
)

print("✅ Groq authentication error translated")


# ========================================
# Groq rate limit
# ========================================

print("\n[2/4] Testing Groq rate-limit error...")

error = GroqRateLimitError(
    "Rate limit exceeded",
    response=FakeResponse(429),
    body=None
)

translated = GroqProvider._translate_error(error)

print(type(translated).__name__)
print(translated)

assert isinstance(
    translated,
    LLMRateLimitError
)

print("✅ Groq rate-limit error translated")


# ========================================
# NVIDIA authentication error
# ========================================

print("\n[3/4] Testing NVIDIA authentication error...")

error = OpenAIAuthenticationError(
    "Invalid API key",
    response=FakeResponse(401),
    body=None
)

translated = NVIDIAProvider._translate_error(error)

print(type(translated).__name__)
print(translated)

assert isinstance(
    translated,
    LLMAuthenticationError
)

print("✅ NVIDIA authentication error translated")


# ========================================
# NVIDIA rate limit
# ========================================

print("\n[4/4] Testing NVIDIA rate-limit error...")

error = OpenAIRateLimitError(
    "Rate limit exceeded",
    response=FakeResponse(429),
    body=None
)

translated = NVIDIAProvider._translate_error(error)

print(type(translated).__name__)
print(translated)

assert isinstance(
    translated,
    LLMRateLimitError
)

print("✅ NVIDIA rate-limit error translated")


print("\n" + "=" * 50)
print("✅ ALL PROVIDER ERROR TESTS PASSED")
print("=" * 50)