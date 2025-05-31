"""Tests for Confluence utility functions."""

from datetime import datetime
from typing import Any, Dict
from unittest.mock import patch

import pytest

from confluence.models import Comment, Label, Page, SearchResult, Space
from confluence.utils import (
    parse_comment_response,
    parse_confluence_response,
    parse_datetime,
    parse_label_response,
    parse_page_response,
    parse_search_result_response,
    parse_space_response,
)


class TestParseDatetime:
    """Test parse_datetime function."""

    def test_parse_datetime_valid_iso_format(self) -> None:
        """Test parsing valid ISO datetime string."""
        date_str = "2023-12-01T10:30:00.000Z"
        result = parse_datetime(date_str)

        assert result is not None
        assert isinstance(result, datetime)
        assert result.year == 2023
        assert result.month == 12
        assert result.day == 1
        assert result.hour == 10
        assert result.minute == 30

    def test_parse_datetime_valid_without_z(self) -> None:
        """Test parsing valid datetime string without Z suffix."""
        date_str = "2023-12-01T10:30:00.000+00:00"
        result = parse_datetime(date_str)

        assert result is not None
        assert isinstance(result, datetime)

    def test_parse_datetime_none_input(self) -> None:
        """Test parsing None input."""
        result = parse_datetime(None)
        assert result is None

    def test_parse_datetime_empty_string(self) -> None:
        """Test parsing empty string."""
        result = parse_datetime("")
        assert result is None

    @patch("confluence.utils.logger")
    def test_parse_datetime_invalid_format(self, mock_logger: Any) -> None:
        """Test parsing invalid datetime format."""
        date_str = "invalid-date"
        result = parse_datetime(date_str)

        assert result is None
        mock_logger.warning.assert_called_once()

    @patch("confluence.utils.logger")
    def test_parse_datetime_type_error(self, mock_logger: Any) -> None:
        """Test parsing when TypeError occurs."""
        # Passing an int instead of string should cause TypeError
        result = parse_datetime(123)  # type: ignore

        assert result is None
        mock_logger.warning.assert_called_once()


class TestParseConfluenceResponse:
    """Test parse_confluence_response function."""

    def test_parse_page_response(self) -> None:
        """Test parsing response as Page."""
        response = {"id": "123", "title": "Test Page"}

        with patch("confluence.utils.parse_page_response") as mock_parse:
            mock_parse.return_value = Page(
                id="123", title="Test Page", space_key="", version=1
            )
            result = parse_confluence_response(response, Page)

            mock_parse.assert_called_once_with(response)
            assert isinstance(result, Page)

    def test_parse_comment_response(self) -> None:
        """Test parsing response as Comment."""
        response = {"id": "123", "content": "Test comment"}

        with patch("confluence.utils.parse_comment_response") as mock_parse:
            mock_parse.return_value = Comment(
                id="123", page_id="", content="Test comment"
            )
            result = parse_confluence_response(response, Comment)

            mock_parse.assert_called_once_with(response)
            assert isinstance(result, Comment)

    def test_parse_space_response(self) -> None:
        """Test parsing response as Space."""
        response = {"id": 123, "key": "TEST", "name": "Test Space"}

        with patch("confluence.utils.parse_space_response") as mock_parse:
            mock_parse.return_value = Space(
                id=123, key="TEST", name="Test Space", type=""
            )
            result = parse_confluence_response(response, Space)

            mock_parse.assert_called_once_with(response)
            assert isinstance(result, Space)

    def test_parse_search_result_response(self) -> None:
        """Test parsing response as SearchResult."""
        response = {"id": "123", "title": "Test Result"}

        with patch("confluence.utils.parse_search_result_response") as mock_parse:
            mock_parse.return_value = SearchResult(
                id="123", title="Test Result", space_key="", content_type="", excerpt=""
            )
            result = parse_confluence_response(response, SearchResult)

            mock_parse.assert_called_once_with(response)
            assert isinstance(result, SearchResult)

    def test_parse_label_response(self) -> None:
        """Test parsing response as Label."""
        response = {"id": "123", "name": "test-label"}

        with patch("confluence.utils.parse_label_response") as mock_parse:
            mock_parse.return_value = Label(
                id="123", name="test-label", prefix="", label=""
            )
            result = parse_confluence_response(response, Label)

            mock_parse.assert_called_once_with(response)
            assert isinstance(result, Label)

    def test_parse_unsupported_model_type(self) -> None:
        """Test parsing with unsupported model type."""
        response = {"id": "123"}

        class UnsupportedModel:
            pass

        with pytest.raises(ValueError, match="Unsupported model type"):
            parse_confluence_response(response, UnsupportedModel)  # type: ignore


class TestParsePageResponse:
    """Test parse_page_response function."""

    def test_parse_complete_page_response(self) -> None:
        """Test parsing complete page response."""
        response = {
            "id": "123456",
            "title": "Test Page",
            "space": {"key": "TEST"},
            "version": {"number": 5},
            "body": {"storage": {"value": "<p>Page content</p>"}},
            "created": "2023-12-01T10:30:00.000Z",
            "lastUpdated": "2023-12-02T15:45:00.000Z",
            "history": {"createdBy": {"displayName": "John Doe"}},
            "_links": {"webui": "/pages/123456"},
        }

        result = parse_page_response(response)

        assert result.id == "123456"
        assert result.title == "Test Page"
        assert result.space_key == "TEST"
        assert result.version == 5
        assert result.content == "<p>Page content</p>"
        assert result.created is not None
        assert result.updated is not None
        assert result.url == "/pages/123456"

    def test_parse_minimal_page_response(self) -> None:
        """Test parsing minimal page response with defaults."""
        response: Dict[str, Any] = {}

        result = parse_page_response(response)

        assert result.id == ""
        assert result.title == ""
        assert result.space_key == ""
        assert result.version == 0
        assert result.content is None
        assert result.created is None
        assert result.updated is None
        assert result.url == ""

    def test_parse_page_response_without_body(self) -> None:
        """Test parsing page response without body content."""
        response = {
            "id": "123",
            "title": "Test Page",
            "space": {"key": "TEST"},
            "version": {"number": 1},
        }

        result = parse_page_response(response)

        assert result.content is None


