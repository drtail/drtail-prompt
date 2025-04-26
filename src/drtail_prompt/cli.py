from __future__ import annotations

import json
from pathlib import Path

import click
from pydantic.json import pydantic_encoder

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
