from services.llm_service import LLMService
from schemas.debate_plan import DebatePlan


class ModeratorService:

    @staticmethod
    def create_plan(topic: str):

        prompt = f"""
You are an expert debate moderator.

Create a debate plan.

Topic:
{topic}

Return JSON with the following structure:

{{
    "topic": "{topic}",
    "category": "",
    "difficulty": "",
    "strategy": "",
    "ai_position": "",
    "rounds": 5,
    "opening_speaker": "User"
}}
"""

        return LLMService.generate_structured(
            prompt,
            DebatePlan
        )