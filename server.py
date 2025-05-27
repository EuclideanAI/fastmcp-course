"""Main FastMCP server entry point for Confluence integration."""

import logging

from fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="confluence_client.log",
)
logger = logging.getLogger(__name__)


mcp = FastMCP(
    name="Confluence MCP Server",
    description="A FastMCP server for Confluence integration",
    version="1.0.0",
)

if __name__ == "__main__":
    logger.info("Starting Confluence MCP server")
    mcp.run()
