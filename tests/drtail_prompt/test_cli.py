from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from drtail_prompt.cli import cli


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def test_data_dir() -> Path:
    """Get the test data directory."""
    return Path(__file__).parent / "data"


def test_validate_command_success(
    runner: CliRunner,
    test_data_dir: Path,
) -> None:
    """Test validate command with a valid prompt file."""
    result = runner.invoke(
        cli,
        ["validate", str(test_data_dir / "basic_1.yaml")],
    )
    assert result.exit_code == 0
    assert "✅ Prompt validation successful" in result.output
    assert "Metadata:" in result.output
    assert "Messages:" in result.output


def test_validate_command_with_inputs(
    runner: CliRunner,
    test_data_dir: Path,
) -> None:
    """Test validate command with input parameters."""
    result = runner.invoke(
        cli,
        [
            "validate",
            str(test_data_dir / "basic_3.yaml"),
            "--set",
            "location=earth",
            "--set",
            "capital=washington",
        ],
    )
    assert result.exit_code == 0
    assert "✅ Prompt validation successful" in result.output


def test_validate_command_with_json_inputs(
    runner: CliRunner,
    test_data_dir: Path,
) -> None:
    """Test validate command with JSON input parameters."""
    result = runner.invoke(
        cli,
        [
            "validate",
            str(test_data_dir / "advanced.yaml"),
            "--set",
            'nested={"location": "earth", "capital": "washington"}',
            "--set",
            'nested_nested={"inner": {"location": "moon", "capital": "moon"}}',
        ],
    )
    assert result.exit_code == 1
    assert "❌ Validation error" in result.output


def test_validate_command_invalid_file(runner: CliRunner) -> None:
    """Test validate command with an invalid file."""
    result = runner.invoke(
        cli,
        ["validate", "nonexistent.yaml"],
    )
    assert result.exit_code != 0
    assert "Error" in result.output


def test_validate_command_invalid_input_format(
    runner: CliRunner,
    test_data_dir: Path,
) -> None:
    """Test validate command with invalid input format."""
    result = runner.invoke(
        cli,
        [
            "validate",
            str(test_data_dir / "basic_3.yaml"),
            "--set",
            "invalid_format",
        ],
    )
    assert result.exit_code != 0
    assert "Invalid parameter format" in result.output


def test_validate_command_validation_error(
    runner: CliRunner,
    test_data_dir: Path,
) -> None:
    """Test validate command with a file that fails validation."""
    result = runner.invoke(
        cli,
        ["validate", str(test_data_dir / "nonexistent.yaml")],
    )
    assert result.exit_code != 0
    assert "Invalid value for 'PROMPT_PATH'" in result.output


def test_generate_schema_command(runner: CliRunner, tmp_path: Path) -> None:
    """Test generate-schema command."""
    output_file = tmp_path / "prompt.json"
    result = runner.invoke(
        cli,
        ["generate-schema", str(output_file)],
    )
    assert result.exit_code == 0
    assert "JSON schema generated successfully" in result.output
    assert output_file.exists()

    # Verify the generated schema
    with output_file.open() as f:
        schema = json.load(f)
    assert "type" in schema
    assert "properties" in schema


def test_generate_schema_command_default_output(
    runner: CliRunner,
    tmp_path: Path,
) -> None:
    """Test generate-schema command with default output."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["generate-schema"])
        assert result.exit_code == 0
        assert "JSON schema generated successfully" in result.output
        assert Path("prompt.json").exists()


def test_version_command(runner: CliRunner) -> None:
    """Test version command."""
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    # Version should be a semantic version string
    assert result.output.strip().count(".") == 2


def test_bump_version_command(runner: CliRunner, tmp_path: Path) -> None:
    """Test bump-version command."""
    # Create a temporary pyproject.toml
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        """
[project]
version = "0.1.0"
""",
    )

    with runner.isolated_filesystem():
        # Copy pyproject.toml to the isolated filesystem
        with open(pyproject, "rb") as src, open("pyproject.toml", "wb") as dst:
            dst.write(src.read())

        result = runner.invoke(cli, ["meta", "bump-version", "1.0.0"])
        assert result.exit_code == 0
        assert "Version bumped to 1.0.0" in result.output

        # Verify the version was updated
        with open("pyproject.toml", "rb") as f:
            content = f.read().decode()
            assert 'version = "1.0.0"' in content
