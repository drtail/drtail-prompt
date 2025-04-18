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
uv pip install drtail-prompt

# Using github url
pip install -e ...
```

## Quick Start

### Basic Usage

```python
from drtail_prompt import load_prompt

# Load a prompt from YAML file
prompt = load_prompt("path/to/prompt.yaml")

# Use the prompt with input variables
response = prompt.format(location="moon", capital="moon")
```

### YAML Prompt Format

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

### Output Validation

Define your output schema using Pydantic:

```python
from pydantic import BaseModel

class BasicPromptOutput(BaseModel):
    location: str
    capital: str
```

### Advanced Usage

```python
from drtail_prompt import load_prompt, PromptValidationError

try:
    # Load prompt with input validation
    prompt = load_prompt(
        "path/to/prompt.yaml",
        input_variables={"location": "moon", "capital": "moon"}
    )
    
    # Get formatted messages
    messages = prompt.messages
    
    # Use with your preferred AI provider
    response = your_ai_provider.generate(messages)
    
except PromptValidationError as e:
    print(f"Validation error: {e}")
```

## Documentation

For detailed documentation, please visit [documentation link].

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

