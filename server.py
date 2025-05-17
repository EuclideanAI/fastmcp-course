import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from fastmcp import FastMCP

from confluence.client import ConfluenceClient
from tools.comment_tools import CommendTools
from tools.page_tools import PageTools
from tools.search_tools import SearchTools

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Application context containing shared resources
@dataclass
class AppContext:
    """Application context with dependencies."""

    confluence: ConfluenceClient


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """
    Manage application lifecycle with type-safe context.

    This function is called when the server starts and stops,
    handling the initialization and cleanup of resources.

    Args:
        server: The FastMCP server instance

    Yields:
        AppContext: The application context with initialized dependencies
    """
    logger.info("Starting Confluence FastMCP server")

    # Initialize Confluence client
    try:
        confluence = ConfluenceClient()
        logger.info("Confluence client initialized successfully")

        # Yield the app context with initialized resources
        yield AppContext(confluence=confluence)
    finally:
        # Cleanup resources when the server shuts down
        logger.info("Shutting down Confluence FastMCP server")
        # await confluence.disconnect()


# Create the FastMCP server with lifespan management
mcp = FastMCP(name="ConfluenceServer", lifespan=app_lifespan)

# Register comment tools
mcp.add_tool(CommendTools.add_comment)
mcp.add_tool(CommendTools.add_label)
mcp.add_tool(CommendTools.get_labels)
mcp.add_tool(CommendTools.get_comments)

# Register page tools
mcp.add_tool(PageTools.get_page)
mcp.add_tool(PageTools.create_page)
mcp.add_tool(PageTools.update_page)
mcp.add_tool(PageTools.delete_page)
mcp.add_tool(PageTools.get_page_children)
mcp.add_tool(PageTools.get_page_ancestors)

# Register search tools
mcp.add_tool(SearchTools.search_confluence)
mcp.add_tool(SearchTools.get_spaces)

if __name__ == "__main__":
    # Start the server
    mcp.run()
