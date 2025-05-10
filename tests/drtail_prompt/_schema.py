from typing import Optional

from pydantic import BaseModel


class BasicPromptInput(BaseModel):
    location: str
    capital: str


class BasicPromptOutput(BaseModel):
    location: str
    capital: str


class NestedPromptInput(BaseModel):
    location: str
    capital: str
    number: int
    optional_field: Optional[str] = None


class NestedNestedInnerPromptInput(BaseModel):
    location: str
    capital: str


class NestedNestedPromptInput(BaseModel):
    inner: NestedNestedInnerPromptInput


class AdvancedPromptInput(BaseModel):
    nested: NestedPromptInput
    nested_nested: NestedNestedPromptInput


class AdvancedPromptInput2(BaseModel):
    nested: NestedPromptInput


class ComplexField(BaseModel):
    name: str
    value: str


class Level4Field(BaseModel):
    detail: str


class Level3Field(BaseModel):
    level4: Level4Field


class Level2Field(BaseModel):
    level3: Level3Field


class AdvancedPromptOutput(BaseModel):
    content: str
    level1: Level2Field
