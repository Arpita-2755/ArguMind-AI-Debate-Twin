from schemas.reflection import ReflectionResult
from services.reasoning_analyzer_service import ReasoningAnalyzerService


print("Testing Reasoning Analyzer Service...")

reflection = ReflectionResult(
    reasoning_patterns=[
        "economic reasoning",
        "causal reasoning",
        "counterargument",
        "assumption testing",
        "analogy",
        "conceptual clarification"
    ],
    strengths=[
        "Exemplary logical partitioning in Round 3",
        "Effective disruption of historical analogies",
        "Strong structural cohesion"
    ],
    weaknesses=[
        "Avoided addressing concrete technical counter-points",
        "Relied heavily on abstract economic theories"
    ],
    assumptions=[
        "Assumes AI coding capabilities will become sufficiently reliable",
        "Assumes increased software demand will not fully offset labor reduction"
    ],
    fallacies=[],
    evidence_usage=(
        "The user relied almost exclusively on deductive logical reasoning, "
        "hypothetical scenarios, and conceptual analogies rather than "
        "empirical evidence."
    ),
    overall_reasoning_quality=9.2,
    summary=(
        "The user demonstrated highly rigorous and logically disciplined "
        "reasoning, particularly through economic reasoning and assumption testing."
    )
)

print("\nRunning analyzer...\n")

result = ReasoningAnalyzerService.analyze(reflection)

print("========== REASONING FINGERPRINT ==========\n")
print(result)

print("\n✅ Reasoning Analyzer Service works!")