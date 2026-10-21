from typing import Type

from openai import OpenAI
from pydantic import BaseModel

from config.nvidia import (
    NVIDIA_API_KEY,
    NVIDIA_MODEL,
    NVIDIA_BASE_URL,
    NVIDIA_TIMEOUT_SECONDS
)

from services.providers.base import BaseLLMProvider
from services.providers.structured_output import (
    build_structured_prompt,
    parse_structured,
)
from openai import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    RateLimitError,
)

from services.llm_errors import (
    LLMAuthenticationError,
    LLMRateLimitError,
    LLMAccessError,
    LLMModelError,
    LLMConnectionError,
    LLMServerError,
    LLMResponseError,
)

class NVIDIAProvider(BaseLLMProvider):

    def __init__(self):

        if not NVIDIA_API_KEY:
            raise ValueError(
                "NVIDIA_API_KEY is not set in the environment."
            )

        # No SDK retries: a slow NVIDIA call should hand over
        # to the next provider, not be retried here.
        self.client = OpenAI(
            api_key=NVIDIA_API_KEY,
            base_url=NVIDIA_BASE_URL,
            timeout=NVIDIA_TIMEOUT_SECONDS,
            max_retries=0
        )

    def generate(self, prompt: str):

        try:

            response = self.client.chat.completions.create(
                model=NVIDIA_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            text = response.choices[0].message.content

            if not text:
                raise LLMResponseError(
                    "NVIDIA returned an empty response."
                )

            return text

        except Exception as error:

            translated_error = self._translate_error(
                error
            )

            if translated_error is error:
                raise

            raise translated_error from error

    def generate_structured(
        self,
        prompt: str,
        schema: Type[BaseModel]
    ):

        # The schema goes in the prompt instead of NVIDIA's
        # strict json_schema mode, which hangs or produces
        # runaway output on the free endpoint.

        try:

            response = self.client.chat.completions.create(
                model=NVIDIA_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": build_structured_prompt(
                            prompt,
                            schema
                        )
                    }
                ],
                max_tokens=4096
            )

            text = response.choices[0].message.content

            return parse_structured(
                text,
                schema,
                "NVIDIA"
            )

        except Exception as error:

            translated_error = self._translate_error(
                error
            )

            if translated_error is error:
                raise

            raise translated_error from error

    @staticmethod
    def _translate_error(error: Exception) -> Exception:

        if isinstance(error, AuthenticationError):
            return LLMAuthenticationError(
                "NVIDIA authentication failed."
            )

        if isinstance(error, RateLimitError):
            return LLMRateLimitError(
                "NVIDIA rate limit or quota exceeded."
            )

        # Also covers APITimeoutError, which subclasses it.
        if isinstance(error, APIConnectionError):
            return LLMConnectionError(
                "Could not connect to NVIDIA or the request timed out."
            )

        if isinstance(error, APIStatusError):

            status_code = error.status_code

            if status_code == 402:
                return LLMAccessError(
                    "NVIDIA access or billing restriction."
                )

            if status_code in (404, 410):
                return LLMModelError(
                    "NVIDIA model is unavailable."
                )

            if status_code >= 500:
                return LLMServerError(
                    "NVIDIA server error."
                )

        return error
