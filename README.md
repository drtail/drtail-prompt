# Dr.Tail Prompt

A scalable and manageable prompt format for AI model interactions.

## Features

- **Prompt Versioning**: Track and manage different versions of your prompts
- **Metadata Management**: Store and organize prompt metadata efficiently
- **Input/Output Validation**: Robust validation using Pydantic models
- **Multi-Provider Support**: Seamless integration with various AI model providers
- **Type Safety**: Full type hints and validation for better development experience

## Installation

```bash
# Using pip
pip install drtail-prompt

# Using poetry
poetry add drtail-prompt

# Using uv
uv add drtail-prompt

# Using github url
pip install -e git@github.com:drtail/drtail-prompt.git@1.0.0
# or
pipenv install -e git@github.com:drtail/drtail-prompt.git@1.0.0
# or
poetry add -e git@github.com:drtail/drtail-prompt.git@1.0.0
```

## Quick Start

### Basic Usage

1. Define prompt in a predefined file format
```yaml
api: drtail/prompt
version: 1.0.0

name: Basic Prompt
description: A basic prompt for DrTail
authors:
  - name: Your Name
    email: your.email@example.com
metadata:
  role: todo
  domain: consultation
  action: extract
input:
  type: pydantic
  model: path.to.your.schema.InputModel
output:
  type: pydantic
  model: path.to.your.schema.OutputModel

messages:
  - role: developer
    content: |
      You are a helpful assistant that extracts information from a conversation.
      The capital of {{location}} is {{capital}}.
  - role: user
    content: What is the capital of the moon?
```

## Prompt YAML Schema

The following table describes all available fields in the prompt YAML schema:

| Field | Description | Default | Options |
|-------|-------------|---------|---------|
| `api` | API identifier for the prompt format | Required | `drtail/prompt` |
| `version` | Schema version | Required | `1.0.0` |
| `name` | Name of the prompt | Required | Any string |
| `description` | Description of the prompt | `""` | Any string |
| `authors` | List of prompt authors | Required | Array of author objects with `name` and `email` |
| `metadata` | Additional metadata for the prompt | `{}` | Any key-value pairs |
| `input` | Input schema definition | Optional | Object with `type` and `model` |
| `output` | Output schema definition | Optional | Object with `type` and `model` |
| `(input,output).type` | Type of input schema | `"pydantic"` | `pydantic` (only at this moment) |
| `(input,output).model` | Path to input schema model | Required if `input` is defined | Valid Python import path |
| `messages` | List of messages in the prompt | Required | Array of message objects |
| `messages[].role` | Role of the message | Required | `system`, `user`, `assistant`, `developer` |
| `messages[].content` | Content of the message | Required | Any string, can include `{{variable}}` placeholders |



2. Use the prompt with your favorite ai toolings
```python
from drtail_prompt import load_prompt

# Load a prompt from YAML file
prompt = load_prompt("path/to/prompt.yaml")

# Use the prompt with input variables
response = client.responses.create(
    model="gpt-4.1",
    input=prompt.messages,
    metadata=prompt.metadata,
)

# use with
chat_completion_response = client.chat.completions.create(
    model="gpt-4.1",
    messages=prompt.messages,
    metadata=prompt.metadata,
)

```


### Output Validation

Define your output schema using Pydantic:

```python
from pydantic import BaseModel

class BasicPromptInput(BaseModel):
    location: str
    capital: str

class BasicPromptOutput(BaseModel):
    text: str
```

```python
from drtail_prompt import load_prompt, PromptValidationError

def main():
    try:
        # Load prompt with input validation
        prompt = load_prompt(
            "path/to/prompt.yaml",
            input_variables={"location": "moon", "capital": "moon"}
        )
    except PromptValidationError as e:
        print(f"Validation error: {e}")

    # Use with your preferred AI provider
    response = client.responses.create(
        model="gpt-4.1",
        input=prompt.messages,
        metadata=prompt.metadata,
        text=prompt.structured_output_format # structured output
    )

```

<!-- ## Documentation

For detailed documentation, please visit [documentation link]. -->

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## Development

For development setup and guidelines, please refer to our [Development Guide](DEVELOPMENT.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) to understand our community guidelines.

<!-- ## Support

If you encounter any issues or have questions, please:
1. Check the [issue tracker](https://github.com/yourusername/dr-tail-prompt/issues)
2. Join our [community chat](https://github.com/yourusername/dr-tail-prompt/discussions)

## Authors

- Your Name - Initial work - [YourGitHub](https://github.com/yourusername) -->

## Acknowledgments

- Thanks to all contributors who have helped shape this project
- Special thanks to the open-source community for inspiration and tools
