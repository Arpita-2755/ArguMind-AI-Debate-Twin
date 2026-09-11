from services.llm_service import LLMService
from schemas.debate_plan import DebatePlan


class ModeratorService:

    @staticmethod
    def create_plan(topic: str, ai_stance: str):

        prompt = f"""
You are an expert debate moderator.

Create a debate plan for the following debate.

Topic:
{topic}

AI Stance:
{ai_stance}

IMPORTANT:
- The AI stance is predetermined.
- You MUST use the given AI stance.
- Do NOT change, reverse, reinterpret, or invent a different stance.
- The "ai_position" field must match the provided AI stance.

Return JSON with the following structure:

{{
    "topic": "{topic}",
    "category": "",
    "difficulty": "",
    "strategy": "",
    "ai_position": "{ai_stance}",
    "rounds": 5,
    "opening_speaker": "User"
}}
"""

        return LLMService.generate_structured(
            prompt,
            DebatePlan
        )