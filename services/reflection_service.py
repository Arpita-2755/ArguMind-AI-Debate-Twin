from prompts.reflection_prompt import build_reflection_prompt
from schemas.reflection import ReflectionResult
from services.llm_service import LLMService


class ReflectionService:

    @staticmethod
    def analyze(transcript, judge_result):

        prompt = build_reflection_prompt(
            transcript,
            judge_result
        )

        return LLMService.generate_structured(
            prompt,
            ReflectionResult
        )