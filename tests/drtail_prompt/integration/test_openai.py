from unittest.mock import Mock, patch
import pytest

from drtail_prompt.core import load_prompt


@pytest.fixture
def mock_openai_client():
    with patch("openai.OpenAI") as mock_client:
        # Create a mock response object
        mock_response = Mock()
        mock_response.id = "mock-response-id"
        mock_response.model = "gpt-3.5-turbo"

        # Configure the mock client to return our mock response
        mock_instance = mock_client.return_value
        mock_instance.responses.create.return_value = mock_response

        yield mock_instance


def test_prompt_should_provide_enough_parameters_for_response_api(mock_openai_client):
    prompt = load_prompt("tests/drtail_prompt/data/basic_1.yaml")
    assert prompt is not None

    response = mock_openai_client.responses.create(
        model="gpt-3.5-turbo",
        input=prompt.messages,
        metadata=prompt.metadata,
    )
    assert response is not None
    assert response.id == "mock-response-id"
    assert response.model == "gpt-3.5-turbo"

    # Verify the API was called with correct parameters
    mock_openai_client.responses.create.assert_called_once_with(
        model="gpt-3.5-turbo",
        input=prompt.messages,
        metadata=prompt.metadata,
    )
    for message in prompt.messages:
        assert message.role in ["user", "assistant", "developer", "system"]
        assert message.content is not None

    assert prompt.metadata is not None
    assert prompt.metadata["name"] == "Basic Prompt"
    assert prompt.metadata["authors"] is not None
    assert prompt.metadata["role"] == "todo"
    assert prompt.metadata["domain"] == "consultation"
    assert prompt.metadata["action"] == "extract"


def test_prompt_should_provide_enough_parameters_for_chat_completion_api(
    mock_openai_client,
):
    prompt = load_prompt("tests/drtail_prompt/data/basic_1.yaml")
    assert prompt is not None

    response = mock_openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt.messages,
        metadata=prompt.metadata,
    )
    assert response is not None

    assert prompt.metadata is not None
    assert prompt.metadata["name"] == "Basic Prompt"
    assert prompt.metadata["authors"] is not None
    assert prompt.metadata["role"] == "todo"
    assert prompt.metadata["domain"] == "consultation"
    assert prompt.metadata["action"] == "extract"


def test_prompt_output_should_be_used_as_text_structured_output(mock_openai_client):
    prompt = load_prompt("tests/drtail_prompt/data/basic_1.yaml")
    assert prompt is not None

    response = mock_openai_client.responses.create(
        model="gpt-3.5-turbo",
        input=prompt.messages,
        metadata=prompt.metadata,
        text=prompt.structured_output_format,
    )
    assert response is not None
    assert response.text is not None
