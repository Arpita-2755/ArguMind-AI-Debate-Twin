import json
from typing import Type

from groq import Groq
from pydantic import BaseModel

from config.groq import GROQ_API_KEY, GROQ_MODEL
from services.providers.base import BaseLLMProvider
from groq import (
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

class GroqProvider(BaseLLMProvider):

    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not set in the environment."
            )

        self.client = Groq(api_key=GROQ_API_KEY)

    def generate(self, prompt: str):

        try:

            response = self.client.chat.completions.create(
                model=GROQ_MODEL,
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
        Convert a Pydantic JSON schema into a schema compatible
        with Groq strict structured-output mode.
        """

        if not isinstance(schema, dict):
            return schema

        # Groq strict mode requires every object property
        # to appear in the required array.
        if schema.get("type") == "object":

            properties = schema.get("properties", {})

            schema["additionalProperties"] = False

            if properties:
                schema["required"] = list(properties.keys())

        # Recursively process nested dictionaries and lists.
        for key, value in list(schema.items()):

            if isinstance(value, dict):
                schema[key] = GroqProvider._make_strict_schema(value)

            elif isinstance(value, list):
                schema[key] = [
                    GroqProvider._make_strict_schema(item)
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

        json_schema = schema.model_json_schema()

        json_schema = self._make_strict_schema(
            json_schema
        )

        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
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
            }
        )

        text = response.choices[0].message.content

        data = json.loads(text)

        return schema.model_validate(data)

    @staticmethod
    def _translate_error(error: Exception) -> Exception:

        if isinstance(error, AuthenticationError):
            return LLMAuthenticationError(
                "Groq authentication failed."
            )

        if isinstance(error, RateLimitError):
            return LLMRateLimitError(
                "Groq rate limit or quota exceeded."
            )

        if isinstance(error, APIConnectionError):
            return LLMConnectionError(
                "Could not connect to Groq."
            )

        if isinstance(error, APIStatusError):

            status_code = error.status_code

            if status_code == 402:
                return LLMAccessError(
                    "Groq access or billing restriction."
                )

            if status_code in (404, 410):
                return LLMModelError(
                    "Groq model is unavailable."
                )

            if status_code >= 500:
                return LLMServerError(
                    "Groq server error."
                )

        return error