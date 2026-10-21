from typing import Type

import httpx
from google.genai import errors as genai_errors
from google.genai import types
from pydantic import BaseModel

from config.llm import client, DEFAULT_MODEL
from services.providers.base import BaseLLMProvider
from services.providers.structured_output import (
    build_structured_prompt,
    parse_structured,
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


class GeminiProvider(BaseLLMProvider):

    def __init__(self):

        self.client = client

    def generate(self, prompt: str) -> str:

        try:

            response = self.client.models.generate_content(
                model=DEFAULT_MODEL,
                contents=prompt
            )

            text = response.text

            if not text:
                raise LLMResponseError(
                    "Gemini returned an empty response."
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

        try:

            response = self.client.models.generate_content(
                model=DEFAULT_MODEL,
                contents=build_structured_prompt(
                    prompt,
                    schema
                ),
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

            return parse_structured(
                response.text,
                schema,
                "Gemini"
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

        if isinstance(error, genai_errors.APIError):

            code = error.code
            message = str(error)

            # Gemini reports a bad key as 400 INVALID_ARGUMENT.
            if code in (401, 403) or (
                code == 400 and "API key" in message
            ):
                return LLMAuthenticationError(
                    "Gemini authentication failed."
                )

            if code == 429:
                return LLMRateLimitError(
                    "Gemini rate limit or quota exceeded."
                )

            if code == 402:
                return LLMAccessError(
                    "Gemini access or billing restriction."
                )

            if code in (404, 410):
                return LLMModelError(
                    "Gemini model is unavailable."
                )

            if code >= 500:
                return LLMServerError(
                    "Gemini server error."
                )

        # Also covers httpx timeouts, which subclass it.
        if isinstance(error, httpx.TransportError):
            return LLMConnectionError(
                "Could not connect to Gemini or the request timed out."
            )

        return error
