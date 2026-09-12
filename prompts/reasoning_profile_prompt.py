from schemas.reasoning_fingerprint import ReasoningFingerprint


def build_reasoning_profile_prompt(
    fingerprints: list[ReasoningFingerprint]
):
    fingerprints_json = "\n\n".join(
        f"DEBATE {i + 1}:\n{fingerprint.model_dump_json(indent=2)}"
        for i, fingerprint in enumerate(fingerprints)
    )

    return f"""
You are an expert cognitive reasoning analyst.

Your task is to build an evolving reasoning profile of a USER
based on reasoning fingerprints extracted from multiple debates.

You are NOT judging the debates.

You are NOT determining debate winners.

Your job is to identify patterns that appear consistently across
the user's reasoning over time.

NUMBER OF DEBATES:
{len(fingerprints)}

REASONING FINGERPRINTS:

{fingerprints_json}


ANALYSIS RULES:

1. REASONING STYLE

Identify broad reasoning characteristics that appear repeatedly.

Do not treat a characteristic observed in only one debate as a
stable trait unless there is strong evidence.

2. STRONGEST REASONING PATTERNS

Identify reasoning patterns that repeatedly appear to be strong.

Prioritize patterns supported across multiple debates.

3. WEAKEST REASONING PATTERNS

Identify weaknesses that appear repeatedly.

Do not treat a weakness from a single debate as permanent unless
there is supporting evidence.

4. EVIDENCE STYLE

Identify the user's general approach to evidence.

Determine whether they tend to rely on:
- empirical evidence
- statistics
- examples
- hypothetical reasoning
- deductive reasoning
- conceptual reasoning
- external sources

5. ARGUMENT STYLE

Identify recurring ways the user constructs arguments.

Examples:
- structured
- counterargument-driven
- analogy-driven
- principle-based
- quantitative
- concession-based

6. COMMON ASSUMPTIONS

Identify assumptions that repeatedly appear in the user's
reasoning.

Do not simply copy debate-specific assumptions.

Generalize them into reusable patterns when appropriate.

7. FALLACY TENDENCIES

Only identify fallacies that appear repeatedly or are strongly
supported by the available fingerprints.

A fallacy observed in only one debate should NOT automatically
become a profile trait.

If there is insufficient evidence, return an empty list.

8. REASONING STRENGTHS

Identify strengths that appear consistently across debates.

9. REASONING WEAKNESSES

Identify weaknesses that appear consistently across debates.

10. OVERALL REASONING SCORE

Provide a score between 0 and 10 representing the user's
overall reasoning quality across the analyzed debates.

11. PROFILE SUMMARY

Write a concise description of the user's overall reasoning style.

This should describe the USER as a persistent reasoning profile,
not summarize individual debates.


IMPORTANT:

- Analyze the USER only.
- Do not analyze opponents.
- Do not determine debate winners.
- Do not invent information.
- Do not infer personality traits.
- Do not assume a pattern is permanent without evidence.
- Give greater weight to patterns appearing across multiple
  fingerprints.
- Distinguish stable patterns from isolated observations.
- Prefer cautious generalizations.
- The profile should become more reliable as more debates are
  analyzed.


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
    "debates_analyzed": {len(fingerprints)},
    "profile_summary": ""
}}
"""