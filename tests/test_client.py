"""Tests for Confluence client functionality using proper mocking."""

from unittest.mock import MagicMock, patch

import pytest
from httpx import HTTPError

from confluence.client import ConfluenceClient
from confluence.models import Comment, Label, Page, SearchResult, Space


@pytest.mark.asyncio
async def test_client_initialization() -> None:
    """Test Confluence client initialization."""
    url = "https://test.atlassian.net"
    username = "test@example.com"
    api_token = "test-api-token"

    with patch("confluence.client.Confluence") as mock_confluence:
        client = ConfluenceClient(url, username, api_token)

        assert client.url == url
        assert client.username == username
        assert client.api_token == api_token

        mock_confluence.assert_called_once_with(
            url=url,
            username=username,
            password=api_token,
            cloud=True,
        )


@pytest.mark.asyncio
async def test_disconnect() -> None:
    """Test client disconnect method."""
    with patch("confluence.client.Confluence"):
        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )

        with patch("confluence.client.logger") as mock_logger:
            await client.disconnect()
            mock_logger.info.assert_called_once_with("Disconnecting from Confluence")


@pytest.mark.asyncio
async def test_get_page_success() -> None:
    """Test successful page retrieval."""
    page_id = "12345"
    mock_response = {
        "id": page_id,
        "title": "Test Page",
        "body": {"storage": {"value": "<p>Test content</p>"}},
        "version": {"number": 1},
        "space": {"key": "TEST", "name": "Test Space"},
    }

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.get_page_by_id.return_value = mock_response

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )
        result = await client.get_page(page_id, include_body=True)

        assert isinstance(result, Page)
        assert result.id == page_id
        assert result.title == "Test Page"
        mock_client.get_page_by_id.assert_called_once_with(
            page_id=page_id, expand="body.storage,version,space"
        )


@pytest.mark.asyncio
async def test_get_page_no_body() -> None:
    """Test page retrieval without body content."""
    page_id = "12345"
    mock_response = {
        "id": page_id,
        "title": "Test Page",
        "version": {"number": 1},
        "space": {"key": "TEST", "name": "Test Space"},
    }

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.get_page_by_id.return_value = mock_response

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )
        result = await client.get_page(page_id, include_body=False)

        assert isinstance(result, Page)
        assert result.id == page_id
        mock_client.get_page_by_id.assert_called_once_with(
            page_id=page_id, expand="version,space"
        )


@pytest.mark.asyncio
async def test_get_page_not_found() -> None:
    """Test page retrieval when page not found."""
    page_id = "nonexistent"

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.get_page_by_id.return_value = None

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )

        with pytest.raises(ValueError, match=f"Page with id {page_id} not found"):
            await client.get_page(page_id)


@pytest.mark.asyncio
async def test_create_page_success() -> None:
    """Test successful page creation."""
    space_key = "TEST"
    title = "New Page"
    content = "<p>New content</p>"

    mock_response = {
        "id": "67890",
        "title": title,
        "body": {"storage": {"value": content}},
        "version": {"number": 1},
        "space": {"key": space_key, "name": "Test Space"},
    }

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.create_page.return_value = mock_response

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )
        result = await client.create_page(space_key, title, content)

        assert isinstance(result, Page)
        assert result.title == title
        assert result.id == "67890"
        mock_client.create_page.assert_called_once_with(
            space=space_key,
            title=title,
            body=content,
            parent_id=None,
            type="page",
            representation="storage",
        )


@pytest.mark.asyncio
async def test_create_page_with_parent() -> None:
    """Test page creation with parent."""
    space_key = "TEST"
    title = "Child Page"
    content = "<p>Child content</p>"
    parent_id = 54321

    mock_response = {
        "id": "67890",
        "title": title,
        "body": {"storage": {"value": content}},
        "version": {"number": 1},
        "space": {"key": space_key, "name": "Test Space"},
    }

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.create_page.return_value = mock_response

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )
        result = await client.create_page(
            space_key, title, content, parent_id=parent_id
        )

        assert isinstance(result, Page)
        assert result.title == title
        mock_client.create_page.assert_called_once_with(
            space=space_key,
            title=title,
            body=content,
            parent_id=parent_id,
            type="page",
            representation="storage",
        )


