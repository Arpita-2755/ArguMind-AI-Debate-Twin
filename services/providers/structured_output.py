import json
from typing import Type

from pydantic import BaseModel, ValidationError

from services.llm_errors import LLMResponseError


def build_structured_prompt(
    prompt: str,
    schema: Type[BaseModel]
) -> str:
    """
    Append the JSON schema to the prompt, for providers
    whose native structured-output mode is unreliable.
    """

    json_schema = json.dumps(
        schema.model_json_schema()
    )

    return (
        f"{prompt}\n\n"
        "Respond with only a JSON object that matches "
        "this JSON schema. Do not add any text, markdown "
        "or code fences around it.\n"
        f"{json_schema}"
    )


def parse_structured(
    text: str,
    schema: Type[BaseModel],
    provider_name: str
):
    """
    Extract the JSON object from a response and validate
    it against the schema. Raises LLMResponseError so the
    router can fall back to the next provider.
    """

    if not text:
        raise LLMResponseError(
            f"{provider_name} returned an empty response."
        )

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end < start:
        raise LLMResponseError(
            f"{provider_name} response did not contain "
            "a JSON object."
        )

    try:

        data = json.loads(text[start:end + 1])

        return schema.model_validate(data)

    except (json.JSONDecodeError, ValidationError) as error:

        raise LLMResponseError(
            f"{provider_name} returned invalid "
            f"{schema.__name__} JSON: {error}"
        ) from error
