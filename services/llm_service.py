from config.llm import client, DEFAULT_MODEL
import json

class LLMService:

    @staticmethod
    def generate(prompt: str) -> str:

        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt
        )

        return response.text
    @staticmethod
    def generate_json(prompt: str):

        prompt += """

Return ONLY valid JSON.

"""

        response = client.models.generate_content(

            model=DEFAULT_MODEL,

            contents=prompt

        )

        return json.loads(response.text)