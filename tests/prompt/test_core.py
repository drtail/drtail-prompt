import pytest
import yaml
from prompt.core import load_prompt
from prompt.exception import PromptValidationError, PromptVersionMismatchError
from prompt.schema import BasicPromptSchema


@pytest.mark.parametrize(
    "prompt_path", ["basic_1.yaml", "basic_2.yaml", "basic_3.yaml"]
)
def test_prompt_schema(prompt_path: str):
    prompt = load_prompt(f"tests/prompt/data/{prompt_path}")

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


def test_prompt_version_mismatch_error():
    with pytest.raises(PromptVersionMismatchError) as exc:
        load_prompt("tests/prompt/data/basic_newer_version.yaml")
    assert "version" in str(exc.value)


def test_prompt_output_validation_error():
    assert False


def test_prompt_input_validation_error():
    assert False
