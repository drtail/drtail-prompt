from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ValidationError

from drtail_prompt.exception import PromptValidationError
from drtail_prompt.schema import BasicPromptSchema, Message


def slugify_name(name: str) -> str:
    return name.lower().replace(" ", "-")


class Prompt(BaseModel):
    data: BasicPromptSchema

    # TODO: define public methods
    ...

    @property
    def messages(self) -> list[Message]:
        return self.data.messages

    @property
    def messages_dict(self) -> list[dict[str, str]]:
        return [message.model_dump() for message in self.messages]

    @property
    def metadata(self) -> dict[str, str]:
        _metadata: dict[str, str] = {}
        _metadata["name"] = slugify_name(self.data.name)
        _metadata["version"] = self.data.version
        if self.data.authors:
            _metadata["last_modified_by"] = self.data.authors[-1].email

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


def load_prompt(path: str, inputs: dict[str, Any] | BaseModel | None = None) -> Prompt:
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
            raise PromptValidationError("Input schema is not defined in the prompt")

        if isinstance(inputs, BaseModel):
            prompt_input_instance = prompt.input.instance
            if not prompt_input_instance:
                raise PromptValidationError("Input model is not defined in the prompt")
            if inputs.model_json_schema() != prompt_input_instance.model_json_schema():
                raise PromptValidationError(
                    "Input model is not the same as the model defined in the prompt",
                )
            inputs = inputs.model_dump()

        try:
            validated_inputs = prompt.input.instance_validate(inputs)
        except ValidationError as e:
            raise PromptValidationError(e) from e

        prompt.interpolate(validated_inputs.model_dump())

    return Prompt(data=prompt)
