from typing import Type

from pydantic import BaseModel

from services.providers.base import BaseLLMProvider
from services.provider_factory import create_default_router
from services.llm_router import LLMRouter


class LLMService:

    _router = create_default_router()


    @classmethod
    def set_provider(
        cls,
        provider: BaseLLMProvider
    ):
        """
        Set a single provider.

        Kept for backwards compatibility with
        existing tests and provider-specific testing.
        """

        cls._router = LLMRouter([
            provider
        ])


    @classmethod
    def set_router(
        cls,
        router: LLMRouter
    ):
        """
        Set the LLM router used by the application.
        """

        cls._router = router


    @classmethod
    def generate(
        cls,
        prompt: str
    ) -> str:

        return cls._router.generate(prompt)


    @classmethod
    def generate_structured(
        cls,
        prompt: str,
        schema: Type[BaseModel]
    ):

        return cls._router.generate_structured(
            prompt,
            schema
        )