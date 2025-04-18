# VS Code Integration Guide

This guide explains how to use the generated JSON schema for YAML autocomplete in VS Code.

## Prerequisites

1. VS Code installed on your system
2. The "YAML" extension by Red Hat installed in VS Code
   - You can install it from the VS Code marketplace or run:
     ```bash
     code --install-extension redhat.vscode-yaml
     ```

## Generating the JSON Schema

1. Install the `drtail-prompt` package:
   ```bash
   pip install drtail-prompt
   ```

2. Generate the JSON schema using the CLI:
   ```bash
   drtailpromptctl generate-schema prompt.json
   ```
   This will create a `prompt.json` file containing the JSON schema.

## Configuring VS Code

There are two ways to configure VS Code to use the JSON schema:

### Method 1: Workspace Settings (Recommended)

1. Create or open `.vscode/settings.json` in your project root:
   ```json
   {
     "yaml.schemas": {
       "https://github.com/drtail/drtail-prompt/releases/download/v0.1.1/prompt.json": ["*.prompt.yaml", "*.prompt.yml"]
     }
   }
   ```

2. Make sure the path to `prompt.json` is relative to your workspace root.

### Method 2: YAML File Association

Add a schema reference directly in your YAML file:

```yaml
# yaml-language-server: $schema=./prompt.json
api: "your-api"
version: "1.0.0"
# ... rest of your prompt configuration
```

## JetBrains IDE Integration

JetBrains IDEs (PyCharm, IntelliJ IDEA, WebStorm, etc.) also support JSON schema validation for YAML files. Here's how to configure it:

### Method 1: Project-Level Schema Association

1. Open your project in a JetBrains IDE
2. Go to **File** > **Settings** (or **Preferences** on macOS)
3. Navigate to **Languages & Frameworks** > **Schemas and DTDs** > **JSON Schema Mappings**
4. Click the **+** button to add a new schema mapping
5. Configure the mapping:
   - **Schema file**: Select your `prompt.json` file
   - **File URL pattern**: Add `*.prompt.yaml` or `*.prompt.yml` to match your YAML files
6. Click **OK** to save the configuration

### Method 2: File-Level Schema Association

Add a schema reference directly in your YAML file:

```yaml
# $schema: ./prompt.json
api: "your-api"
version: "1.0.0"
# ... rest of your prompt configuration
```

### Method 3: Remote Schema Association

For remote schema files (like GitHub-hosted schemas):

1. Go to **File** > **Settings** (or **Preferences** on macOS)
2. Navigate to **Languages & Frameworks** > **Schemas and DTDs** > **JSON Schema Mappings**
3. Click the **+** button to add a new schema mapping
4. Configure the mapping:
   - **Schema URL**: Enter the URL to your schema (e.g., `https://github.com/drtail/drtail-prompt/releases/download/v0.1.1/prompt.json`)
   - **File URL pattern**: Add `*.prompt.yaml` or `*.prompt.yml`
5. Click **OK** to save the configuration

### JetBrains IDE Features

Once configured, you'll get:

1. **Code Completion**: Intelligent suggestions for properties and values
2. **Validation**: Real-time validation against the schema
3. **Documentation**: Hover tooltips showing property descriptions
4. **Quick Documentation**: View schema details with Ctrl+Q (or Cmd+Q on macOS)
5. **Go to Declaration**: Navigate to schema definitions with Ctrl+B (or Cmd+B on macOS)

## Features

Once configured, you'll get:

1. **Autocomplete**: VS Code will suggest valid properties and values based on the schema
2. **Validation**: Real-time validation of your YAML against the schema
3. **Documentation**: Hover over properties to see their descriptions
4. **Error Detection**: Immediate feedback for invalid configurations

## Example Usage

Here's an example of how the autocomplete works in a YAML file:

```yaml
api: "openai"  # Will show autocomplete for supported APIs
version: "1.0.0"
name: "my-prompt"  # Will validate required fields
description: "A sample prompt"
authors:
  - name: "John Doe"  # Will show required fields for authors
    email: "john@example.com"
metadata:
  role: "user"  # Will suggest valid roles
  domain: "general"
  action: "chat"
messages:
  - role: "system"  # Will validate message structure
    content: "You are a helpful assistant"
```

## Troubleshooting

1. **Schema not loading**:
   - Ensure the path to `prompt.json` is correct
   - Try using an absolute path in the settings
   - Restart VS Code after configuration changes

2. **Autocomplete not working**:
   - Verify the YAML extension is installed and enabled
   - Check if the file extension matches your schema configuration
   - Ensure the schema file is valid JSON

3. **Validation errors**:
   - Check the schema version matches your YAML version
   - Verify all required fields are present
   - Ensure field values match the schema constraints

## Additional Resources

- [VS Code YAML Extension Documentation](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)
- [JSON Schema Documentation](https://json-schema.org/understanding-json-schema/)
- [YAML Language Server Documentation](https://github.com/redhat-developer/yaml-language-server)
- [JetBrains JSON Schema Support](https://www.jetbrains.com/help/idea/json.html#ws_json_schema_add_custom)
