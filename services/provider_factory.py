from services.llm_router import LLMRouter

from services.providers.groq_provider import GroqProvider
from services.providers.nvidia_provider import NVIDIAProvider
from services.providers.gemini_provider import GeminiProvider

from config.groq import GROQ_API_KEY
from config.nvidia import NVIDIA_API_KEY
from config.llm import client


def create_default_router() -> LLMRouter:

    providers = []

    # ---------------------------------------------
    # 1. Groq
    # ---------------------------------------------

    if GROQ_API_KEY:
        providers.append(
            GroqProvider()
        )


    # ---------------------------------------------
    # 2. NVIDIA
    # ---------------------------------------------

    if NVIDIA_API_KEY:
        providers.append(
            NVIDIAProvider()
        )


    # ---------------------------------------------
    # 3. Gemini
    # ---------------------------------------------

    if client:
        providers.append(
            GeminiProvider()
        )


    # ---------------------------------------------
    # Safety check
    # ---------------------------------------------

    if not providers:
        raise RuntimeError(
            "No LLM providers are configured. "
            "Please configure at least one provider."
        )


    return LLMRouter(providers)