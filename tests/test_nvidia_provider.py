from services.providers.nvidia_provider import NVIDIAProvider
from schemas.reasoning_profile import UserReasoningProfile


print("=" * 40)
print("       NVIDIA PROVIDER TEST")
print("=" * 40)


provider = NVIDIAProvider()

print("\nProvider:")
print(type(provider).__name__)


# ----------------------------------------
# Test normal generation
# ----------------------------------------

print("\nTesting normal generation...")

response = provider.generate(
    "Explain in one sentence why logical reasoning "
    "is important in a debate."
)

print("\nResponse:")
print(response)

assert isinstance(response, str)
assert len(response.strip()) > 0


# ----------------------------------------
# Test structured generation
# ----------------------------------------

print("\nTesting structured generation...")

profile = provider.generate_structured(
    """
Create a simple example reasoning profile for
a highly analytical debate participant.

The profile should contain realistic values for
every required field.
""",
    UserReasoningProfile
)

print("\nStructured response:")
print(profile)

assert isinstance(
    profile,
    UserReasoningProfile
)


print("\n" + "=" * 40)
print("✅ NVIDIA PROVIDER TEST PASSED")
print("=" * 40)