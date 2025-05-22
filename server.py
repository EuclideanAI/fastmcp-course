"""Main FastMCP server entry point for Confluence integration."""
import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

from fastmcp import FastMCP

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


# Create a named server
mcp = FastMCP("Confluence MCP Server")

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
    logger.info("Starting Confluence MCP server")
    mcp.run()
