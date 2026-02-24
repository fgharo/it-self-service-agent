"""Migration Utilities MCP Server.

A FastMCP server that provides tools for migration utilities.
"""

import os
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Literal

from mcp.server.fastmcp import Context, FastMCP
from shared_models import configure_logging
from starlette.responses import JSONResponse
from tracing_config.auto_tracing import run as auto_tracing_run

from migration_utilities.tracing import trace_mcp_tool

SERVICE_NAME = "migration-utilities-mcp-server"
logger = configure_logging(SERVICE_NAME)
auto_tracing_run(SERVICE_NAME, logger)


@asynccontextmanager
async def lifespan(app: FastMCP) -> AsyncGenerator[None, None]:
    """Initialize and validate configuration at startup."""
    # Startup: Initialize configuration
    logger.info("Initializing Migration Utilities configuration")

    try:
        yield
    finally:
        # Cleanup
        logger.info("Shutting down Migration Utilities MCP server")


MCP_TRANSPORT: Literal["stdio", "sse", "streamable-http"] = os.environ.get("MCP_TRANSPORT", "sse")  # type: ignore[assignment]
MCP_PORT = int(
    os.environ.get(
        "SELF_SERVICE_AGENT_MIGRATION_UTILITIES_SERVER_SERVICE_PORT_HTTP", "8002"
    )
)
MCP_HOST = os.environ.get("MCP_HOST", "0.0.0.0")
mcp = FastMCP(
    "Migration Utilities Server",
    host=MCP_HOST,
    stateless_http=(MCP_TRANSPORT == "streamable-http"),
    lifespan=lifespan,
)


@mcp.custom_route("/health", methods=["GET"])  # type: ignore
async def health(request: Any) -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse({"status": "OK"})


@mcp.tool()
@trace_mcp_tool()
def get_destination_cluster(
    app_id: str,
    app_name: str,
    namespace: str,
    source_ecs_cluster: str,
    ctx: Context[Any, Any],
) -> str:
    """Get the destination cluster for a migration.

    Args:
        app_id: The application ID
        app_name: The name of the application
        namespace: The namespace for the application
        source_ecs_cluster: The source ECS cluster name

    Returns:
        The destination cluster name (default: "xyz")
    """
    try:
        logger.info(
            "Getting destination cluster",
            tool="get_destination_cluster",
            app_id=app_id,
            app_name=app_name,
            namespace=namespace,
            source_ecs_cluster=source_ecs_cluster,
        )

        # Return default value
        return "xyz"

    except Exception as e:
        error_msg = f"Error getting destination cluster: {str(e)}"
        logger.error(error_msg)
        return error_msg


def main() -> None:
    """Run the Migration Utilities MCP server."""
    mcp.run(transport=MCP_TRANSPORT)


# Expose the ASGI app for uvicorn (for streamable-http transport)
app = mcp.streamable_http_app()


if __name__ == "__main__":
    main()
