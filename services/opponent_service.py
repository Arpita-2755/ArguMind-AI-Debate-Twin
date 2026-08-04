from services.llm_service import LLMService
from prompts.opponent_prompt import build_opponent_prompt


class OpponentService:

    @staticmethod
    def generate_opening(plan, user_position):

        prompt = build_opponent_prompt(
            plan,
            user_position
        )

        return LLMService.generate(prompt)