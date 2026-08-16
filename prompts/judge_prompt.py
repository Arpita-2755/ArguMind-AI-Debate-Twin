from schemas.debate_transcript import DebateTranscript


def build_judge_prompt(transcript: DebateTranscript):

    return f"""
You are an expert international debate judge.

Your task is to evaluate the debate objectively.

TOPIC:
{transcript.topic}

DEBATE PLAN:
{transcript.debate_plan.model_dump_json(indent=2)}

DEBATE TRANSCRIPT:
{transcript.model_dump_json(indent=2)}

Evaluate the arguments based on:

1. Logic
2. Evidence
3. Clarity
4. Persuasiveness

SCORING RULES:

- Every score must be between 0 and 10.
- Decimals are allowed.
- Never use percentages.
- Judge the quality of the arguments, not which position you personally agree with.
- Do not favor the AI or the human automatically.
- Consider both sides fairly.
- Identify concrete strengths and weaknesses.

Return ONLY valid JSON.

Do not include markdown.
Do not include code fences.
Do not include explanations outside the JSON.

The response must start with '{{' and end with '}}'.

JSON FORMAT:

{{
    "winner": "User or Opponent",
    "logic_score": 0.0,
    "evidence_score": 0.0,
    "clarity_score": 0.0,
    "persuasion_score": 0.0,
    "strengths": [],
    "weaknesses": [],
    "summary": ""
}}
"""