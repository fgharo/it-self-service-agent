# Migration Utilities MCP Server

A FastMCP server that provides tools for migration utilities. This server implements the Model Context Protocol (MCP) to expose migration utility functionality through standardized tools.

## Features

- **Migration Utilities**: Tools for managing application migrations
- **Destination Cluster Lookup**: Get destination cluster information for migrations

## Tools

### `get_destination_cluster(app_id: str, app_name: str, namespace: str, source_ecs_cluster: str)`

Gets the destination cluster for a migration.

**Parameters:**
- `app_id` (string): The application ID
- `app_name` (string): The name of the application
- `namespace` (string): The namespace for the application
- `source_ecs_cluster` (string): The source ECS cluster name

**Returns:**
- The destination cluster name (default: "xyz")

## Development Commands

Navigate to the `mcp-servers/migration-utilities/` directory for all development operations:

```bash
# Sync project dependencies
uv sync --all-packages

# Run unit tests
uv run pytest

# Code formatting and linting
uv run black .
uv run flake8 .

# Run the MCP server
uv run python -m migration_utilities.server
```

## Usage

### Running the Server

```bash
cd mcp-servers/migration-utilities/
uv run python -m migration_utilities.server
```

## Sample Usage

```python
# Get destination cluster for a migration
destination_cluster = get_destination_cluster(
    app_id="app-123",
    app_name="my-app",
    namespace="production",
    source_ecs_cluster="source-cluster"
)
```

## Architecture

This MCP server follows the FastMCP framework patterns:

- **Tools**: Expose callable functions to MCP clients
- **Type Safety**: Full Python type hints and validation
- **Error Handling**: Proper exception handling with meaningful messages
- **Testing**: Comprehensive test coverage with pytest
- **Tracing**: OpenTelemetry tracing support

## Project Structure

```
migration-utilities/
├── src/
│   └── migration_utilities/
│       ├── __init__.py
│       ├── server.py           # Main MCP server implementation
│       └── tracing.py           # Tracing utilities
├── tests/
│   └── test_migration_utilities.py     # Unit tests
├── pyproject.toml              # Project configuration
├── README.md                   # This file
└── uv.lock                     # Dependency lock file (generated)
```

## Environment Variables

- `MCP_TRANSPORT`: Transport protocol (default: "sse")
- `SELF_SERVICE_AGENT_MIGRATION_UTILITIES_SERVER_SERVICE_PORT_HTTP`: HTTP port (default: 8002)
- `MCP_HOST`: Host address (default: "0.0.0.0")

## Error Handling

The server validates all required parameters and returns meaningful error messages:

- All successful operations return formatted results
- Health check endpoint available at `/health`

