"""Tests for Confluence client functionality."""
from unittest.mock import patch

import pytest

from confluence.client import ConfluenceClient


@pytest.mark.asyncio
async def test_client_initialization():
    """Test Confluence client initialization."""
    url = "https://test.atlassian.net"
    username = "test@example.com"
    api_token = "test-api-token"

    with patch("atlassian.Confluence") as mock_confluence:
        client = ConfluenceClient(url, username, api_token)

        # Check that the Atlassian Confluence client was properly initialized
        mock_confluence.assert_called_once_with(
            url=url,
            username=username,
            password=api_token,
            cloud=True,
        )


@pytest.mark.asyncio
async def test_get_page(mock_confluence_client, mock_page):
    """Test getting a page from Confluence."""
    page_id = "12345"
    include_body = True

    # Setup mock response
    mock_confluence_client.get_page.return_value = mock_page

    # Call the method
    result = await mock_confluence_client.get_page(page_id, include_body)

    # Check that the method was called with the correct arguments
    mock_confluence_client.get_page.assert_called_once_with(
        page_id=page_id,
        include_body=include_body,
    )

    # Check that the result is the mock page
    assert result == mock_page


@pytest.mark.asyncio
async def test_create_page(mock_confluence_client, mock_page):
    """Test creating a page in Confluence."""
    space_key = "TEST"
    title = "Test Page"
    content = "<p>Test content</p>"
    parent_id = None
    content_format = "storage"

    # Setup mock response
    mock_confluence_client.create_page.return_value = mock_page

    # Call the method
    result = await mock_confluence_client.create_page(
        space_key,
        title,
        content,
        parent_id,
        content_format,
    )

    # Check that the method was called with the correct arguments
    mock_confluence_client.create_page.assert_called_once_with(
        space_key=space_key,
        title=title,
        content=content,
        parent_id=parent_id,
        content_format=content_format,
    )

    # Check that the result is the mock page
    assert result == mock_page


@pytest.mark.asyncio
async def test_update_page(mock_confluence_client, mock_page):
    """Test updating a page in Confluence."""
    page_id = "12345"
    title = "Updated Test Page"
    content = "<p>Updated test content</p>"
    minor_edit = False
    content_format = "storage"
    version_comment = "Test update"

    # Setup mock response
    mock_confluence_client.update_page.return_value = mock_page

    # Call the method
    result = await mock_confluence_client.update_page(
        page_id,
        title,
        content,
        minor_edit,
        content_format,
        version_comment,
    )

    # Check that the method was called with the correct arguments
    mock_confluence_client.update_page.assert_called_once_with(
        page_id=page_id,
        title=title,
        content=content,
        minor_edit=minor_edit,
        content_format=content_format,
        version_comment=version_comment,
    )

    # Check that the result is the mock page
    assert result == mock_page


@pytest.mark.asyncio
async def test_search(mock_confluence_client, mock_search_result):
    """Test searching in Confluence."""
    query = "test"
    spaces = ["TEST"]
    content_type = "page"
    limit = 10

    # Setup mock response
    mock_confluence_client.search.return_value = [mock_search_result]

    # Call the method
    results = await mock_confluence_client.search(
        query,
        spaces,
        content_type,
        limit,
    )

    # Check that the method was called with the correct arguments
    mock_confluence_client.search.assert_called_once_with(
        query=query,
        spaces=spaces,
        content_type=content_type,
        limit=limit,
    )

    # Check that the result is a list containing the mock search result
    assert len(results) == 1
    assert results[0] == mock_search_result
