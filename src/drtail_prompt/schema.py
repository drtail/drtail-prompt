from typing import Any, Optional
from typing_extensions import Self


from pydantic import BaseModel, Field, model_validator

from drtail_prompt.exception import PromptVersionMismatchError

SCHEMA_MAX_VERSION = "1.0.0"


class Author(BaseModel):
    name: str
    email: str


class Metadata(BaseModel):
    role: str
    domain: str
    action: str


class IOBase(BaseModel):
    type: str
    model: Optional[str] = Field(default=None)
    schema_: Optional[dict] = Field(default=None, alias="schema")

    instance: Optional[BaseModel] = Field(init=False, default=None)

    def post_init(self, __context: Any) -> None:
        if not self.model or self.type != "pydantic":
            return

        module_path, class_name = self.model.rsplit(".", 1)

        module = __import__(module_path, fromlist=[class_name])
        input_model_pydantic: BaseModel = getattr(module, class_name)

        self.set_instance(input_model_pydantic)

    def set_instance(self, instance: BaseModel) -> None:
        self.instance = instance

    def instance_validate(self, data: dict[str, Any]) -> BaseModel:
        if self.instance is None:
            raise ValueError("Instance is not set")
        return self.instance.model_validate(data)

    @model_validator(mode="after")
    def validate_instance(self) -> Self:
        if not self.model and not self.schema_:
            raise ValueError("Model or schema is not set")

        if not self.type == "pydantic":
            raise NotImplementedError("Only pydantic is supported for now")

        if not self.model:
            raise NotImplementedError("Schema is not supported for now")

        module_path, class_name = self.model.rsplit(".", 1)

        module = __import__(module_path, fromlist=[class_name])
        input_model_pydantic: BaseModel = getattr(module, class_name)

        if self.instance is None:
            self.set_instance(input_model_pydantic)

        return self


class Input(IOBase): ...


class Output(IOBase): ...


class Message(BaseModel):
    role: str
    content: str


def _nested_format(template: str, data_dict: dict[str, Any]) -> str:
    import re

    placeholders = re.findall(r"\{([^{}]+)\}", template)
    result = template

    for placeholder in placeholders:
        keys = placeholder.split(".")
        value = data_dict
        try:
            for key in keys:
                value = value[key]
            result = result.replace(f"{{{placeholder}}}", str(value))
        except (KeyError, TypeError):
            pass

    return result


class BasicPromptSchema(BaseModel):
    api: str
    version: str
    name: str
    description: str
    authors: list[Author]
    metadata: Metadata
    input: Optional[Input] = Field(default=None)
    output: Optional[Output] = Field(default=None)
    messages: list[Message]

    class Config:
        from_attributes = True

    def interpolate(self, data: dict[str, Any]) -> "BasicPromptSchema":
        for message in self.messages:
            # TODO: use jinja2 to interpolate the message content
            message.content = message.content.replace("{{", "{").replace("}}", "}")
            # Handle nested dictionary access in template variables
            message.content = _nested_format(message.content, data)
        return self

    @model_validator(mode="before")
    def validate_version(cls, data):
        if data.get("version") != SCHEMA_MAX_VERSION:
            raise PromptVersionMismatchError(
                f"version must be less than or equal to {SCHEMA_MAX_VERSION}, got {data.get('version')}"
            )
        return data
