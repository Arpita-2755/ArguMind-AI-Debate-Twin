from schemas.reasoning_profile import UserReasoningProfile


print("Testing UserReasoningProfile schema...")


profile = UserReasoningProfile(
    reasoning_style=[
        "Analytical",
        "Causal",
        "Theoretical"
    ],

    strongest_reasoning_patterns=[
        "Assumption testing",
        "Counterargument",
        "Causal reasoning"
    ],

    weakest_reasoning_patterns=[
        "Empirical reasoning",
        "Technical evidence"
    ],

    evidence_style=(
        "Primarily deductive and hypothetical, "
        "with limited empirical evidence."
    ),

    argument_style=[
        "Structured",
        "Counterargument-driven",
        "Principle-based"
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

    debates_analyzed=1,

    profile_summary=(
        "A structured and analytical thinker who "
        "primarily uses causal and theoretical reasoning."
    )
)


print(profile)

print("\n✅ UserReasoningProfile schema works!")