@pytest.mark.asyncio
async def test_update_page_success() -> None:
    """Test successful page update."""
    page_id = "12345"
    title = "Updated Page"
    content = "<p>Updated content</p>"

    mock_response = {
        "id": page_id,
        "title": title,
        "body": {"storage": {"value": content}},
        "space": {"key": "TEST", "name": "Test Space"},
    }

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.update_page.return_value = mock_response

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )
        result = await client.update_page(
            page_id, title, content, version_comment="Test update"
        )

        assert isinstance(result, Page)
        assert result.title == title
        mock_client.update_page.assert_called_once_with(
            page_id=page_id,
            title=title,
            body=content,
            type="page",
            representation="storage",
            minor_edit=False,
            version_comment="Test update",
        )


@pytest.mark.asyncio
async def test_delete_page_success() -> None:
    """Test successful page deletion."""
    page_id = "12345"

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.remove_page.return_value = True

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )
        result = await client.delete_page(page_id)

        assert result["status"] == "success"
        assert result["page_id"] == page_id
        mock_client.remove_page.assert_called_once_with(page_id=page_id)


@pytest.mark.asyncio
async def test_get_page_children() -> None:
    """Test getting page children."""
    page_id = "12345"
    mock_response = [
        {
            "id": "child1",
            "title": "Child 1",
            "version": {"number": 1},
            "space": {"key": "TEST", "name": "Test Space"},
        },
        {
            "id": "child2",
            "title": "Child 2",
            "version": {"number": 1},
            "space": {"key": "TEST", "name": "Test Space"},
        },
    ]

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.get_page_child_by_type.return_value = mock_response

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )
        result = await client.get_page_children(page_id, limit=25)

        assert len(result) == 2
        assert all(isinstance(page, Page) for page in result)
        assert result[0].id == "child1"
        assert result[1].id == "child2"
        mock_client.get_page_child_by_type.assert_called_once_with(
            page_id=page_id, type="page", limit=25
        )


@pytest.mark.asyncio
async def test_get_page_ancestors() -> None:
    """Test getting page ancestors."""
    page_id = "12345"
    mock_response = {
        "id": page_id,
        "title": "Current Page",
        "ancestors": [
            {
                "id": "ancestor1",
                "title": "Ancestor 1",
                "version": {"number": 1},
                "space": {"key": "TEST", "name": "Test Space"},
            },
            {
                "id": "ancestor2",
                "title": "Ancestor 2",
                "version": {"number": 1},
                "space": {"key": "TEST", "name": "Test Space"},
            },
        ],
    }

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.get_page_by_id.return_value = mock_response

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )
        result = await client.get_page_ancestors(page_id)

        assert len(result) == 2
        assert all(isinstance(page, Page) for page in result)
        assert result[0].id == "ancestor1"
        assert result[1].id == "ancestor2"
        mock_client.get_page_by_id.assert_called_once_with(
            page_id=page_id, expand="ancestors"
        )


@pytest.mark.asyncio
async def test_search_content() -> None:
    """Test content search."""
    query = "test search"
    mock_response = {
        "results": [
            {
                "id": "result1",
                "title": "Result 1",
                "type": "page",
                "url": "/pages/result1",
                "excerpt": "Test excerpt 1",
                "content": {
                    "id": "result1",
                    "title": "Result 1",
                    "version": {"number": 1},
                    "space": {"key": "TEST", "name": "Test Space"},
                },
            },
            {
                "id": "result2",
                "title": "Result 2",
                "type": "page",
                "url": "/pages/result2",
                "excerpt": "Test excerpt 2",
                "content": {
                    "id": "result2",
                    "title": "Result 2",
                    "version": {"number": 1},
                    "space": {"key": "TEST", "name": "Test Space"},
                },
            },
        ]
    }

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.cql.return_value = mock_response

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )
        result = await client.search(query, limit=10)

        assert len(result) == 2
        assert all(isinstance(sr, SearchResult) for sr in result)
        assert result[0].id == "result1"
        assert result[1].id == "result2"
        mock_client.cql.assert_called_once_with(
            cql='text ~ "test search"', limit=10, expand="body.view,space"
        )


@pytest.mark.asyncio
async def test_get_spaces() -> None:
    """Test getting spaces."""
    mock_response = {
        "results": [
            {"key": "TEST1", "name": "Test Space 1", "type": "global"},
            {"key": "TEST2", "name": "Test Space 2", "type": "personal"},
        ]
    }

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.get_all_spaces.return_value = mock_response

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )
        result = await client.get_spaces(limit=25)

        assert len(result) == 2
        assert all(isinstance(space, Space) for space in result)
        assert result[0].key == "TEST1"
        assert result[1].key == "TEST2"
        mock_client.get_all_spaces.assert_called_once_with(
            limit=25, expand="description.plain"
        )


