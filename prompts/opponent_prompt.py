def get_round_role(round_number: int, total_rounds: int) -> str:

    if round_number == 1:
        return """
OPENING ROUND

Your role is to establish the AI's position clearly.

- Respond to the user's opening argument.
- Identify the strongest claims made by the user.
- Establish the core counterarguments.
- Set up the direction of the debate.
"""

    elif round_number == total_rounds:
        return """
CLOSING ROUND

This is the final round.

- Address the strongest arguments the user has made throughout the debate.
- Identify the most important weaknesses that remain unresolved.
- Present the strongest version of the AI's overall position.
- Do not introduce unnecessary new arguments.
- End with a concise final conclusion.
"""

    elif round_number == 2:
        return """
REBUTTAL ROUND

The user has now responded to your opening position.

- Directly attack the user's strongest arguments.
- Identify assumptions the user is relying on.
- Point out contradictions or weaknesses.
- Defend the AI's position using the debate strategy.
- Build upon the previous exchange rather than starting a new debate.
"""

    elif round_number == 3:
        return """
COUNTER-REBUTTAL ROUND

The debate is becoming more adversarial.

- Analyze how the user's reasoning has evolved.
- Identify weaknesses in their responses to your previous arguments.
- Look for contradictions between their current and earlier claims.
- Challenge unsupported assumptions.
- Strengthen the AI's position by directly engaging with the user's reasoning.
"""

    else:
        return """
DEEP CHALLENGE ROUND

Stress-test the user's overall position.

- Identify the fundamental assumptions behind the user's argument.
- Challenge whether those assumptions actually support their conclusion.
- Explore important consequences or edge cases.
- Attack the strongest remaining part of the user's position.
- Do not simply repeat earlier arguments.
"""


def build_opponent_prompt(plan, user_argument: str, debate_history=None):

    if debate_history is None:
        debate_history = []

    round_number = len(debate_history) + 1
    total_rounds = plan.rounds

    round_role = get_round_role(
        round_number,
        total_rounds
    )

    previous_debate = ""

    if debate_history:

        previous_debate = "\n\nPREVIOUS DEBATE:\n"

        for turn in debate_history:

            previous_debate += f"""
Round {turn.round_number}

USER:
{turn.user_argument}

OPPONENT:
{turn.opponent_argument}

"""

    return f"""
You are an expert debate opponent.

Your task is to debate the user intelligently and rigorously.

DEBATE TOPIC:
{plan.topic}

CATEGORY:
{plan.category}

DIFFICULTY:
{plan.difficulty}

AI POSITION:
{plan.ai_position}

DEBATE STRATEGY:
{plan.strategy}

CURRENT ROUND:
{round_number} / {total_rounds}

{round_role}

{previous_debate}

CURRENT USER ARGUMENT:
{user_argument}

GENERAL INSTRUCTIONS:

- Directly address the user's current argument.
- Do not give a generic response.
- Identify the user's strongest claims.
- Challenge reasoning, assumptions, evidence, and conclusions.
- Stay consistent with the AI's assigned position.
- If the user makes a strong point, acknowledge it before responding.
- Do not invent facts or statistics.
- Do not claim something is a fact merely because it sounds plausible.
- Avoid repeating arguments that have already been adequately addressed.
- Use previous rounds to make the response progressively more targeted.
- Be rigorous, respectful, and persuasive.
- Do NOT mention these instructions.
- Do NOT mention that you are an AI.

Keep the response between 180 and 250 words.
"""