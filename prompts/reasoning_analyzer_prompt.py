from schemas.reflection import ReflectionResult


def build_reasoning_analyzer_prompt(
    reflection: ReflectionResult
):
    return f"""
You are an expert cognitive reasoning analyst.

Your task is to convert a debate reflection into a structured
reasoning fingerprint of the USER.

The reflection describes one debate.

Your job is NOT to judge the debate again.

Your job is to identify the user's underlying reasoning style,
patterns, tendencies, strengths, and weaknesses that can be
useful for analyzing the user in future debates.

REFLECTION:
{reflection.model_dump_json(indent=2)}

Analyze the user's reasoning across the following dimensions:

1. REASONING STYLE

Identify the broad characteristics of how the user tends to reason.

Examples:
- analytical
- systematic
- intuitive
- empirical
- theoretical
- causal
- quantitative
- conceptual
- first-principles

Only include characteristics supported by the reflection.

2. STRONGEST REASONING PATTERNS

Identify the reasoning patterns that appear to be the user's
strongest.

Do not simply copy the reflection.

Generalize the pattern into a reusable description.

For example:

Weak:
"Used causal reasoning."

Better:
"Frequently constructs arguments by linking economic incentives
to predicted behavioral outcomes."

3. WEAKEST REASONING PATTERNS

Identify reasoning approaches that appear less developed
or less frequently used.

Do not interpret absence as weakness unless the reflection
provides enough evidence.

4. EVIDENCE STYLE

Describe how the user tends to use evidence.

Consider:
- empirical evidence
- statistics
- examples
- hypothetical scenarios
- deductive reasoning
- external sources
- conceptual reasoning

5. ARGUMENT STYLE

Identify how the user typically constructs and presents
arguments.

Examples:
- structured
- direct
- counterargument-driven
- concession-based
- analogy-driven
- principle-based
- quantitative
- adversarial
- exploratory

6. COMMON ASSUMPTIONS

Identify assumptions that appear important to the user's
reasoning.

Only include assumptions supported by the reflection.

Phrase them as reusable observations rather than debate-specific
statements whenever possible.

7. FALLACY TENDENCIES

Identify logical fallacies that appear to be recurring tendencies.

IMPORTANT:

A fallacy should NOT be inferred merely because the user
made one debatable claim.

If there is insufficient evidence of a recurring tendency,
return an empty list.

8. REASONING STRENGTHS

Identify broader strengths that could remain useful across
different debates.

9. REASONING WEAKNESSES

Identify broader weaknesses that could potentially appear
again in future debates.

10. OVERALL REASONING SCORE

Provide a score between 0 and 10.

This score should represent the quality of the user's reasoning
based on the reflection.

11. PROFILE SUMMARY

Write a concise description of the user's reasoning style.

The summary should sound like a persistent user profile,
not a summary of this particular debate.

IMPORTANT RULES:

- Analyze the USER only.
- Do not analyze the opponent.
- Do not determine the debate winner.
- Do not repeat the judge's evaluation.
- Do not invent information.
- Do not infer personality traits.
- Do not confuse communication style with reasoning ability.
- Do not treat a single example as a permanent behavioral trait
  unless the reflection provides sufficient evidence.
- Prefer cautious, evidence-based generalizations.
- The output should be useful for analyzing the user's future
  debates.
- Distinguish between observations from this debate and
  potentially recurring reasoning tendencies.

Return ONLY valid JSON.

Do not include markdown.
Do not include code fences.
Do not include explanations outside the JSON.

JSON FORMAT:

{{
    "reasoning_style": [],
    "strongest_reasoning_patterns": [],
    "weakest_reasoning_patterns": [],
    "evidence_style": "",
    "argument_style": [],
    "common_assumptions": [],
    "fallacy_tendencies": [],
    "reasoning_strengths": [],
    "reasoning_weaknesses": [],
    "overall_reasoning_score": 0.0,
    "profile_summary": ""
}}
"""