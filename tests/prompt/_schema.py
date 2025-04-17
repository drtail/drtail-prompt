from pydantic import BaseModel


class BasicPromptInput(BaseModel):
    location: str
    capital: str
