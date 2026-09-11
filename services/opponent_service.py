from services.llm_service import LLMService
from prompts.opponent_prompt import build_opponent_prompt


class OpponentService:

    @staticmethod
    def generate_response(
        plan,
        user_argument,
        debate_history
    ):

        prompt = build_opponent_prompt(
            plan,
            user_argument,
            debate_history
        )

        return LLMService.generate(prompt)