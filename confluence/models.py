"""Models for Confluence objects."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Page:
    """Represents a Confluence page."""

    id: str
    title: str
    space_key: str
    version: int
    content: Optional[str] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    creator: Optional[Dict[str, Any]] = None
    url: Optional[str] = None


@dataclass
class SearchResult:
    """Represents a Confluence search result."""

    id: str
    title: str
    space_key: str
    content_type: str
    excerpt: Optional[str] = None
    url: Optional[str] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    content: Optional[str] = None


@dataclass
class Space:
    """Represents a Confluence space."""

    id: int
    key: str
    name: str
    type: str
    description: Optional[str] = None
    homepage_id: Optional[str] = None
    status: Optional[str] = None


@dataclass
class Comment:
    """Represents a Confluence comment."""

    id: str
    page_id: str
    content: str
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
    author: Optional[Dict[str, Any]] = None
    parent_comment_id: Optional[str] = None


@dataclass
class Label:
    """Represents a Confluence label."""

    id: str
    name: str
    prefix: str
    label: str
