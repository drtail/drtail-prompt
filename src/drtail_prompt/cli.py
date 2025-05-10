from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import click
from pydantic.json import pydantic_encoder

from drtail_prompt.core import load_prompt
from drtail_prompt.exception import PromptValidationError
from drtail_prompt.schema import BasicPromptSchema


@click.group()
def cli() -> None:
    """DRTail Prompt CLI tools."""
    pass


@cli.group()
def meta() -> None:
    """Controls library itself."""
    pass


@cli.command()
@click.argument(
    "prompt_path",
    type=click.Path(
        exists=True,
        dir_okay=False,
        path_type=Path,
    ),  # type: ignore
)
@click.option(
    "--set",
    "set_params",
    multiple=True,
    help=(
        "Set input parameters in the format 'key=value'. Can be used multiple times."
    ),
)
def validate(prompt_path: Path, set_params: tuple[str, ...]) -> None:
    """Validate a prompt YAML file.

    PROMPT_PATH is the path to the prompt YAML file to validate.
    """
    # Convert set parameters to dictionary
    inputs: dict[str, Any] = {}
    for param in set_params:
        try:
            key, value = param.split("=", 1)
            # Try to parse value as JSON first, fallback to string
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                pass
            inputs[key] = value
        except ValueError:
            click.echo(
                f"Error: Invalid parameter format '{param}'. Use 'key=value' format.",
            )
            raise

    try:
        # Load and validate the prompt
        prompt = load_prompt(str(prompt_path), inputs=inputs if inputs else None)
        click.echo(f"✅ Prompt validation successful: {prompt_path}")

        # Print metadata if available
        if prompt.metadata:
            click.echo("\nMetadata:")
            for key, value in prompt.metadata.items():
                click.echo(f"  {key}: {value}")

        # Print messages if available
        if prompt.messages:
            click.echo("\nMessages:")
            for msg in prompt.messages:
                click.echo(f"  [{msg.role}]: {msg.content[:100]}...")

    except PromptValidationError as e:
        click.echo(f"❌ Validation error: {e}", err=True)
        raise
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise


@cli.command()
@click.argument(
    "output",
    type=click.Path(dir_okay=False, path_type=Path),  # type: ignore
    default="prompt.json",
)
def generate_schema(output: Path | None = None) -> None:
    """Generate JSON schema from a YAML prompt schema file.

    OUTPUT is the path to the output JSON schema file.
    """

    # Generate JSON schema
    json_schema = BasicPromptSchema.model_json_schema()

    # Determine output path
    if output is None:
        output = Path("prompt.json")

    # Write the JSON schema
    with output.open("w") as f:
        json.dump(json_schema, f, indent=2, default=pydantic_encoder)

    click.echo(f"JSON schema generated successfully: {output}")


@cli.command()
def version() -> None:
    """Print the version of the library."""
    from drtail_prompt import __version__

    click.echo(__version__)


@meta.command()
@click.argument("version", type=str)
def bump_version(version: str) -> None:
    """Bump the version of the library.

    VERSION is the new version of the library.
    """
    import tomli
    import tomli_w  # type: ignore

    # Update pyproject.toml
    with open("pyproject.toml", "rb") as f:
        data = tomli.load(f)

    data["project"]["version"] = version

    with open("pyproject.toml", "wb") as f:
        tomli_w.dump(data, f)

    click.echo(f"Version bumped to {version} in pyproject.toml")


if __name__ == "__main__":
    cli()
