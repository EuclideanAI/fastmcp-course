# Confluence FastMCP Server - Project Architecture

## Description

This project is to build a Confluence MCP server using python [FastMCP](https://github.com/jlowin/fastmcp). The server will be a standalone python program that can be later invoked by a MCP host e.g. Claude desktop, VS code copilot etc.

## System Requirements

1. **Package Management**:

   - `uv` as the default package manager
   - Dependencies managed through `pyproject.toml`
   - Virtual environment isolation for development and deployment

2. **Code Quality Standards**:

   - **Linting**:
     - Ruff for fast linting
     - Type annotations required for all function parameters and returns
     - Maximum line length of 88 characters (Black-compatible)
     - Docstrings required for all public functions, methods, and classes
   - **Formatting**:
     - Ruff for consistent code formatting
     - Isort for import statement organization
     - Trailing commas on multiline collections
     - Use of double quotes for strings

3. **Method Decoration Pattern**:
   - For FastMCP tools, follow proper method decoration patterns:
     - Static methods can be decorated directly with `@mcp.tool()`
     - Instance methods should be registered after instance creation with `mcp.add_tool(obj.method)`
     - Class methods should be registered after class definition with `mcp.add_tool(MyClass.method)`
   - See detailed examples in `decorating-methods.prompt.md`

## Core Components

1. **FastMCP Server**:

   - manage the mcp server session
   - manage the app lifespan

2. **Confluence Client**: Confluence Client class including a client session and all confluence apis

   - Confluence client session initiation
   - APIs from [atlassian-python-api](https://github.com/atlassian-api/atlassian-python-api)

3. **Model**: Data models that are used with Confluence Client

   - Page
   - Search
   - Comment
   - Label
   - Space

4. **utils**: Any utils that are needed e.g. specific parsing, handling datetime values etc.
   - parsers
   - datetime handler

## Folder structure

```
fastmcp-course/
├── server.py              # Main FastMCP server entry point
├── confluence/
│   ├── __init__.py        # Package initialization
│   ├── client.py          # Confluence client implementation
│   ├── models.py          # Data models for Confluence objects
│   └── utils.py           # Utility functions
├── tools/
│   ├── __init__.py        # Package initialization
│   ├── page_tools.py      # Tools for page operations
│   ├── search_tools.py    # Tools for search operations
│   └── comment_tools.py   # Tools for comment operations
├── tests/                 # Test suite
│   ├── conftest.py        # Test configurations and fixtures
│   ├── test_client.py     # Tests for client functionality
│   └── test_tools.py      # Tests for MCP tools
├── config.py              # Configuration management
└── README.md              # Project documentation
```

Example environment variables:

```
CONFLUENCE_URL=https://your-domain.atlassian.net
CONFLUENCE_USERNAME=your-email@example.com
CONFLUENCE_API_TOKEN=your-api-token
```

## Error Handling

The server will implement comprehensive error handling:

1. API error handling with meaningful error messages
2. Rate limiting awareness with backoff strategies
3. Connection error recovery
4. Detailed logging with configurable verbosity

## Testing Strategy

The testing approach will include:

1. Unit tests for individual components
2. Integration tests with mock Confluence API
3. End-to-end tests with a test Confluence instance
4. Load testing for performance characteristics

## Code example

### Server

The FastMCP server is your core interface to the MCP protocol. It handles connection management, protocol compliance, and message routing:

```python
# Add lifespan support for startup/shutdown with strong typing
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass

from confluence import ConfluenceClient  # Replace with your actual DB type

from fastmcp import Context, FastMCP

# Create a named server
mcp = FastMCP("My App")


@dataclass
class AppContext:
    confluence: ConfluenceClient


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""
    # Initialize confluence api client
    confluence = ConfluenceClient()
    try:
        yield AppContext(confluence=confluence)
    finally:
        # Cleanup on shutdown
        await confluence.disconnect()


# Pass lifespan to server
mcp = FastMCP("My App", lifespan=app_lifespan)


# Access type-safe lifespan context in tools
@mcp.tool()
def query_db(ctx: Context) -> str:
    """Tool that uses initialized resources"""
    db = ctx.request_context.lifespan_context.confluence
    return confluence.search()
```

### Example Tool Implementation

Here's an example of implementing a specific Confluence tool:

1. Define a staticmethod in SeaerchTools class

```python
class SearchTools:
  @staticmethod
  async def search_confluence(
      ctx: Context,
      query: str,
      spaces: list[str] = None,
      limit: int = 10
  ) -> dict:
      """
      Search Confluence content using CQL or text search

      Args:
          query: Search terms or CQL query
          spaces: Optional list of space keys to restrict search
          limit: Maximum number of results to return

      Returns:
          Dictionary with search results
      """
      client = ctx.request_context.lifespan_context.confluence

      try:
          results = await client.search(
              cql_or_text=query,
              spaces=spaces,
              limit=limit
          )
          return {
              "status": "success",
              "results": results,
              "count": len(results)
          }
      except Exception as e:
          return {
              "status": "error",
              "message": str(e)
          }
```

2. Register the tool with the server

```python
from tools.search_tools import SearchTools
from fastmcp import FastMCP
mcp = FastMCP("My App")
# Register the tool
mcp.add_tool(SearchTools.search_confluence)
```
