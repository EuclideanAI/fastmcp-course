# FastMCP from Zero to Hero: Course Outline

![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)

## Introduction

- What's MCP (Model Context Protocol)
- Why do we need it (key features and benefits)
- Live Demo with Atlassian MCP Server

## Quick Start

- Set up the dev environment
- Creating your first server
- Understand the core building blocks - Tools, Resources, Prompts, Context

## Project 1 - Confluence MCP

- Building a Confluence MCP
- Integrate with VS Code Copilot and Claude Desktop

## Project 2 - Unit Test, Network, Authentication and Remote Server

- Unit test
- Transport protocols
- Authentication
- Remote Server Deployment

## Project 3 - Advanced Topics

- Mounting to FastAPI
- Sampling
- Proxy Server

## Porject 4 - MCP Client

## Project Instructions

### Project 1 - Confluence MCP

For detailed instructions, refer to the [Project 1 Guide](./instructions/instruct-project1.md).

## Development Setup

This project uses modern Python development tools to ensure code quality and consistency.

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver

### Setting Up Development Environment

1. **Clone the project branch:**

   - **Project 1 (Confluence MCP):**
     ```bash
     git clone -b project1 https://github.com/EuclideanAI/fastmcp-course.git
     cd fastmcp-course
     ```
   - **Project 2 (Network, Authentication and Remote Server):**
     ```bash
     git clone -b project2 https://github.com/EuclideanAI/fastmcp-course.git
     cd fastmcp-course
     ```
   - **Project 3 (Advanced Topics):**
     ```bash
     git clone -b project3 https://github.com/EuclideanAI/fastmcp-course.git
     cd fastmcp-course
     ```

2. **Install dependencies using [uv](https://docs.astral.sh/uv/getting-started/installation/):**

   - If you don't have `uv` installed, follow the [installation guide](https://docs.astral.sh/uv/getting-started/installation/).
   - If `uv` is already installed, sync dependencies:
     ```bash
     uv sync
     ```

3. **Set up pre-commit hooks (recommended):**

   ```bash
   uv run pre-commit install
   uv run pre-commit install --hook-type commit-msg
   ```

4. **Lint your code with Ruff:**

   ```bash
   uv run ruff check .
   ```

5. **Format your code with Ruff:**

   ```bash
   uv run ruff format .
   ```

6. **Run pre-commit on all files:**

   ```bash
   uv run pre-commit run --all-files
   ```

### Code Quality Standards

This project enforces strict code quality standards through automated tools:

#### Pre-commit Hooks

We use pre-commit hooks to ensure code quality before commits. The hooks include:

- **Ruff**: Fast linting and code formatting
- **MyPy**: Static type checking
- **Standard hooks**: Trailing whitespace, end-of-file fixes, YAML/TOML validation
- **Conventional Commits**: Enforces conventional commit message format

#### Conventional Commits

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) specification. All commit messages must follow this format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Allowed types:**

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

**Examples:**

```
feat: add search functionality to confluence tools
fix: resolve type annotation issues in test files
docs: update README with conventional commit guidelines
test: add unit tests for page operations
```

### System Prompts for Copilot Agent

The system prompts saved under `.github/prompts` outline the code quality standard for copilot coding agent (it will be included as system prompt in every conversation):

- planning.prompt.md

## Requirements

You will need to have the following installed/ready:

- Python 3.10+ (Can install this through uv)
- Confluence instance (Cloud)
- Confluence API credentials

## Configuration

Configure the application via environment variables (create `.env` file):

```
CONFLUENCE_URL="https://your-domain.atlassian.net"
CONFLUENCE_USERNAME="your-email@example.com"
CONFLUENCE_PAT="your-api-token"
```

## Usage

Run the FastMCP server with Inspector:

```bash
fastmcp dev server.py
```

Run the FastMCP server as a normal mcp server in local:

```bash
uv run server.py
```

## Running Tests

This project includes comprehensive tests for the Confluence client and MCP tools. To run the tests:

```bash
uv run pytest
```

For more verbose output:

```bash
uv run pytest -v
```

To run specific test files:

```bash
uv run pytest tests/test_client.py
uv run pytest tests/test_tools.py
```

### Test Coverage

The coverage badge at the top of this README is automatically updated via GitHub Actions whenever code is pushed to the main branch.

#### Local Testing

To run tests with coverage locally:

```bash
# Run tests with coverage
uv run pytest

# Manually update the coverage badge (optional - GitHub Actions handles this automatically)
uv run python update_coverage_badge.py
```

#### Automated Coverage Updates

The project includes GitHub Actions workflows that:

1. **On Push to Main**: Automatically runs tests, calculates coverage, and updates the badge in the README
2. **On Pull Requests**: Runs tests and provides coverage information (badge updates only happen on main branch)

The coverage badge shows the current test coverage percentage with color coding:

- 🟢 Green: 90%+ coverage
- 🟡 Yellow-Green: 80-89% coverage
- 🟡 Yellow: 60-79% coverage
- 🟠 Orange: 50-59% coverage
- 🔴 Red: <50% coverage

## AI Integration

The Confluence MCP server can be integrated with various AI assistants:

### VS Code Copilot

To integrate with VS Code Copilot:

1. Ensure the server is running locally with `uv run server.py`
2. Open VS Code with the Copilot extension installed
3. Connect Copilot to the local MCP server

### Claude Desktop

To integrate with Claude Desktop:

1. Ensure the server is running locally with `uv run server.py`
2. Open Claude Desktop
3. In settings, add the local MCP server URL (typically `http://localhost:8000`)

## Project Structure

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
├── tests/
│   ├── conftest.py        # Test configurations and fixtures
│   ├── test_client.py     # Tests for client functionality
│   └── test_tools.py      # Tests for MCP tools
├── config.py              # Configuration management
├── .env.example           # Example environment variables
└── README.md              # Project documentation
```

## License

[MIT]
