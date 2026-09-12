from schemas.reasoning_fingerprint import ReasoningFingerprint

print("Testing ReasoningFingerprint schema...")

result = ReasoningFingerprint(
    reasoning_style=["Analytical", "Causal"],
    strongest_reasoning_patterns=["Causal reasoning"],
    weakest_reasoning_patterns=["Evidence-based reasoning"],
    evidence_style="Mostly hypothetical reasoning",
    argument_style=["Structured", "Counterargument-driven"],
    common_assumptions=["Assumes AI productivity gains reduce labor demand"],
    fallacy_tendencies=[],
    reasoning_strengths=["Logical structure"],
    reasoning_weaknesses=["Limited empirical evidence"],
    overall_reasoning_score=8.5,
    profile_summary="The user tends to use structured causal reasoning."
)

print(result)

print("\n✅ ReasoningFingerprint schema works!")