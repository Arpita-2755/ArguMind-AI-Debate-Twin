from schemas.debate_transcript import DebateTranscript
from schemas.judge_result import JudgeResult


def build_reflection_prompt(
    transcript: DebateTranscript,
    judge_result: JudgeResult
):

    return f"""
You are an expert reasoning analyst.

Your task is to reflect on the USER'S reasoning throughout the debate.

You are NOT the judge.

The judge has already evaluated who performed better.

Your task is to analyze HOW the user reasoned.

DEBATE TOPIC:
{transcript.topic}

DEBATE TRANSCRIPT:
{transcript.model_dump_json(indent=2)}

JUDGE RESULT:
{judge_result.model_dump_json(indent=2)}

Analyze the USER only.

Identify:

1. REASONING PATTERNS

Identify recurring reasoning approaches used by the user.

Examples:
- causal reasoning
- economic reasoning
- analogy
- first-principles reasoning
- consequence-based reasoning
- counterargument
- assumption testing
- generalization

Only include patterns that are actually visible in the transcript.

2. STRENGTHS

Identify the user's strongest reasoning behaviors.

3. WEAKNESSES

Identify weaknesses or limitations in the user's reasoning.

Do not criticize the user's conclusion simply because you disagree with it.

Focus on reasoning quality.

4. ASSUMPTIONS

Identify important assumptions underlying the user's arguments.

5. FALLACIES

Identify genuine logical fallacies if present.

Do not invent fallacies.

If no clear fallacies are present, return an empty list.

6. EVIDENCE USAGE

Describe how effectively the user used evidence.

Consider:
- empirical evidence
- examples
- statistics
- sources
- hypothetical reasoning

7. OVERALL REASONING QUALITY

Give a score between 0 and 10.

8. SUMMARY

Provide a concise assessment of the user's reasoning throughout the debate.

IMPORTANT RULES:

- Analyze only the user's reasoning.
- Do not evaluate the opponent.
- Do not simply repeat the judge's evaluation.
- Do not confuse confidence with reasoning quality.
- Do not invent facts that are not present in the transcript.
- Do not assume an argument is a fallacy merely because it is controversial.
- Base your analysis strictly on the transcript.
- Be specific.
- Be objective.

Return ONLY valid JSON.

Do not include markdown.
Do not include code fences.
Do not include explanations outside the JSON.

JSON FORMAT:

{{
    "reasoning_patterns": [],
    "strengths": [],
    "weaknesses": [],
    "assumptions": [],
    "fallacies": [],
    "evidence_usage": "",
    "overall_reasoning_quality": 0.0,
    "summary": ""
}}
"""