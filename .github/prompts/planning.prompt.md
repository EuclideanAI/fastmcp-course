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
     - Black for consistent code formatting
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

## Authentication and Configuration

The server will support the following authentication methods for Confluence:

- API Token authentication
- Personal Access Token (PAT)
- OAuth2 (for advanced use cases)

Configuration will be managed through:

- Environment variables (for sensitive information)
- Configuration file (for non-sensitive defaults)
- Command-line arguments (for overrides)

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

## MCP Tools Implementation

The server will expose the following tools through MCP:

1. **Content Tools**:

   - `search_confluence`: Search content with various filters
   - `get_page`: Get page content by ID
   - `create_page`: Create new page in a space
   - `update_page`: Update existing page
   - `delete_page`: Delete a page

2. **Metadata Tools**:

   - `get_page_history`: View page history/versions
   - `add_label`: Add labels to content
   - `get_labels`: Get labels for content
   - `get_comments`: Get comments for a page

3. **Navigation Tools**:
   - `get_page_children`: List child pages
   - `get_page_ancestors`: Get parent pages/breadcrumbs
   - `get_spaces`: List available spaces

## Testing Strategy

The testing approach will include:

1. Unit tests for individual components
2. Integration tests with mock Confluence API
3. End-to-end tests with a test Confluence instance
4. Load testing for performance characteristics

## Project Setups

To ensure the code quality standards described in the System Requirements section are consistently applied, the following project setups should be implemented:

### 1. VS Code Configuration

Create a `.vscode/settings.json` file with the following configuration:

```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true,
    "source.fixAll": true
  },
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.lintOnSave": true,
  "python.linting.ruffEnabled": true,
  "python.analysis.typeCheckingMode": "basic",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.rulers": [88]
  },
  "isort.args": ["--profile", "black"],
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.analysis.extraPaths": ["${workspaceFolder}"],
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/*.pyc": true
  }
}
```

### 2. Pre-commit Hooks

Create a `.pre-commit-config.yaml` file to enforce standards on commits:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-json
      - id: check-added-large-files

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.2.2
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

### 3. Project Configuration in pyproject.toml

Ensure the `pyproject.toml` file includes the following tool configurations:

```toml
[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true

[tool.black]
line-length = 88
target-version = ["py310"]

[tool.isort]
profile = "black"
line_length = 88

[tool.ruff]
line-length = 88
target-version = "py310"
select = [
    "E", # pycodestyle errors
    "W", # pycodestyle warnings
    "F", # pyflakes
    "I", # isort
    "B", # flake8-bugbear
    "C4", # flake8-comprehensions
    "N", # pep8-naming
]
ignore = [
    "E501", # line too long, handled by black
    "B008", # do not perform function calls in argument defaults
]
```

### 4. Developer Documentation

Update the README.md to include development setup instructions:

````markdown
## Development Setup

This project uses modern Python development tools to ensure code quality and consistency.

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver

### Setting Up Development Environment

1. Clone this repository:

```bash
git clone <repository-url>
cd <project-name>
```
````

2. Create a virtual environment using uv:

```bash
uv venv
```

3. Activate the virtual environment:

```bash
# On macOS/Linux
source .venv/bin/activate

# On Windows
.\.venv\Scripts\activate
```

4. Install development dependencies:

```bash
uv pip install -e ".[dev]"
```

5. Set up pre-commit hooks:

```bash
pre-commit install
```

### Code Quality Standards

This project enforces the following standards:

- **Type Annotations**: All functions must have parameter and return type annotations
- **Code Formatting**: Black with 88 character line length
- **Import Sorting**: isort configured with Black compatibility
- **Linting**: Ruff for fast linting and error detection
- **Method Decoration**: Follow the patterns for FastMCP tools

````

### 5. Dependencies in pyproject.toml

Ensure development dependencies include all necessary tools:

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.3.1",
    "pytest-asyncio>=0.21.0",
    "black>=23.3.0",
    "isort>=5.12.0",
    "mypy>=1.3.0",
    "ruff>=0.0.267",
    "pre-commit>=3.3.1",
]
````

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

```python
@mcp.tool()
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
