import json
from typing import Type

from pydantic import BaseModel

from config.llm import client, DEFAULT_MODEL


class LLMService:

    @staticmethod
    def generate(prompt: str) -> str:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt
        )

        return response.text

    @staticmethod
    def generate_structured(prompt: str, schema: Type[BaseModel]):

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

        # Remove markdown if Gemini wraps JSON in ```json ... ```
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        data = json.loads(text)

        return schema(**data)