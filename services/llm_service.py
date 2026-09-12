from typing import Type

from pydantic import BaseModel

from services.providers.base import BaseLLMProvider
from services.providers.gemini_provider import GeminiProvider


class LLMService:

    _provider: BaseLLMProvider = GeminiProvider()


    @classmethod
    def set_provider(
        cls,
        provider: BaseLLMProvider
    ):
        cls._provider = provider


    @classmethod
    def generate(
        cls,
        prompt: str
    ) -> str:

        return cls._provider.generate(prompt)


    @classmethod
    def generate_structured(
        cls,
        prompt: str,
        schema: Type[BaseModel]
    ):

        return cls._provider.generate_structured(
            prompt,
            schema
        )