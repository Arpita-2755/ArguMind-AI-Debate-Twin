from services.llm_errors import (
    LLMError,
    LLMAuthenticationError,
    LLMRateLimitError,
    LLMAccessError,
    LLMModelError,
    LLMConnectionError,
    LLMServerError,
)


print("=" * 50)
print("          LLM ERROR TEST")
print("=" * 50)


errors = [
    LLMAuthenticationError(
        "Invalid API key"
    ),
    LLMRateLimitError(
        "Rate limit exceeded"
    ),
    LLMAccessError(
        "Provider access denied"
    ),
    LLMModelError(
        "Model unavailable"
    ),
    LLMConnectionError(
        "Connection failed"
    ),
    LLMServerError(
        "Provider server error"
    ),
]


for error in errors:

    print(
        f"\n{type(error).__name__}: "
        f"{error}"
    )

    assert isinstance(
        error,
        LLMError
    )


print("\n" + "=" * 50)
print("✅ ALL LLM ERROR TESTS PASSED")
print("=" * 50)