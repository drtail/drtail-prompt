from typing import List, Optional
from pydantic import BaseModel, Field


class Author(BaseModel):
    name: str
    email: str


class Metadata(BaseModel):
    role: str
    domain: str
    action: str


class Output(BaseModel):
    type: str
    model: Optional[str] = Field(default=None)
    schema_: Optional[dict] = Field(default=None, alias="schema")


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
    output: Output
    messages: List[Message]

    class Config:
        from_attributes = True
