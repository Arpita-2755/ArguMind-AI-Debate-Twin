class LLMError(Exception):
    """Base exception for LLM-related errors."""
    pass


class LLMAuthenticationError(LLMError):
    """API key or authentication failure."""
    pass


class LLMRateLimitError(LLMError):
    """Provider rate limit or quota exceeded."""
    pass


class LLMAccessError(LLMError):
    """Provider access/billing restriction."""
    pass


class LLMModelError(LLMError):
    """Requested model is unavailable or unsupported."""
    pass


class LLMConnectionError(LLMError):
    """Network or connection failure."""
    pass


class LLMServerError(LLMError):
    """Provider-side server failure."""
    pass