import pytest
import yaml
from prompt.core import load_prompt
from prompt.exception import PromptValidationError, PromptVersionMismatchError
from prompt.schema import BasicPromptSchema, Message


@pytest.mark.parametrize(
    "prompt_path", ["basic_1.yaml", "basic_2.yaml", "basic_3.yaml"]
)
def test_prompt_schema(prompt_path: str):
    prompt = load_prompt(f"tests/prompt/data/{prompt_path}")

    assert prompt.data.api == "drtail/prompt"
    assert prompt.data.version == "1.0.0"
    assert prompt.data.name == "Basic Prompt"
    assert prompt.data.description == "A basic prompt for DrTail"
    assert prompt.data.authors[0].model_dump() == {
        "name": "Humphrey Ahn",
        "email": "ahnsv@bc.edu",
    }
    assert prompt.data.metadata.model_dump() == {
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


def test_prompt_input_interpolation():
    prompt = load_prompt(
        "tests/prompt/data/basic_3.yaml", {"location": "moon", "capital": "moon"}
    )
    assert (
        prompt.messages[0].content.strip()
        == "You are a helpful assistant that extracts information from a conversation.\nThe capital of moon is moon."
    )


def test_prompt_input_model_not_found():
    with pytest.raises(PromptValidationError) as exc:
        load_prompt("tests/prompt/data/invalid_model_path.yaml", {"location": "moon"})
    assert "Module" in str(exc.value)
    assert "not found" in str(exc.value)


def test_prompt_input_validation_error():
    with pytest.raises(PromptValidationError) as exc:
        load_prompt("tests/prompt/data/basic_3.yaml", {"location": "moon"})
    assert "capital" in str(exc.value)


def test_prompt_get_messages():
    prompt = load_prompt("tests/prompt/data/basic_1.yaml")
    assert prompt.messages == [
        Message(
            role="developer",
            content="You are a helpful assistant that extracts information from a conversation. The capital of {{location}} is {{capital}}.",
        ),
        Message(role="user", content="What is the capital of the moon?"),
    ]
