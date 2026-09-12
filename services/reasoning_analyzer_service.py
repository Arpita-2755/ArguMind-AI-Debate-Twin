from prompts.reasoning_analyzer_prompt import build_reasoning_analyzer_prompt
from schemas.reasoning_fingerprint import ReasoningFingerprint
from services.llm_service import LLMService


class ReasoningAnalyzerService:

    @staticmethod
    def analyze(reflection):
        prompt = build_reasoning_analyzer_prompt(
            reflection
        )

        return LLMService.generate_structured(
            prompt,
            ReasoningFingerprint
        )