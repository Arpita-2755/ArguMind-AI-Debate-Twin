from typing import Type
from pydantic import BaseModel

from services.providers.base import BaseLLMProvider
from services.llm_errors import (
    LLMError,
    LLMAuthenticationError,
    LLMRateLimitError,
    LLMAccessError,
    LLMModelError,
    LLMConnectionError,
    LLMServerError,
)


class LLMRouter:

    FALLBACK_ERRORS = (
        LLMRateLimitError,
        LLMAccessError,
        LLMModelError,
        LLMConnectionError,
        LLMServerError,
    )

    def __init__(self, providers: list[BaseLLMProvider]):

        if not providers:
            raise ValueError(
                "LLMRouter requires at least one provider."
            )

        self.providers = providers

    def generate(self, prompt: str) -> str:

        errors = []

        for provider in self.providers:

            provider_name = type(provider).__name__

            try:

                print(
                    f"[LLM Router] Trying {provider_name}..."
                )

                response = provider.generate(prompt)

                print(
                    f"[LLM Router] {provider_name} succeeded."
                )

                return response

            except self.FALLBACK_ERRORS as error:

                print(
                    f"[LLM Router] {provider_name} "
                    f"temporarily unavailable: {error}"
                )

                errors.append(
                    f"{provider_name}: {error}"
                )

                continue

            except LLMAuthenticationError:

                print(
                    f"[LLM Router] {provider_name} "
                    f"authentication failed."
                )

                raise

            except LLMError:

                print(
                    f"[LLM Router] {provider_name} "
                    f"returned an unexpected LLM error."
                )

                raise

            except Exception:

                print(
                    f"[LLM Router] {provider_name} "
                    f"raised an unexpected error."
                )

                raise

        raise RuntimeError(
            "All LLM providers failed.\n"
            + "\n".join(errors)
        )

    def generate_structured(
        self,
        prompt: str,
        schema: Type[BaseModel]
    ):

        errors = []

        for provider in self.providers:

            provider_name = type(provider).__name__

            try:

                print(
                    f"[LLM Router] Trying {provider_name}..."
                )

                response = provider.generate_structured(
                    prompt,
                    schema
                )

                print(
                    f"[LLM Router] {provider_name} succeeded."
                )

                return response

            except self.FALLBACK_ERRORS as error:

                print(
                    f"[LLM Router] {provider_name} "
                    f"temporarily unavailable: {error}"
                )

                errors.append(
                    f"{provider_name}: {error}"
                )

                continue

            except LLMAuthenticationError:

                print(
                    f"[LLM Router] {provider_name} "
                    f"authentication failed."
                )

                raise

            except LLMError:

                print(
                    f"[LLM Router] {provider_name} "
                    f"returned an unexpected LLM error."
                )

                raise

            except Exception:

                print(
                    f"[LLM Router] {provider_name} "
                    f"raised an unexpected error."
                )

                raise

        raise RuntimeError(
            "All LLM providers failed.\n"
            + "\n".join(errors)
        )