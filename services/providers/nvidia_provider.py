import json
from typing import Type

from openai import OpenAI
from pydantic import BaseModel

from config.nvidia import (
    NVIDIA_API_KEY,
    NVIDIA_MODEL,
    NVIDIA_BASE_URL
)

from services.providers.base import BaseLLMProvider
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
)

class NVIDIAProvider(BaseLLMProvider):

    def __init__(self):

        if not NVIDIA_API_KEY:
            raise ValueError(
                "NVIDIA_API_KEY is not set in the environment."
            )

        self.client = OpenAI(
            api_key=NVIDIA_API_KEY,
            base_url=NVIDIA_BASE_URL
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

            return response.choices[0].message.content

        except Exception as error:

            translated_error = self._translate_error(
                error
            )

            raise translated_error from error

    @staticmethod
    def _make_strict_schema(schema: dict) -> dict:
        """
        Convert a Pydantic JSON schema into a strict
        JSON schema compatible with NVIDIA structured outputs.
        """

        if not isinstance(schema, dict):
            return schema

        if schema.get("type") == "object":

            properties = schema.get(
                "properties",
                {}
            )

            schema["additionalProperties"] = False

            if properties:
                schema["required"] = list(
                    properties.keys()
                )

        for key, value in list(schema.items()):

            if isinstance(value, dict):

                schema[key] = (
                    NVIDIAProvider._make_strict_schema(
                        value
                    )
                )

            elif isinstance(value, list):

                schema[key] = [
                    NVIDIAProvider._make_strict_schema(item)
                    if isinstance(item, dict)
                    else item
                    for item in value
                ]

        return schema

    def generate_structured(
        self,
        prompt: str,
        schema: Type[BaseModel]
    ):

        try:

            json_schema = schema.model_json_schema()

            json_schema = (
                self._make_strict_schema(
                    json_schema
                )
            )

            response = self.client.chat.completions.create(
                model=NVIDIA_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": schema.__name__,
                        "strict": True,
                        "schema": json_schema
                    }
                },
                max_tokens=2048
            )

            text = response.choices[0].message.content

            data = json.loads(text)

            return schema.model_validate(data)

        except Exception as error:

            translated_error = self._translate_error(
                error
            )

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

        if isinstance(error, APIConnectionError):
            return LLMConnectionError(
                "Could not connect to NVIDIA."
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