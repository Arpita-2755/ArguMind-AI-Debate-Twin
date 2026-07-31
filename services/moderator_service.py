from services.llm_service import LLMService


class ModeratorService:

    @staticmethod
    def analyze_topic(topic: str):

        prompt = f"""
You are an expert debate moderator.

Analyze the debate topic.

Topic:
{topic}

Return:

1. Topic Category
2. Difficulty
3. Recommended Debate Strategy

Keep your response short.
"""

        return LLMService.generate(prompt)