"""Test configuration and fixtures."""

from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastmcp import Context

from config import Config, ConfluenceConfig
from confluence.client import ConfluenceClient
from confluence.models import Comment, Label, Page, SearchResult, Space


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


@pytest.fixture
def mock_search_result() -> SearchResult:
    """Return a mock search result for testing."""
    return SearchResult(
        id="12345",
        title="Test Page",
        space_key="TEST",
        content_type="page",
        excerpt="This is a test page",
    )


@pytest.fixture
def mock_space() -> Space:
    """Return a mock Confluence space for testing."""
    return Space(
        id=1,
        key="TEST",
        name="Test Space",
        type="global",
        description="Test space description",
    )


@pytest.fixture
def mock_comment() -> Comment:
    """Return a mock Confluence comment for testing."""
    return Comment(
        id="54321",
        page_id="12345",
        content="<p>Test comment</p>",
    )


@pytest.fixture
def mock_label() -> Label:
    """Return a mock Confluence label for testing."""
    return Label(
        id="98765",
        name="test-label",
        prefix="global",
        label="test-label",
    )


@pytest.fixture
def mock_confluence_client() -> AsyncMock:
    """Return a mock Confluence client for testing."""
    mock_client = AsyncMock(spec=ConfluenceClient)
    return mock_client


@pytest.fixture
async def mock_context(
    mock_confluence_client: ConfluenceClient
) -> AsyncGenerator[Context, None]:
    """Return a mock FastMCP context for testing."""
    # Create a mock AppContext with the mock Confluence client
    mock_app_context = MagicMock()
    mock_app_context.confluence = mock_confluence_client

    # Create a mock Context with lifespan_context attribute
    mock_ctx = MagicMock(spec=Context)
    mock_ctx.lifespan_context = mock_app_context  # Direct access to lifespan_context

    yield mock_ctx
