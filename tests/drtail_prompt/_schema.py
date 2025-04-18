from pydantic import BaseModel


class BasicPromptInput(BaseModel):
    location: str
    capital: str


class BasicPromptOutput(BaseModel):
    location: str
    capital: str
