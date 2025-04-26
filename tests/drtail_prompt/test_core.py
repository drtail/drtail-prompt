import pytest

from drtail_prompt.core import load_prompt
from drtail_prompt.exception import PromptValidationError


@pytest.mark.parametrize(
    "prompt_path",
    ["basic_1.yaml", "basic_2.yaml", "basic_3.yaml"],
)
def test_prompt_schema(prompt_path: str):
    prompt = load_prompt(f"tests/drtail_prompt/data/{prompt_path}")

    assert prompt.data.api == "drtail/prompt@v1"
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
    with pytest.raises(PromptValidationError) as exc:
        load_prompt("tests/drtail_prompt/data/basic_error_1.yaml")
        assert "model" in str(exc.value)


def test_prompt_version_validation_error():
    with pytest.raises(PromptValidationError) as exc:
        load_prompt("tests/drtail_prompt/data/basic_error_version.yaml")
    assert "version" in str(exc.value)


def test_prompt_has_empty_authors_should_have_no_last_modified_by():
    prompt = load_prompt("tests/drtail_prompt/data/basic_error_authors.yaml")
    assert prompt.metadata.get("last_modified_by") is None


@pytest.mark.parametrize(
    "prompt_path",
    ["basic_error_1.yaml", "invalid_model_path.yaml"],
)
def test_prompt_output_validation_error(prompt_path: str):
    with pytest.raises(PromptValidationError) as exc:
        load_prompt(f"tests/drtail_prompt/data/{prompt_path}")
    assert "No module named" in str(exc.value)


def test_prompt_input_interpolation():
    prompt = load_prompt(
        "tests/drtail_prompt/data/basic_3.yaml",
        {"location": "moon", "capital": "moon"},
    )
    assert (
        prompt.messages[0].content.strip()
        == "You are a helpful assistant that extracts information from a conversation.\nThe capital of moon is moon."
    )


def test_prompt_input_nested_interpolation():
    prompt = load_prompt(
        "tests/drtail_prompt/data/advanced.yaml",
        {
            "nested": {"location": "moon", "capital": "moon", "number": 1},
            "nested_nested": {"inner": {"location": "moon", "capital": "moon"}},
        },
    )
    assert (
        prompt.messages[0].content.strip()
        == "You are a helpful assistant that extracts information from a conversation.\nThe capital of moon is moon.\nThe number is moon and moon."
    )


def test_prompt_input_model_not_found():
    with pytest.raises(PromptValidationError) as exc:
        load_prompt(
            "tests/drtail_prompt/data/invalid_model_path.yaml",
            {"location": "moon"},
        )
    assert "No module" in str(exc.value)


def test_prompt_input_validation_error():
    with pytest.raises(PromptValidationError) as exc:
        load_prompt("tests/drtail_prompt/data/basic_3.yaml", {"location": "moon"})
    assert "capital" in str(exc.value)


def test_prompt_get_messages():
    prompt = load_prompt("tests/drtail_prompt/data/basic_1.yaml")
    assert (
        prompt.messages[0].content
        == "You are a helpful assistant that extracts information from a conversation.\nThe capital of {{location}} is {{capital}}.\n"
    )


def test_prompt_get_messages_dict():
    prompt = load_prompt("tests/drtail_prompt/data/basic_1.yaml")
    assert prompt.messages_dict == [
        {
            "role": "developer",
            "content": "You are a helpful assistant that extracts information from a conversation.\nThe capital of {{location}} is {{capital}}.\n",
        },
        {
            "role": "user",
            "content": "What is the capital of the moon?",
        },
    ]
