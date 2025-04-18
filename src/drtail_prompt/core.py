from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ValidationError

from drtail_prompt.exception import PromptValidationError
from drtail_prompt.schema import BasicPromptSchema, Message


class Prompt(BaseModel):
    data: BasicPromptSchema

    # TODO: define public methods
    ...

    @property
    def messages(self) -> list[Message]:
        return self.data.messages

    @property
    def metadata(self) -> dict[str, str]:
        _metadata: dict[str, str] = {}
        _metadata["name"] = self.data.name
        if self.data.metadata:
            _metadata.update(self.data.metadata.model_dump())

        return _metadata

    @property
    def structured_output_format(self) -> dict[str, Any]:
        """
        Returns the structured output format for the prompt.
        See https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses&example=structured-data#how-to-use
        """
        if not self.data.output:
            return {}

        if not self.data.output.instance:
            raise PromptValidationError("Output instance is not set")

        schema = self.data.output.instance.model_json_schema()
        return {
            "format": {
                "type": "json_schema",
                "name": schema["title"],
                "schema": schema,
            },
        }


def load_prompt(path: str, inputs: dict[str, Any] | None = None) -> Prompt:
    filepath = Path(path)
    with open(filepath) as file:
        yaml_data = yaml.safe_load(file)
        try:
            prompt = BasicPromptSchema.model_validate(yaml_data)
        except ValidationError as e:
            raise PromptValidationError(e) from e
        except ModuleNotFoundError as e:
            raise PromptValidationError(e) from e

    if inputs:
        if not prompt.input:
            raise PromptValidationError("Input is not defined in the prompt")

        try:
            validated_inputs = prompt.input.instance_validate(inputs)
        except ValidationError as e:
            raise PromptValidationError(e) from e

        prompt.interpolate(validated_inputs.model_dump())

    return Prompt(data=prompt)
