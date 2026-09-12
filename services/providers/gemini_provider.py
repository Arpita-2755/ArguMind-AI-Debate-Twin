import json
from typing import Type

from pydantic import BaseModel

from config.llm import client, DEFAULT_MODEL
from services.providers.base import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):

    def generate(self, prompt: str) -> str:

        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt
        )

        return response.text


    def generate_structured(
        self,
        prompt: str,
        schema: Type[BaseModel]
    ):

        prompt += """
Return ONLY valid JSON.
Do not include markdown.
Do not include explanation.
"""

        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = (
                text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

        data = json.loads(text)

        return schema(**data)