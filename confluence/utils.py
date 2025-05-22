"""Utility functions for Confluence client."""
import logging
from datetime import datetime
from typing import Any, Dict, Type, TypeVar, Union, cast

from confluence.models import Comment, Label, Page, SearchResult, Space

logger = logging.getLogger(__name__)

T = TypeVar('T', Page, Comment, Space, SearchResult, Label)


def parse_datetime(date_str: Union[str, None]) -> Union[datetime, None]:
    """
    Parse datetime string from Confluence API.

    Args:
        date_str: Date string in ISO format

    Returns:
        Parsed datetime object or None
    """
    if not date_str:
        return None

    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except (ValueError, TypeError) as e:
        logger.warning("Failed to parse datetime: %s - %s", date_str, e)
        return None


def parse_confluence_response(response: Dict[Any, Any], model_type: Type[T]) -> T:
    """
    Parse raw Confluence API response into appropriate model.

    Args:
        response: Raw API response dictionary
        model_type: Target model class

    Returns:
        Instantiated model object
    """
    if model_type == Page:
        return cast(T, parse_page_response(response))
    elif model_type == Comment:
        return cast(T, parse_comment_response(response))
    elif model_type == Space:
        return cast(T, parse_space_response(response))
    elif model_type == SearchResult:
        return cast(T, parse_search_result_response(response))
    elif model_type == Label:
        return cast(T, parse_label_response(response))
    else:
        raise ValueError(f"Unsupported model type: {model_type}")


def parse_page_response(response: Dict[Any, Any]) -> Page:
    """
    Parse Confluence page response.

    Args:
        response: Raw API response for a page

    Returns:
        Page object
    """
    content = None
    if "body" in response and "storage" in response["body"]:
        content = response["body"]["storage"].get("value")

    space_key = response.get("space", {}).get("key", "")

    return Page(
        id=str(response.get("id", "")),
        title=response.get("title", ""),
        space_key=space_key,
        version=int(response.get("version", {}).get("number", 0)),
        content=content,
        created=parse_datetime(response.get("created")),
        updated=parse_datetime(response.get("lastUpdated")),
        creator=response.get("history", {}).get("createdBy", {}),
        url=response.get("_links", {}).get("webui", "")
    )


def parse_comment_response(response: Dict[Any, Any]) -> Comment:
    """
    Parse Confluence comment response.

    Args:
        response: Raw API response for a comment

    Returns:
        Comment object
    """
    content = ""
    if "body" in response and "storage" in response["body"]:
        content = response["body"]["storage"].get("value", "")

    return Comment(
        id=str(response.get("id", "")),
        page_id=str(response.get("container", {}).get("id", "")),
        content=content,
        created=parse_datetime(response.get("created")),
        updated=parse_datetime(response.get("lastUpdated")),
        author=response.get("author", {}),
        parent_comment_id=str(response.get("parent", {}).get("id", ""))
                          if "parent" in response else None,
    )


def parse_space_response(response: Dict[Any, Any]) -> Space:
    """
    Parse Confluence space response.

    Args:
        response: Raw API response for a space

    Returns:
        Space object
    """
    description = None
    if "description" in response and "plain" in response["description"]:
        description = response["description"]["plain"].get("value", "")

    return Space(
        id=int(response.get("id", 0)),
        key=response.get("key", ""),
        name=response.get("name", ""),
        type=response.get("type", ""),
        description=description,
        homepage_id=str(response.get("homepage", {}).get("id", ""))
                     if "homepage" in response else None,
        status=response.get("status", "")
    )


def parse_search_result_response(response: Dict[Any, Any]) -> SearchResult:
    """
    Parse Confluence search result response.

    Args:
        response: Raw API response for a search result

    Returns:
        SearchResult object
    """
    content = None
    if "body" in response and "view" in response["body"]:
        content = response["body"]["view"].get("value", "")

    content_type = response.get("type", "")
    space_key = response.get("space", {}).get("key", "")

    return SearchResult(
        id=str(response.get("id", "")),
        title=response.get("title", ""),
        space_key=space_key,
        content_type=content_type,
        excerpt=response.get("excerpt", ""),
        url=response.get("_links", {}).get("webui", ""),
        created=parse_datetime(response.get("created")),
        updated=parse_datetime(response.get("lastUpdated")),
        content=content,
    )


def parse_label_response(response: Dict[Any, Any]) -> Label:
    """
    Parse Confluence label response.

    Args:
        response: Raw API response for a label

    Returns:
        Label object
    """
    return Label(
        id=str(response.get("id", "")),
        name=response.get("name", ""),
        prefix=response.get("prefix", ""),
        label=response.get("label", "")
    )
