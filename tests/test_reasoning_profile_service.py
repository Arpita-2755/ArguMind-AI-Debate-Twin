from schemas.reasoning_fingerprint import ReasoningFingerprint
from services.reasoning_profile_service import ReasoningProfileService


print("Testing Reasoning Profile Service...")


fingerprints = [

    # Debate 1
    ReasoningFingerprint(
        reasoning_style=[
            "Analytical",
            "Causal",
            "Theoretical"
        ],

        strongest_reasoning_patterns=[
            "Causal reasoning",
            "Assumption testing"
        ],

        weakest_reasoning_patterns=[
            "Empirical reasoning"
        ],

        evidence_style=(
            "Mostly deductive and hypothetical."
        ),

        argument_style=[
            "Structured",
            "Counterargument-driven"
        ],

        common_assumptions=[
            "Assumes technological capabilities will scale reliably."
        ],

        fallacy_tendencies=[],

        reasoning_strengths=[
            "Logical structure",
            "Conceptual clarity"
        ],

        reasoning_weaknesses=[
            "Limited empirical grounding"
        ],

        overall_reasoning_score=9.2,

        profile_summary=(
            "A structured analytical thinker."
        )
    ),


    # Debate 2
    ReasoningFingerprint(
        reasoning_style=[
            "Analytical",
            "Causal",
            "Conceptual"
        ],

        strongest_reasoning_patterns=[
            "Causal reasoning",
            "Counterargument"
        ],

        weakest_reasoning_patterns=[
            "Empirical reasoning"
        ],

        evidence_style=(
            "Relies primarily on logical reasoning "
            "and hypothetical scenarios."
        ),

        argument_style=[
            "Structured",
            "Counterargument-driven",
            "Principle-based"
        ],

        common_assumptions=[
            "Assumes incentives strongly influence outcomes."
        ],

        fallacy_tendencies=[],

        reasoning_strengths=[
            "Logical reasoning",
            "Strong counterarguments"
        ],

        reasoning_weaknesses=[
            "Limited empirical evidence"
        ],

        overall_reasoning_score=8.8,

        profile_summary=(
            "A logically structured and causal thinker."
        )
    ),


    # Debate 3
    ReasoningFingerprint(
        reasoning_style=[
            "Analytical",
            "Causal",
            "Theoretical"
        ],

        strongest_reasoning_patterns=[
            "Assumption testing",
            "Causal reasoning"
        ],

        weakest_reasoning_patterns=[
            "Evidence-based reasoning"
        ],

        evidence_style=(
            "Frequently uses conceptual models "
            "and hypothetical examples."
        ),

        argument_style=[
            "Structured",
            "Principle-based"
        ],

        common_assumptions=[
            "Assumes economic incentives drive behavior."
        ],

        fallacy_tendencies=[],

        reasoning_strengths=[
            "Systematic reasoning",
            "Conceptual clarity"
        ],

        reasoning_weaknesses=[
            "Weak empirical grounding"
        ],

        overall_reasoning_score=9.0,

        profile_summary=(
            "A systematic thinker who favors theoretical reasoning."
        )
    )
]


print("\nAnalyzing 3 debate fingerprints...\n")


profile = ReasoningProfileService.build_profile(
    fingerprints
)


print("\n========== USER REASONING PROFILE ==========\n")

print(profile)


print("\n✅ Reasoning Profile Service works!")