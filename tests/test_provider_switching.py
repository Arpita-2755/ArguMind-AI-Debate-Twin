from services.llm_service import LLMService

from services.providers.groq_provider import GroqProvider
from services.providers.nvidia_provider import NVIDIAProvider


print("=" * 50)
print("       ARGUMIND PROVIDER SWITCHING TEST")
print("=" * 50)


# ----------------------------------------
# NVIDIA
# ----------------------------------------

print("\n[1/2] Switching to NVIDIA...")

LLMService.set_provider(NVIDIAProvider())

print("Current provider:")
print(type(LLMService._router.providers[0]).__name__)

response = LLMService.generate(
    "Explain in one sentence what a debate is."
)

print("\nNVIDIA response:")
print(response)

assert type(LLMService._router.providers[0]).__name__ == "NVIDIAProvider"
assert isinstance(response, str)
assert len(response.strip()) > 0

print("✅ NVIDIA works through LLMService")


# ----------------------------------------
# Groq
# ----------------------------------------

print("\n[2/2] Switching to Groq...")

LLMService.set_provider(GroqProvider())

print(
    "Current provider:",
    type(LLMService._router.providers[0]).__name__
)

response = LLMService.generate(
    "Explain in one sentence what logical reasoning is."
)

print("\nGroq response:")
print(response)

assert type(LLMService._router.providers[0]).__name__ == "GroqProvider"
assert isinstance(response, str)
assert len(response.strip()) > 0

print("✅ Groq works through LLMService")


print("\n" + "=" * 50)
print("✅ PROVIDER SWITCHING TEST PASSED")
print("=" * 50)