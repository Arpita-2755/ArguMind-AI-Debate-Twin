import json
import time
from typing import Type

from pydantic import BaseModel

from config.llm import client, DEFAULT_MODEL


class LLMService:

    MAX_RETRIES = 3
    RETRY_DELAY = 2

    @staticmethod
    def generate(prompt: str) -> str:

        for attempt in range(LLMService.MAX_RETRIES):

            try:

                response = client.models.generate_content(
                    model=DEFAULT_MODEL,
                    contents=prompt
                )

                return response.text

            except Exception as e:

                print(f"[LLM] Attempt {attempt + 1} failed: {e}")

                if attempt == LLMService.MAX_RETRIES - 1:
                    raise

                time.sleep(LLMService.RETRY_DELAY)

    @staticmethod
    def generate_structured(prompt: str, schema: Type[BaseModel]):

        prompt += """

Return ONLY valid JSON.
Do not include markdown.
Do not include explanation.
"""

        for attempt in range(LLMService.MAX_RETRIES):

            try:

                response = client.models.generate_content(
                    model=DEFAULT_MODEL,
                    contents=prompt
                )

                text = response.text.strip()

                if text.startswith("```"):
                    text = text.replace("```json", "").replace("```", "").strip()

                data = json.loads(text)

                return schema(**data)

            except Exception as e:

                print(f"[LLM] Attempt {attempt + 1} failed: {e}")

                if attempt == LLMService.MAX_RETRIES - 1:
                    raise

                time.sleep(LLMService.RETRY_DELAY)