# Project 2 - FastMCP Server: Testing, Network, Authentication & Remote Deployment

A comprehensive guide to building a production-ready Model Context Protocol (MCP) server with advanced features including unit testing, transport protocols, authentication mechanisms, and remote server deployment.

## Description

Project 2 extends the basic Confluence MCP server from Project 1 by adding enterprise-grade features essential for production deployments. This project focuses on code quality through comprehensive testing, secure communication protocols, robust authentication systems, and scalable remote deployment strategies.

## Learning Objectives

By completing this project, you will:

- Implement comprehensive unit testing for MCP servers using pytest
- Understand and implement different transport protocols for MCP communication
- Integrate authentication mechanisms for secure API access
- Deploy MCP servers to remote environments with proper configuration
- Learn best practices for production-ready MCP server development

## Features

### 🧪 Unit Testing

- **Comprehensive Test Suite**: Complete test coverage for all MCP tools and client operations
- **Mock Testing**: Proper mocking of external API calls for isolated testing
- **Fixture Management**: Reusable test fixtures for consistent test environments
- **Coverage Reporting**: Automated coverage tracking and reporting
- **CI/CD Integration**: GitHub Actions workflows for automated testing

### 🌐 Transport Protocols

- **StdIO**: Standard I/O for local client/server communication
- **Server-Sent Events (SSE)**: Streaming updates for long-running operations
- **Streamable HTTP**:

### 🔐 Authentication & Security

- **Multiple Auth Methods**: Support for API tokens, OAuth 2.0, and JWT
- **Input Validation**: Comprehensive request validation and sanitization
- **Audit Logging**: Security event logging and monitoring

### 🚀 Remote Server Deployment

- **Container Support**: Docker containerization for consistent deployments
- **Cloud Deployment**: Deploy to AWS, GCP, Azure, or other cloud providers
- **Environment Management**: Proper configuration management for different environments
- **Health Checks**: Endpoint monitoring and health verification

## Prerequisites

- Completion of Project 1 (Basic Confluence MCP Server)
- Python 3.10+
- Docker (for containerization)
- Cloud provider account (AWS, GCP, Azure, etc.) for remote deployment
- Confluence Cloud instance with API access

## Pytest Fundamentals: A Quick Tutorial

Before diving into the implementation, let's understand the key pytest concepts used throughout this project. This 5-10 minute guide covers the essential testing patterns you'll encounter.

### What is Pytest?

Pytest is Python's most popular testing framework. It makes writing and running tests simple while providing powerful features for complex testing scenarios.

### Key Concepts

#### 1. Basic Test Structure

Tests are functions that start with `test_` and use `assert` statements:

```python
def test_basic_example():
    """Test that demonstrates basic assertion."""
    result = 2 + 2
    assert result == 4
    assert result != 5
```

#### 2. Fixtures: Reusable Test Data

Fixtures provide consistent test data and setup. They're decorated with `@pytest.fixture` and can be reused across multiple tests.

**From our `conftest.py`:**

```python
@pytest.fixture
def mock_config() -> Config:
    """Return a mock configuration for testing."""
    confluence_config = ConfluenceConfig(
        url="https://test.atlassian.net",
        username="test@example.com",
        api_token="test-api-token",
    )
    return Config(confluence=confluence_config, debug=True)

@pytest.fixture
def mock_page() -> Page:
    """Return a mock Confluence page for testing."""
    return Page(
        id="12345",
        title="Test Page",
        space_key="TEST",
        version=1,
        content="<p>Test content</p>",
    )
```

**Usage in tests:**

```python
def test_config_values(mock_config):
    """Test uses the mock_config fixture."""
    assert mock_config.confluence.url == "https://test.atlassian.net"
    assert mock_config.debug is True
```

#### 3. Mocking with @patch

Mocking replaces real objects with fake ones during testing. Use `@patch` to mock external dependencies:

**From our `test_client.py`:**

```python
from unittest.mock import patch

@patch("confluence.client.Confluence")
async def test_client_initialization(mock_confluence):
    """Test that demonstrates patching external dependencies."""
    client = ConfluenceClient("https://test.atlassian.net", "test@example.com", "token")

    # Verify the mock was called correctly
    mock_confluence.assert_called_once_with(
        url="https://test.atlassian.net",
        username="test@example.com",
        password="token",
        cloud=True,
    )
```

**Environment variable mocking:**

```python
@patch.dict(os.environ, {"CONFLUENCE_URL": "https://test.com"})
def test_config_from_env():
    """Test loading config from environment variables."""
    config = load_config()
    assert config.confluence.url == "https://test.com"
```

#### 4. Async Testing

For async functions, use `@pytest.mark.asyncio`:

**From our `test_tools.py`:**

```python
@pytest.mark.asyncio
async def test_get_page_tool(mock_context, mock_page):
    """Test async MCP tool functionality."""
    page_id = "12345"

    # Setup mock response
    mock_context.request_context.lifespan_context.confluence.get_page.return_value = mock_page

    # Call the async tool
    result = await PageTools.get_page(mock_context, page_id, True)

    # Verify the mock was called
    mock_context.request_context.lifespan_context.confluence.get_page.assert_called_once_with(
        page_id=page_id,
        include_body=True,
    )
```

