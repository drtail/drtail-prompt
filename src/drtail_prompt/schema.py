from typing import Any, Optional

from jinja2 import Template
from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Self


class Author(BaseModel):
    name: str
    email: str


class Metadata(BaseModel):
    role: Optional[str] = Field(default=None)
    domain: Optional[str] = Field(default=None)
    action: Optional[str] = Field(default=None)

    model_config = ConfigDict(extra="allow")


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


def is_valid_semver(version: str) -> bool:
    try:
        parts = version.split(".")
        if len(parts) < 2 or len(parts) > 3:
            return False

        for part in parts:
            if "+" in part:
                part = part.split("+")[0]
            if "-" in part:
                part = part.split("-")[0]

            if not part.isdigit() or int(part) < 0:
                return False

        return True
    except Exception:
        return False


class BasicPromptSchema(BaseModel):
    api: str = Field(
        default="drtail/prompt@v1",
        description="Schema API. Should be fixed to drtail/prompt@v1 for backward compatibility.",
    )
    version: str = Field(
        default="1.0.0",
        description="Prompt version. Should be a valid semantic version. This will appear in the tag of the prompt.",
    )
    name: str = Field(
        description="Name of the prompt. Intended to be used as a unique identifier. This will appear in the tag of the prompt.",
    )
    description: str = Field(
        description="Description of the prompt. Should be concise and to the point.",
    )
    authors: list[Author] = Field(
        description="Authors of the prompt. Include all authors who have contributed to the prompt.",
    )
    metadata: Metadata = Field(
        description="Metadata of the prompt. Recommend to include role, domain, and action. Feel free to add more fields as needed.",
    )
    input: Optional[Input] = Field(
        default=None,
        description="Input of the prompt. If the prompt does not require input, set it to None.",
    )
    output: Optional[Output] = Field(
        default=None,
        description="Output of the prompt. If the prompt does not require output, set it to None.",
    )
    messages: list[Message] = Field(description="Messages of the prompt.")

    class Config:
        from_attributes = True

    def interpolate(self, data: dict[str, Any]) -> "BasicPromptSchema":
        for message in self.messages:
            template = Template(message.content)
            message.content = template.render(**data)
        return self

    @model_validator(mode="before")
    def validate_version(cls, data: dict[str, Any]) -> dict[str, Any]:
        version = data.get("version")
        if not version:
            raise ValueError("Version is required")
        if not is_valid_semver(version):
            raise ValueError("Invalid version")
        return data

    @model_validator(mode="before")
    def validate_api(cls, data: dict[str, Any]) -> dict[str, Any]:
        try:
            api = data["api"]
            api_name, api_version = api.split("@")
        except KeyError as e:
            raise ValueError("API is required") from e
        except ValueError as e:
            raise ValueError(
                "Invalid API format. Should be like drtail/prompt@v1",
            ) from e

        if api_name != "drtail/prompt":
            raise ValueError("Invalid API name. Should be drtail/prompt")

        if api_version != "v1":
            raise NotImplementedError("Only v1 is supported for now")

        return data
