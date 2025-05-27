# 🚀 FastMCP from Zero to Hero: Building Production-Ready AI Agents with Model Context Protocol

_Master the Model Context Protocol and build production-ready AI agents that can connect to any tool or service_

**🎥 Watch the full course:** [FastMCP from Zero to Hero - Complete Tutorial](https://youtu.be/LUIbO0TQkfA)

---

## 📋 Table of Contents

- [What is MCP and Why It Matters](#what-is-mcp-and-why-it-matters)
- [Live Demo: AI Agent in Action](#live-demo-ai-agent-in-action)
- [Core Building Blocks of MCP](#core-building-blocks-of-mcp)
- [Project Setup and Architecture](#project-setup-and-architecture)
- [Building the Confluence MCP Server](#building-the-confluence-mcp-server)
- [Integration with AI Clients](#integration-with-ai-clients)
- [Testing and Debugging](#testing-and-debugging)
- [Conclusion and Next Steps](#conclusion-and-next-steps)

---

## 🔮 What is MCP and Why It Matters

> "Think of MCP like a universal USB-C connector for AI applications—one standard that works regardless of which AI model or tools you're using."

MCP stands for **Model Context Protocol**. It's a standardized way for AI models to communicate with various tools and services. Just like USB-C lets you use the same cable to connect different devices, MCP makes your AI integrations portable and future-proof.

### 🎯 Key Benefits of MCP

- **Portability:** Easily swap AI models or clients without rewriting code
- **Modularity:** Spend less time on custom integrations, more on features
- **Standardization:** Everyone integrates with LLMs the same way
- **Future-proofing:** New AI models and tools plug into existing setup
- **Rapid Growth:** 10,000+ MCP servers already available in registries

---

## 🎬 Live Demo: AI Agent Building Confluence Pages

**🎥 See this demo in action:** [Watch the live demo at 2:30](https://youtu.be/LUIbO0TQkfA?t=150)

Before diving into the technical details, let's see MCP in action! Imagine you're a product manager and you type:

_"I need to create a PRD (Product Requirement Document) for an AI-powered baby tracker app. The app should help parents track feeding times, sleep patterns, nappy changes, and growth milestones..."_

Watch what happens:

1. 🔍 Agent detects available tools from the Atlassian MCP server
2. 📝 Generates a comprehensive PRD in a `PRD.md` file
3. 🔗 Connects to Confluence workspace to find templates
4. 📄 Creates a new Confluence page with proper formatting
5. ✨ Converts content to match company standards

All of this happens automatically, with the AI agent orchestrating multiple tools seamlessly!

---

## 🏗️ Core Building Blocks of MCP

MCP has three fundamental components that work together to create powerful AI integrations:

### 🛠️ Tools

**Model-controlled** - The AI model decides when and how to use them during reasoning

- Function calling capabilities
- API integrations
- Action execution

### 📚 Resources

**Application-controlled** - Data or configuration exposed to your application

- Configuration data
- Static content
- Reference materials

### 💬 Prompts

**User-controlled** - Specific instructions that guide model behavior

- Template prompts
- Context injection
- Behavior guidance

> **⚠️ Client Support Note:** Not all MCP clients support all three building blocks. Most IDEs (VS Code Copilot, Cursor, Windsurf) currently only support **Tools**. To see all three components working together, use **Claude Desktop**.

---

## ⚙️ Project Setup and Architecture

### 🛠️ Tech Stack

`Python 3.10+` • `FastMCP` • `UV Package Manager` • `Atlassian Python API` • `Ruff (Linting)` • `Pytest (Testing)`

### 📁 Project Structure

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
├── config.py              # Configuration management
└── README.md              # Project documentation
```

### Quick Setup

**Step 1: Install UV Package Manager**

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Step 2: Initialize Project**

```bash
uv init fastmcp-confluence
cd fastmcp-confluence
uv add fastmcp atlassian-python-api
```

---

## 👨‍💻 Building the Confluence MCP Server

### 🔧 Server Implementation

The heart of our MCP server uses FastMCP's context management system:

```python
"""Main FastMCP server entry point for Confluence integration."""

import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

from fastmcp import FastMCP
from config import load_config
from confluence import ConfluenceClient
from tools import CommentTools, PageTools, SearchTools

@dataclass
class AppContext:
    """Application context for the lifespan."""
    confluence: ConfluenceClient

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context."""
    config = load_config()
    confluence = ConfluenceClient(
        url=config.confluence.url,
        username=config.confluence.username,
        api_token=config.confluence.api_token,
    )

    try:
        yield AppContext(confluence=confluence)
    finally:
        logger.info("Shutting down Confluence MCP server")

# Create the FastMCP server
mcp = FastMCP("Confluence MCP Server", lifespan=app_lifespan)
```

### 🔨 Tool Implementation Pattern

Each tool follows a consistent pattern using static methods:

```python
class PageTools:
    """Tools for interacting with Confluence pages."""

    @staticmethod
    async def get_page(
        ctx: Context,
        page_id: str,
        include_body: bool = True,
    ) -> Dict[str, Any]:
        """
        Get Confluence page content and metadata by ID.

        Args:
            page_id: The ID of the Confluence page
            include_body: Whether to include the full page content

        Returns:
            Dictionary with page information
        """
        client = ctx.request_context.lifespan_context.confluence

        try:
            page = await client.get_page(page_id=page_id, include_body=include_body)
            return {
                "status": "success",
                "page": page
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
```

### 🔌 Tool Registration

Tools are registered with the MCP server using a simple registration function:

```python
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

register_tools()
```

### ✅ Complete Feature Set

Our Confluence MCP server provides comprehensive functionality:

- **Page Management:** Create, read, update, delete pages
- **Hierarchical Navigation:** Get page children and ancestors
- **Search Capabilities:** CQL and text search across spaces
- **Comment System:** Add and retrieve page comments
- **Label Management:** Add and retrieve page labels
- **Space Navigation:** List and explore Confluence spaces

---

## 🔗 Integration with AI Clients

### 🖥️ Claude Desktop Integration

Setting up with Claude Desktop is straightforward:

**Step 1: Open Claude Desktop Settings**
Navigate to Settings → Developer → Edit config

**Step 2: Add MCP Server Configuration**

```json
{
  "mcpServers": {
    "confluence": {
      "command": "uv",
      "args": ["run", "fastmcp", "dev", "server.py"],
      "cwd": "/path/to/your/fastmcp-course"
    }
  }
}
```

### 💻 VS Code Copilot Integration

For VS Code Copilot, add to your `settings.json`:

```json
{
  "github.copilot.chat.mcp.enabled": true,
  "github.copilot.chat.mcp.servers": {
    "confluence": {
      "command": "uv",
      "args": ["run", "fastmcp", "dev", "server.py"],
      "cwd": "/path/to/your/fastmcp-course"
    }
  }
}
```

---

## 🧪 Testing and Debugging

### 🔍 MCP Inspector

FastMCP includes a built-in inspector for testing:

```bash
# Start the server with inspector
fastmcp dev server.py

# Opens web interface at http://localhost:6274
```

### 🎯 Testing Workflow

1. **Start Inspector:** Launch server with `fastmcp dev`
2. **Test Tools:** Use web interface to test individual tools
3. **Validate Responses:** Ensure proper error handling and data format
4. **Integration Testing:** Connect with Claude Desktop or VS Code

### 🐛 Common Issues and Solutions

**⚠️ Troubleshooting Tips:**

- **Context Issues:** Ensure AppContext is properly initialized before FastMCP instance
- **Tool Registration:** Call `register_tools()` after server creation
- **Environment Variables:** Verify Confluence credentials are properly set
- **API Errors:** Check logs for detailed error messages and API responses

### 📊 Example Test Results

Our comprehensive test suite covers:

```bash
# Run tests
python -m pytest

# Results
tests/test_client.py ✓ Confluence client initialization
tests/test_tools.py ✓ Page creation and retrieval
tests/test_tools.py ✓ Search functionality
tests/test_tools.py ✓ Comment and label management
```

---

## 🎯 Conclusion and Next Steps

### 🎉 What You've Accomplished

- ✅ Built a production-ready Confluence MCP server
- ✅ Implemented comprehensive page, search, and comment tools
- ✅ Integrated with Claude Desktop and VS Code Copilot
- ✅ Learned MCP core concepts and best practices
- ✅ Set up proper error handling and logging

### 🚀 What's Next

**📡 Project 2: Remote Deployment**

- Docker containerization
- Cloud deployment (GCP, AWS, Azure)
- Authentication and security
- Network transports (SSE, WebSocket)

**⚡ Project 3: Advanced Topics**

- FastAPI integration
- Sampling and monitoring
- Proxy servers
- Performance optimization

**🛠️ Build Your Own**

- Custom MCP servers
- Domain-specific tools
- MCP client development
- Custom user interfaces

### 🌟 Key Takeaways

> "MCP represents a paradigm shift in how we build AI applications. By standardizing tool integration, we're moving from custom, one-off solutions to a unified ecosystem where AI agents can seamlessly interact with any service or tool."

The Model Context Protocol is more than just a technical standard—it's the foundation for the next generation of AI applications. With MCP, you can:

- **Scale Efficiently:** Add new tools without architectural changes
- **Future-Proof:** Adapt to new AI models and services easily
- **Collaborate Better:** Share and reuse MCP servers across teams
- **Build Faster:** Focus on business logic, not integration code

### 🔗 Resources and Links

- **🎥 Full Course Video:** [FastMCP from Zero to Hero - Complete Tutorial](https://youtu.be/LUIbO0TQkfA)
- **Source Code:** [github.com/EuclideanAI/fastmcp-course](https://github.com/EuclideanAI/fastmcp-course)
- **FastMCP Documentation:** [github.com/jlowin/fastmcp](https://github.com/jlowin/fastmcp)
- **MCP Official Docs:** [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **UV Package Manager:** [github.com/astral-sh/uv](https://github.com/astral-sh/uv)
- **Atlassian Python API:** [atlassian-python-api](https://github.com/atlassian-api/atlassian-python-api)

**🎓 Ready to learn more?** [Watch the complete course](https://youtu.be/LUIbO0TQkfA) and build your next AI agent! Start with MCP and join the thousands of developers already building the future of AI integrations!

---

**FastMCP from Zero to Hero Course**
_Building Production-Ready AI Agents with Model Context Protocol_
© 2025 - Happy Coding! 🚀
