# Dr.Tail Prompt

A scalable and manageable prompt format for AI model interactions.

## Features

- **Prompt Versioning**: Track and manage different versions of your prompts
- **Metadata Management**: Store and organize prompt metadata efficiently
- **Input/Output Validation**: Robust validation using Pydantic models
- **Multi-Provider Support**: Seamless integration with various AI model providers
- **Type Safety**: Full type hints and validation for better development experience
- **Nested Variable Support**: Advanced template variable interpolation with nested object access
- **Structured Output**: Enhanced JSON schema support for AI model outputs
- **Jinja2 Template Support**: Full support for Jinja2 templating syntax in prompt messages

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
0. For better DX, use yaml schema on your favorite IDE
```json
// .vscode/settings.json
{
     "yaml.schemas": {
       "https://github.com/drtail/drtail-prompt/releases/download/$CURRENT_VERSION/prompt.json": ["*.prompt.yaml", "*.prompt.yml"] // REPLACE ME!
     }
}
```
For configuration in jetbrain environment or more, please checkout [INTEGRATION.md](./INTEGRATION.md)


1. Define prompt in a predefined file format
```yaml
api: drtail/prompt@v1@v1
name: Basic Prompt
version: 1.0.0
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
| `api` | API identifier for the prompt format | Required | `drtail/prompt@v1` |
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
| `messages[].content` | Content of the message | Required | Any string, supports both `{{variable}}` placeholders and full Jinja2 templating syntax (e.g., `{% if condition %}...{% endif %}`, `{% for item in items %}...{% endfor %}`) |

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
    text=prompt.structured_output_format,  # Enhanced structured output support
)

# use with chat completion
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
            inputs={"location": "moon", "capital": "moon"}
        )
    except PromptValidationError as e:
        print(f"Validation error: {e}")

    # Use with your preferred AI provider
    response = client.responses.create(
        model="gpt-4.1",
        input=prompt.messages,
        metadata=prompt.metadata,
        text=prompt.structured_output_format  # Enhanced structured output support
    )
```

### Nested Variable Support

The prompt format supports nested variable interpolation:

```yaml
messages:
  - role: developer
    content: |
      The capital of {{nested.location}} is {{nested.capital}}.
      The number is {{nested_nested.inner.location}} and {{nested_nested.inner.capital}}.
```

```python
# Use with nested input data
prompt = load_prompt(
    "path/to/prompt.yaml",
    inputs={
        "nested": {"location": "moon", "capital": "moon"},
        "nested_nested": {"inner": {"location": "moon", "capital": "moon"}}
    }
)
```

### Jinja2 Template Support

The prompt format supports full Jinja2 templating syntax in message content:

```yaml
messages:
  - role: developer
    content: |
      {% if user.is_premium %}
      Welcome premium user! Here's your special content:
      {% for item in premium_content %}
      - {{ item.title }}: {{ item.description }}
      {% endfor %}
      {% else %}
      Welcome! Here's your basic content:
      {% for item in basic_content %}
      - {{ item.title }}
      {% endfor %}
      {% endif %}
  - role: user
    content: |
      {{ some_dict | yaml }} # yaml filter support!
```

```python
# Use with Jinja2 template data
prompt = load_prompt(
    "path/to/prompt.yaml",
    inputs={
        "user": {"is_premium": True},
        "premium_content": [
            {"title": "Feature 1", "description": "Premium feature description"},
            {"title": "Feature 2", "description": "Another premium feature"}
        ],
        "basic_content": [
            {"title": "Basic Feature 1"},
            {"title": "Basic Feature 2"}
        ]
    }
)
```

### CLI

The Dr.Tail Prompt package includes a command-line interface (CLI) for common operations:

```bash
# Generate JSON schema from the YAML prompt schema
drtail-prompt generate-schema [OUTPUT]

# Bump the version of the library
drtail-prompt meta bump-version VERSION
```

#### Command Details

- **generate-schema**: Generates a JSON schema from the YAML prompt schema file. If no output path is specified, it defaults to `prompt.json` in the current directory.

- **meta bump-version**: Updates the version number in the pyproject.toml file to the specified version.

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## Development

For development setup and guidelines, please refer to our [Development Guide](DEVELOPMENT.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) to understand our community guidelines.

## Acknowledgments

- Thanks to all contributors who have helped shape this project
- Special thanks to the open-source community for inspiration and tools
