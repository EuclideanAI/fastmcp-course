"""Main FastMCP server entry point for Confluence integration."""

import logging
import os
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

from config import load_config
from confluence import ConfluenceClient
from tools import CommentTools, PageTools, SearchTools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="confluence_client.log",
)
logger = logging.getLogger(__name__)


@dataclass
class AppContext:
    """Application context for the lifespan."""

    confluence: ConfluenceClient


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """
    Manage application lifecycle with type-safe context.

    Args:
        server: The FastMCP server instance

    Yields:
        AppContext: The application context
    """
    # Load configuration from environment variables
    try:
        config = load_config()
        logger.info("Configuration loaded successfully")

        # Initialize confluence api client
        confluence = ConfluenceClient(
            url=config.confluence.url,
            username=config.confluence.username,
            api_token=config.confluence.api_token,
        )

        logger.info("Confluence client initialized")
        yield AppContext(confluence=confluence)
    finally:
        # Cleanup on shutdown
        logger.info("Shutting down Confluence MCP server")


# Create a named server
mcp = FastMCP("Confluence MCP Server", lifespan=app_lifespan)

# Create the ASGI application
mcp_app = mcp.http_app(path="/mcp")


# Health check endpoint
async def health_check(request: Request) -> JSONResponse:
    """Health check endpoint for load balancers and monitoring."""
    return JSONResponse(
        {
            "status": "healthy",
            "service": "Confluence MCP Server",
            "timestamp": request.scope.get("utc_time"),
        }
    )


# Create a Starlette app and mount the MCP server
app = Starlette(
    routes=[
        Route("/health", health_check, methods=["GET"]),
        Mount("/mcp-server", app=mcp_app),
        # Add other routes as needed
    ],
    lifespan=mcp_app.lifespan,
)


# Register tools
def register_tools() -> None:
    """Register all tools with the MCP server."""
    # Page tools
    mcp.add_tool(PageTools.get_page)
    mcp.add_tool(PageTools.create_page)
    mcp.add_tool(PageTools.update_page)
    mcp.add_tool(PageTools.delete_page)
    mcp.add_tool(PageTools.get_page_children)
    mcp.add_tool(PageTools.get_page_ancestors)

    # Search tools
    mcp.add_tool(SearchTools.search_confluence)
    mcp.add_tool(SearchTools.get_spaces)

    # Comment and label tools
    mcp.add_tool(CommentTools.get_comments)
    mcp.add_tool(CommentTools.add_comment)
    mcp.add_tool(CommentTools.get_labels)
    mcp.add_tool(CommentTools.add_label)

    logger.info("All tools registered successfully")


register_tools()


if __name__ == "__main__":
    import uvicorn

    # Get port from environment variable (Cloud Run sets this)
    port = int(os.environ.get("PORT", 8000))

    logger.info(f"Starting Confluence MCP server on port {port}")

    # Run the Starlette app with uvicorn for Cloud Run compatibility
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
