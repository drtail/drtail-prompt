import pytest
import yaml
from prompt.exception import PromptValidationError
from prompt.schema import BasicPromptSchema


@pytest.mark.parametrize("prompt_path", ["basic.yaml", "basic_2.yaml"])
def test_prompt_schema(prompt_path: str):
    with open(f"tests/prompt/data/{prompt_path}", "r") as file:
        yaml_data = yaml.safe_load(file)
        prompt = BasicPromptSchema(**yaml_data)

    assert prompt.api == "drtail/prompt"
    assert prompt.version == "1.0.0"
    assert prompt.name == "Basic Prompt"
    assert prompt.description == "A basic prompt for DrTail"
    assert prompt.authors[0].model_dump() == {
        "name": "Humphrey Ahn",
        "email": "ahnsv@bc.edu",
    }
    assert prompt.metadata.model_dump() == {
        "role": "todo",
        "domain": "consultation",
        "action": "extract",
    }


def test_prompt_validation_error():
    with open("tests/prompt/data/basic_error_1.yaml", "r") as file:
        yaml_data = yaml.safe_load(file)
        with pytest.raises(PromptValidationError) as exc:
            BasicPromptSchema(**yaml_data)
        assert "model" in str(exc.value)
