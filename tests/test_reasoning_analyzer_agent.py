from schemas.reflection import ReflectionResult
from graph.state import DebateState
from graph.enums import DebatePhase
from agents.reasoning_analyzer import ReasoningAnalyzerAgent

print("Testing Reasoning Analyzer Agent...")

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


state = DebateState(
    topic="Should AI replace software engineers?",
    user_stance="Support",
    ai_stance="Oppose",
    current_phase=DebatePhase.OPENING,
)


state.metadata["reflection"] = reflection


agent = ReasoningAnalyzerAgent()


print("\nRunning agent...\n")


state = agent.run(state)


print("\n========== REASONING FINGERPRINT ==========\n")

print(state.metadata["reasoning_fingerprint"])


print("\n✅ Reasoning Analyzer Agent works!")