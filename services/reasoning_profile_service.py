from prompts.reasoning_profile_prompt import build_reasoning_profile_prompt
from schemas.reasoning_fingerprint import ReasoningFingerprint
from schemas.reasoning_profile import UserReasoningProfile
from services.llm_service import LLMService


class ReasoningProfileService:

    @staticmethod
    def build_profile(
        fingerprints: list[ReasoningFingerprint]
    ):
        prompt = build_reasoning_profile_prompt(
            fingerprints
        )

        return LLMService.generate_structured(
            prompt,
            UserReasoningProfile
        )