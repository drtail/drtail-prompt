import yaml
from pydantic import ValidationError

from prompt.exception import PromptValidationError
from prompt.schema import BasicPromptSchema


def load_prompt(path: str) -> BasicPromptSchema:
    with open(path, "r") as file:
        yaml_data = yaml.safe_load(file)
        try:
            return BasicPromptSchema.model_validate(yaml_data)
        except ValidationError as e:
            raise PromptValidationError(e) from e
