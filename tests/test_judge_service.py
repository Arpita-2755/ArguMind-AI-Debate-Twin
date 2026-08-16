from schemas.debate_plan import DebatePlan
from schemas.debate_turn import DebateTurn
from schemas.debate_transcript import DebateTranscript

from services.judge_service import JudgeService


plan = DebatePlan(
    topic="Should AI replace software engineers?",
    category="Technology",
    difficulty="Intermediate",
    strategy="Evidence Driven",
    ai_position="Against",
    rounds=3,
    opening_speaker="User"
)

turns = [
    DebateTurn(
        round_number=1,
        phase="Opening",
        user_argument="""
AI can replace software engineers because it can write code much faster,
works continuously without fatigue, and reduces software development costs.
        """,
        opponent_argument="""
AI is a powerful tool, but software engineering is more than writing code.
Architecture, ethics, accountability, and creative problem solving still
require humans.
        """
    )
]

transcript = DebateTranscript(
    topic=plan.topic,
    debate_plan=plan,
    turns=turns
)

result = JudgeService.evaluate(transcript)

print("\n========== JUDGE RESULT ==========\n")

print(result)
print(type(result))