@pytest.mark.asyncio
async def test_get_comments() -> None:
    """Test getting page comments."""
    page_id = "12345"
    mock_response = {
        "results": [
            {
                "id": "comment1",
                "body": {"storage": {"value": "Comment 1"}},
                "version": {"number": 1, "when": "2023-01-01T00:00:00.000Z"},
                "history": {"createdBy": {"displayName": "User 1"}},
            },
            {
                "id": "comment2",
                "body": {"storage": {"value": "Comment 2"}},
                "version": {"number": 1, "when": "2023-01-02T00:00:00.000Z"},
                "history": {"createdBy": {"displayName": "User 2"}},
            },
        ]
    }

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.get_page_comments.return_value = mock_response

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )
        result = await client.get_comments(page_id, depth="all")

        assert len(result) == 2
        assert all(isinstance(comment, Comment) for comment in result)
        assert result[0].id == "comment1"
        assert result[1].id == "comment2"
        mock_client.get_page_comments.assert_called_once_with(
            content_id=page_id, expand="body.storage", depth="all"
        )


@pytest.mark.asyncio
async def test_add_comment() -> None:
    """Test adding a comment to a page."""
    page_id = "12345"
    content = "Test comment"
    mock_response = {
        "id": "new_comment",
        "body": {"storage": {"value": content}},
        "version": {"number": 1, "when": "2023-01-01T00:00:00.000Z"},
        "history": {"createdBy": {"displayName": "Test User"}},
    }

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.add_comment.return_value = mock_response

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )
        result = await client.add_comment(page_id, content)

        assert isinstance(result, Comment)
        assert result.id == "new_comment"
        mock_client.add_comment.assert_called_once_with(page_id=page_id, text=content)


@pytest.mark.asyncio
async def test_get_labels() -> None:
    """Test getting page labels."""
    page_id = "12345"
    mock_response = {
        "results": [
            {"id": "label1", "name": "important", "prefix": "global"},
            {"id": "label2", "name": "draft", "prefix": "global"},
        ]
    }

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.get_page_labels.return_value = mock_response

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )
        result = await client.get_labels(page_id)

        assert len(result) == 2
        assert all(isinstance(label, Label) for label in result)
        assert result[0].name == "important"
        assert result[1].name == "draft"
        mock_client.get_page_labels.assert_called_once_with(page_id=page_id)


@pytest.mark.asyncio
async def test_add_label() -> None:
    """Test adding a label to a page."""
    page_id = "12345"
    label = "new-label"

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.set_page_label.return_value = None

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )
        result = await client.add_label(page_id, label)

        assert result["status"] == "success"
        assert result["label"] == label
        assert result["page_id"] == page_id
        mock_client.set_page_label.assert_called_once_with(page_id=page_id, label=label)


@pytest.mark.asyncio
async def test_error_handling() -> None:
    """Test error handling in client methods."""
    page_id = "12345"

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.get_page_by_id.side_effect = HTTPError("API Error")

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )

        with pytest.raises(HTTPError):
            await client.get_page(page_id)


@pytest.mark.asyncio
async def test_client_properties() -> None:
    """Test client property access."""
    url = "https://test.atlassian.net"
    username = "test@example.com"
    api_token = "test-token"

    with patch("confluence.client.Confluence"):
        client = ConfluenceClient(url, username, api_token)

        assert client.url == url
        assert client.username == username
        assert client.api_token == api_token


@pytest.mark.asyncio
async def test_search_with_spaces_and_content_type() -> None:
    """Test search with space and content type filters."""
    query = "test search"
    spaces = ["SPACE1", "SPACE2"]
    content_type = "page"

    mock_response = {
        "results": [
            {
                "id": "result1",
                "title": "Result 1",
                "type": "page",
                "url": "/pages/result1",
                "excerpt": "Test excerpt 1",
                "content": {
                    "id": "result1",
                    "title": "Result 1",
                    "space": {"key": "SPACE1", "name": "Space 1"},
                },
            }
        ]
    }

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.cql.return_value = mock_response

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )
        result = await client.search(
            query, spaces=spaces, content_type=content_type, limit=10
        )

        assert len(result) == 1
        expected_cql = '((text ~ "test search") AND (space = "SPACE1" OR space = "SPACE2")) AND type = page'
        mock_client.cql.assert_called_once_with(
            cql=expected_cql, limit=10, expand="body.view,space"
        )


