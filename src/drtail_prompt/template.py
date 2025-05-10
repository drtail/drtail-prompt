from __future__ import annotations

import json
from typing import Any

from jinja2.environment import Environment
from yaml import dump


def yaml(value: str | dict[str, Any], exclude_none: bool = True) -> str:
    """
    Custom filter to convert JSON string to YAML format.

    Args:
        value: JSON string to convert
        exclude_none: If True, exclude fields with None values

    Returns:
        YAML formatted string
    """
    if isinstance(value, str):
        data: dict[str, Any] = json.loads(value)
    else:
        data = value

    try:
        # Remove None values if exclude_none is True
        if exclude_none and isinstance(data, dict):

            def remove_none(d: dict[str, Any]) -> dict[str, Any]:
                result: dict[str, dict[str, Any] | list[dict[str, Any]] | Any] = {}
                for k, v in d.items():
                    if v is None:
                        continue
                    elif isinstance(v, dict):
                        nested = remove_none(v)
                        if nested:  # Only add non-empty dictionaries
                            result[k] = nested
                    elif isinstance(v, list):
                        result[k] = [
                            remove_none(i) if isinstance(i, dict) else i
                            for i in v
                            if i is not None
                        ]
                    else:
                        result[k] = v
                return result

            data = remove_none(data)

        # Convert to YAML format
        return dump(data, default_flow_style=False, sort_keys=False)
    except json.JSONDecodeError:
        return json.dumps(data)


environment = Environment(trim_blocks=True, lstrip_blocks=True, autoescape=True)
environment.filters["yaml"] = yaml