class TestParseCommentResponse:
    """Test parse_comment_response function."""

    def test_parse_complete_comment_response(self) -> None:
        """Test parsing complete comment response."""
        response = {
            "id": "comment123",
            "container": {"id": "page456"},
            "body": {"storage": {"value": "<p>Comment content</p>"}},
            "created": "2023-12-01T10:30:00.000Z",
            "lastUpdated": "2023-12-01T11:00:00.000Z",
            "author": {"displayName": "Jane Doe"},
            "parent": {"id": "comment100"},
        }

        result = parse_comment_response(response)

        assert result.id == "comment123"
        assert result.page_id == "page456"
        assert result.content == "<p>Comment content</p>"
        assert result.created is not None
        assert result.updated is not None
        assert result.parent_comment_id == "comment100"

    def test_parse_minimal_comment_response(self) -> None:
        """Test parsing minimal comment response."""
        response: Dict[str, Any] = {}

        result = parse_comment_response(response)

        assert result.id == ""
        assert result.page_id == ""
        assert result.content == ""
        assert result.created is None
        assert result.updated is None
        assert result.parent_comment_id is None

    def test_parse_comment_response_without_parent(self) -> None:
        """Test parsing comment response without parent."""
        response = {
            "id": "comment123",
            "container": {"id": "page456"},
            "body": {"storage": {"value": "Comment content"}},
        }

        result = parse_comment_response(response)

        assert result.parent_comment_id is None


class TestParseSpaceResponse:
    """Test parse_space_response function."""

    def test_parse_complete_space_response(self) -> None:
        """Test parsing complete space response."""
        response = {
            "id": 123,
            "key": "TEST",
            "name": "Test Space",
            "type": "global",
            "description": {"plain": {"value": "Test space description"}},
            "homepage": {"id": "home123"},
            "status": "current",
        }

        result = parse_space_response(response)

        assert result.id == 123
        assert result.key == "TEST"
        assert result.name == "Test Space"
        assert result.type == "global"
        assert result.description == "Test space description"
        assert result.homepage_id == "home123"
        assert result.status == "current"

    def test_parse_minimal_space_response(self) -> None:
        """Test parsing minimal space response."""
        response: Dict[str, Any] = {}

        result = parse_space_response(response)

        assert result.id == 0
        assert result.key == ""
        assert result.name == ""
        assert result.type == ""
        assert result.description is None
        assert result.homepage_id is None
        assert result.status == ""

    def test_parse_space_response_without_description(self) -> None:
        """Test parsing space response without description."""
        response = {
            "id": 123,
            "key": "TEST",
            "name": "Test Space",
            "type": "global",
        }

        result = parse_space_response(response)

        assert result.description is None

    def test_parse_space_response_without_homepage(self) -> None:
        """Test parsing space response without homepage."""
        response = {
            "id": 123,
            "key": "TEST",
            "name": "Test Space",
            "type": "global",
        }

        result = parse_space_response(response)

        assert result.homepage_id is None


class TestParseSearchResultResponse:
    """Test parse_search_result_response function."""

    def test_parse_complete_search_result_response(self) -> None:
        """Test parsing complete search result response."""
        response = {
            "id": "result123",
            "title": "Search Result",
            "space": {"key": "TEST"},
            "type": "page",
            "excerpt": "This is a search result excerpt",
            "body": {"view": {"value": "<p>Full content</p>"}},
            "created": "2023-12-01T10:30:00.000Z",
            "lastUpdated": "2023-12-02T15:45:00.000Z",
            "_links": {"webui": "/pages/result123"},
        }

        result = parse_search_result_response(response)

        assert result.id == "result123"
        assert result.title == "Search Result"
        assert result.space_key == "TEST"
        assert result.content_type == "page"
        assert result.excerpt == "This is a search result excerpt"
        assert result.content == "<p>Full content</p>"
        assert result.created is not None
        assert result.updated is not None
        assert result.url == "/pages/result123"

    def test_parse_minimal_search_result_response(self) -> None:
        """Test parsing minimal search result response."""
        response: Dict[str, Any] = {}

        result = parse_search_result_response(response)

        assert result.id == ""
        assert result.title == ""
        assert result.space_key == ""
        assert result.content_type == ""
        assert result.excerpt == ""
        assert result.content is None
        assert result.created is None
        assert result.updated is None
        assert result.url == ""


class TestParseLabelResponse:
    """Test parse_label_response function."""

    def test_parse_complete_label_response(self) -> None:
        """Test parsing complete label response."""
        response = {
            "id": "label123",
            "name": "test-label",
            "prefix": "global",
            "label": "test-label-full",
        }

        result = parse_label_response(response)

        assert result.id == "label123"
        assert result.name == "test-label"
        assert result.prefix == "global"
        assert result.label == "test-label-full"

    def test_parse_minimal_label_response(self) -> None:
        """Test parsing minimal label response."""
        response: Dict[str, Any] = {}

        result = parse_label_response(response)

        assert result.id == ""
        assert result.name == ""
        assert result.prefix == ""
        assert result.label == ""
