from typing import List, Optional
from pydantic import BaseModel, Field, model_validator

from prompt.exception import PromptVersionMismatchError

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


class Input(IOBase):
    pass


class Output(IOBase):
    pass


class Message(BaseModel):
    role: str
    content: str


class BasicPromptSchema(BaseModel):
    api: str
    version: str
    name: str
    description: str
    authors: List[Author]
    metadata: Metadata
    input: Optional[Input] = Field(default=None)
    output: Optional[Output] = Field(default=None)
    messages: List[Message]

    class Config:
        from_attributes = True

    @model_validator(mode="before")
    def validate_version(cls, data):
        if data.get("version") != SCHEMA_MAX_VERSION:
            raise PromptVersionMismatchError(
                f"version must be less than or equal to {SCHEMA_MAX_VERSION}, got {data.get('version')}"
            )
        return data