@pytest.mark.asyncio
async def test_parameter_mapping_bug() -> None:
    """Test that demonstrates what we're actually testing - parameter mapping bugs."""
    space_key = "TEST"
    title = "New Page"
    content = "<p>New content</p>"

    # Let's say there was a bug in our client code where we accidentally
    # passed 'content' instead of 'body' to the API call

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.create_page.return_value = {
            "id": "67890",
            "title": title,
            "body": {"storage": {"value": content}},
            "version": {"number": 1},
            "space": {"key": space_key, "name": "Test Space"},
        }

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )
        await client.create_page(space_key, title, content)

        # This would FAIL if our client code had a bug like:
        # self.client.create_page(content=content)  # Wrong parameter name!
        # instead of:
        # self.client.create_page(body=content)     # Correct parameter name!

        mock_client.create_page.assert_called_once_with(
            space=space_key,
            title=title,
            body=content,  # ← This assertion catches parameter mapping bugs
            parent_id=None,
            type="page",
            representation="storage",
        )


@pytest.mark.asyncio
async def test_response_processing_logic() -> None:
    """Test that we correctly process the API response."""
    space_key = "TEST"
    title = "New Page"
    content = "<p>New content</p>"

    # Test with a realistic API response structure
    api_response = {
        "id": "67890",
        "title": "New Page",
        "body": {"storage": {"value": "<p>New content</p>"}},
        "space": {"key": "TEST", "name": "Test Space"},
        # API might return extra fields we don't care about
        "_links": {"webui": "/display/TEST/New+Page"},
        "status": "current",
    }

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.create_page.return_value = api_response

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )
        result = await client.create_page(space_key, title, content)

        # We're testing that our code correctly:
        # 1. Extracts the right fields from the API response
        # 2. Creates a proper Page object
        # 3. Ignores extra fields we don't need
        assert isinstance(result, Page)
        assert result.space_key == "TEST"
        assert result.id == "67890"
        assert result.title == "New Page"
        # Note: Based on the error, Page.space might be a dict, not an object


@pytest.mark.asyncio
async def test_error_scenarios() -> None:
    """Test various error conditions."""
    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client

        # Test None response handling
        mock_client.create_page.return_value = None
        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )

        with pytest.raises(ValueError, match="Failed to create page"):
            await client.create_page("TEST", "Title", "Content")

        # Test exception handling
        mock_client.create_page.side_effect = Exception("Network error")

        with pytest.raises(Exception, match="Network error"):
            await client.create_page("TEST", "Title", "Content")


@pytest.mark.asyncio
async def test_null_response_scenarios() -> None:
    """Test handling of null responses from Confluence API."""
    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )

        # Test null response in create_page
        mock_client.create_page.return_value = None
        with pytest.raises(
            ValueError, match="Failed to create page.*or response is None"
        ):
            await client.create_page("TEST", "Title", "Content")

        # Test null response in update_page
        mock_client.update_page.return_value = None
        with pytest.raises(
            ValueError, match="Failed to update page.*or response is None"
        ):
            await client.update_page("123", "Title", "Content")

        # Test null response in get_page_children
        mock_client.get_page_child_by_type.return_value = None
        with pytest.raises(
            ValueError, match="Failed to get child pages.*or response is None"
        ):
            await client.get_page_children("123")

        # Test null response in get_spaces
        mock_client.get_all_spaces.return_value = None
        with pytest.raises(
            ValueError, match="Failed to get spaces or response is None"
        ):
            await client.get_spaces()


@pytest.mark.asyncio
async def test_search_cql_error_handling() -> None:
    """Test error handling in search method with CQL failures."""
    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client

        # Mock CQL method to raise an exception
        mock_client.cql.side_effect = Exception("CQL syntax error")

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )

        with pytest.raises(ValueError, match="CQL query failed.*Query was:"):
            await client.search("test query")


@pytest.mark.asyncio
async def test_add_label_exception_handling() -> None:
    """Test exception handling in add_label method."""
    page_id = "12345"
    label = "test-label"

    with patch("confluence.client.Confluence") as mock_confluence_class:
        mock_client = MagicMock()
        mock_confluence_class.return_value = mock_client
        mock_client.set_page_label.side_effect = Exception("API Error")

        client = ConfluenceClient(
            "https://test.atlassian.net", "test@example.com", "test-token"
        )
        result = await client.add_label(page_id, label)

        assert result["status"] == "error"
        assert result["page_id"] == page_id
        assert result["label"] == label
        assert "API Error" in result["message"]
