# FastMCP from Zero to Hero: Course Outline

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

## Project 2 - Network, Authentication and Remote Server

- Transport protocols
- Authentication
- Remote Server Deployment

## Project 3 - Advanced Topics

- Mounting to FastAPI
- Sampling
- Proxy Server

<br>

# Project 1 - Confluence FastMCP Server

A Model Context Protocol (MCP) server for interacting with Atlassian Confluence, built with Python and FastMCP.

## Description

This project implements an MCP server that provides AI assistants with tools to interact with Confluence. The server enables capabilities such as searching content, retrieving page information, creating and updating pages, and managing comments and labels.

## Features

- **Content Operations**: Search, retrieve, create, update, and delete Confluence pages
- **Navigation**: Get page children and ancestors for hierarchical navigation
- **Metadata Management**: Manage comments and labels
- **Space Management**: List and navigate Confluence spaces

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

3. **Lint your code with Ruff:**

   ```bash
   uv run ruff check .
   ```

4. **Format your code with Ruff:**
   ```bash
   uv run ruff format .
   ```

### Code Quality Standards - System Prompt for Copilot Agent

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
CONFLUENCE_API_TOKEN="your-api-token"
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
├── config.py              # Configuration management
└── README.md              # Project documentation
```

## License

[MIT]
