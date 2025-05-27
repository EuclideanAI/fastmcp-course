"""Tests for MCP tools."""

from typing import Any

import pytest
from fastmcp import Context

from tools.comment_tools import CommentTools
from tools.page_tools import PageTools
from tools.search_tools import SearchTools


@pytest.mark.asyncio
async def test_get_page_tool(mock_context: Context, mock_page: Any) -> None:
    """Test get_page tool."""
    page_id = "12345"
    include_body = True

    # Setup mock response
    mock_context.request_context.lifespan_context.confluence.get_page.return_value = (
        mock_page
    )

    # Call the tool
    result = await PageTools.get_page(mock_context, page_id, include_body)

    # Check that the method was called with the correct arguments
    mock_context.request_context.lifespan_context.confluence.get_page.assert_called_once_with(
        page_id=page_id,
        include_body=include_body,
    )

    # Check the result structure
    assert result["status"] == "success"
    assert result["page"] == mock_page.__dict__


@pytest.mark.asyncio
async def test_create_page_tool(mock_context: Context, mock_page: Any) -> None:
    """Test create_page tool."""
    space_key = "TEST"
    title = "Test Page"
    content = "<p>Test content</p>"
    parent_id = None
    content_format = "storage"

    # Setup mock response
    mock_context.request_context.lifespan_context.confluence.create_page.return_value = mock_page

    # Call the tool
    result = await PageTools.create_page(
        mock_context,
        title,
        content,
        space_key,
        parent_id,
        content_format,
    )

    # Check that the method was called with the correct arguments
    mock_context.request_context.lifespan_context.confluence.create_page.assert_called_once_with(
        space_key=space_key,
        title=title,
        content=content,
        parent_id=parent_id,
        content_format=content_format,
    )

    # Check the result structure
    assert result["status"] == "success"
    assert result["page"] == mock_page.__dict__


@pytest.mark.asyncio
async def test_search_confluence_tool(
    mock_context: Context, mock_search_result: Any
) -> None:
    """Test search_confluence tool."""
    query = "test"
    spaces = ["TEST"]
    content_type = "page"
    limit = 10

    # Setup mock response
    mock_context.request_context.lifespan_context.confluence.search.return_value = [
        mock_search_result
    ]

    # Call the tool
    result = await SearchTools.search_confluence(
        mock_context,
        query,
        spaces,
        content_type,
        limit,
    )

    # Check that the method was called with the correct arguments
    mock_context.request_context.lifespan_context.confluence.search.assert_called_once_with(
        query=query,
        spaces=spaces,
        content_type=content_type,
        limit=limit,
    )

    # Check the result structure
    assert result["status"] == "success"
    assert len(result["results"]) == 1
    assert result["results"][0] == mock_search_result.__dict__
    assert result["count"] == 1


@pytest.mark.asyncio
async def test_get_comments_tool(mock_context: Context, mock_comment: Any) -> None:
    """Test get_comments tool."""
    page_id = "12345"
    depth = "all"

    # Setup mock response
    mock_context.request_context.lifespan_context.confluence.get_comments.return_value = [
        mock_comment
    ]

    # Call the tool
    result = await CommentTools.get_comments(mock_context, page_id, depth)

    # Check that the method was called with the correct arguments
    mock_context.request_context.lifespan_context.confluence.get_comments.assert_called_once_with(
        page_id=page_id,
        depth=depth,
    )

    # Check the result structure
    assert result["status"] == "success"
    assert len(result["comments"]) == 1
    assert result["comments"][0] == mock_comment.__dict__
    assert result["count"] == 1


@pytest.mark.asyncio
async def test_add_label_tool(mock_context: Context) -> None:
    """Test add_label tool."""
    page_id = "12345"
    label = "test-label"
    expected_result = {"status": "success", "label": label, "page_id": page_id}

    # Setup mock response
    mock_context.request_context.lifespan_context.confluence.add_label.return_value = (
        expected_result
    )

    # Call the tool
    result = await CommentTools.add_label(mock_context, page_id, label)

    # Check that the method was called with the correct arguments
    mock_context.request_context.lifespan_context.confluence.add_label.assert_called_once_with(
        page_id=page_id,
        label=label,
    )

    # Check the result structure
    assert result == expected_result


@pytest.mark.asyncio
async def test_get_spaces_tool(mock_context: Context, mock_space: Any) -> None:
    """Test get_spaces tool."""
    limit = 25

    # Setup mock response
    mock_context.request_context.lifespan_context.confluence.get_spaces.return_value = [
        mock_space
    ]

    # Call the tool
    result = await SearchTools.get_spaces(mock_context, limit)

    # Check that the method was called with the correct arguments
    mock_context.request_context.lifespan_context.confluence.get_spaces.assert_called_once_with(
        limit=limit,
    )

    # Check the result structure
    assert result["status"] == "success"
    assert len(result["spaces"]) == 1
    assert result["spaces"][0] == mock_space.__dict__
    assert result["count"] == 1