#### 5. Exception Testing

Test that your code properly handles errors using `pytest.raises`:

**From our `test_client.py`:**

```python
async def test_page_not_found():
    """Test handling of missing pages."""
    page_id = "nonexistent"

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.get_page_by_id.return_value = None

        client = ConfluenceClient("https://test.atlassian.net", "test@example.com", "token")

        # Test that the right exception is raised
        with pytest.raises(ValueError, match=f"Page with id {page_id} not found"):
            await client.get_page(page_id)
```

#### 6. Parametrized Testing

Run the same test with different inputs using `@pytest.mark.parametrize`:

**From our `test_config.py`:**

```python
@pytest.mark.parametrize(
    "debug_value,expected",
    [
        ("true", True),
        ("TRUE", True),
        ("1", True),
        ("false", False),
        ("0", False),
        ("invalid", False),
    ],
)
def test_debug_flag_parsing(debug_value, expected):
    """Test parsing various debug flag values."""
    with patch.dict(os.environ, {"DEBUG": debug_value}):
        config = load_config()
        assert config.debug == expected
```

### Common Testing Patterns in Our Project

#### 1. Setup-Action-Assert Pattern

```python
def test_example():
    # Setup: Prepare test data
    mock_data = {"key": "value"}

    # Action: Call the function being tested
    result = process_data(mock_data)

    # Assert: Verify the result
    assert result["processed"] is True
```

#### 2. Mock Configuration Pattern

```python
@patch("module.external_service")
def test_service_integration(mock_service):
    # Configure mock behavior
    mock_service.return_value = "expected_response"

    # Test the integration
    result = call_service()

    # Verify both result and interaction
    assert result == "expected_response"
    mock_service.assert_called_once()
```

#### 3. Context Manager Testing

```python
def test_context_manager():
    """Test proper resource management."""
    with patch("module.resource") as mock_resource:
        with MyContextManager() as manager:
            manager.do_something()

        # Verify cleanup was called
        mock_resource.cleanup.assert_called_once()
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_client.py

# Run tests matching a pattern
pytest -k "test_config"

# Run with coverage reporting
pytest --cov=confluence --cov-report=html
```

### Test Organization in Our Project

- **`conftest.py`**: Shared fixtures and test configuration
- **`test_client.py`**: Tests for Confluence API client
- **`test_tools.py`**: Tests for MCP tools (page, search, comment tools)
- **`test_config.py`**: Tests for configuration loading and validation
- **`test_server.py`**: Tests for server initialization and lifecycle
- **`test_utils.py`**: Tests for utility functions

This foundation will help you understand the testing patterns used throughout Project 2. Each test follows these principles to ensure reliable, maintainable code.

## Implementation Guide

### Phase 1: Unit Testing Foundation

#### 1.1 Enhanced Test Configuration

```python
# tests/conftest.py - Enhanced with more fixtures and configuration
```

#### 1.2 Comprehensive Client Testing

- Mock Confluence API responses
- Test error handling and retry logic
- Validate authentication flows
- Test rate limiting behavior

#### 1.3 Tool Testing Strategy

- Unit tests for each MCP tool
- Integration tests for tool combinations
- Performance testing for large operations
- Security testing for input validation

### Phase 2: Transport Protocol Implementation

#### 2.1 Standard I/O

- RESTful endpoint design
- Request/response validation
- Error handling and status codes
- Content negotiation

#### 2.2 Server-Sent Events (SSE)

- Streaming updates for long operations
- Event formatting and client handling
- Connection lifecycle management
- Fallback mechanisms

#### 2.3 Streamable HTTP

### Phase 3: Authentication & Security

#### 3.1 Multi-Auth Support

```python
# confluence/auth.py - Authentication handler implementation
```

#### 3.2 Security Enhancements

- Input validation and sanitization
- Rate limiting implementation
- CORS configuration
- Security headers and middleware

#### 3.3 Audit and Monitoring

- Security event logging
- Performance monitoring
- Error tracking and alerting
- Usage analytics

### Phase 4: Remote Deployment

#### 4.1 Containerization

```dockerfile
# deployment/Dockerfile - Production-ready container
```

#### 4.2 Cloud Deployment Options

**Google Cloud Platform:**

- Cloud Run for serverless container deployment
- Cloud Load Balancing for traffic management
- Cloud Monitoring for observability
- Cloud IAM for authentication

## Resources

- [FastMCP Documentation](https://fastmcp.readthedocs.io/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Confluence REST API Documentation](https://developer.atlassian.com/cloud/confluence/rest/v1/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Kubernetes Deployment Guide](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

## Next Steps

After completing Project 2, you'll be ready for:

- **Project 3**: Advanced topics including Infra as Code, CI/CD pipeline, FastAPI mounting, sampling, and proxy servers
- **Production Deployment**: Real-world deployment with monitoring and scaling
