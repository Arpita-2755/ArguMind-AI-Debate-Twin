from prompts.judge_prompt import build_judge_prompt
from schemas.judge_result import JudgeResult
from services.llm_service import LLMService


class JudgeService:

    @staticmethod
    def evaluate(transcript):

        prompt = build_judge_prompt(transcript)

        return LLMService.generate_structured(
            prompt,
            JudgeResult
        )