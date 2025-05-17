from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class ContentType(str, Enum):
    """Types of content in Confluence"""

    PAGE = "page"
    BLOGPOST = "blogpost"
    COMMENT = "comment"
    ATTACHMENT = "attachment"


@dataclass
class User:
    """Represents a Confluence user"""

    id: str
    username: str
    display_name: str
    email: Optional[str] = None


@dataclass
class Space:
    """Represents a Confluence space"""

    id: str
    key: str
    name: str
    description: Optional[str] = None
    type: Optional[str] = None  # personal, global, etc.


@dataclass
class Label:
    """Represents a Confluence content label"""

    id: str
    name: str
    prefix: str = "global"


@dataclass
class Content:
    """Base class for Confluence content"""

    id: str
    title: str
    type: ContentType
    space: Space
    creator: User
    version: Dict[str, Any]
    body: Optional[Dict[str, Any]] = None
    ancestors: Optional[List["Content"]] = None
    children: Optional[List["Content"]] = None
    labels: Optional[List[Label]] = None
    status: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> "Content":
        """Create a Content object from API response data"""
        space_data = api_data.get("space", {})
        space = Space(
            id=str(space_data.get("id", "")),  # Convert to string as API may return int
            key=space_data.get("key", ""),
            name=space_data.get("name", ""),
            description=space_data.get("description", None),
            type=space_data.get("type", None),
        )

        creator_data = api_data.get("creator", {})
        creator = User(
            id=creator_data.get("accountId", ""),
            username=creator_data.get("username", ""),
            display_name=creator_data.get("displayName", ""),
            email=creator_data.get("email", ""),
        )

        # Process labels if present
        labels_data = api_data.get("metadata", {}).get("labels", {}).get("results", [])
        labels = (
            [
                Label(
                    id=label.get("id", ""),
                    name=label.get("name", ""),
                    prefix=label.get("prefix", "global"),
                )
                for label in labels_data
            ]
            if labels_data
            else None
        )

        # Process ancestors if present
        ancestors_data = api_data.get("ancestors", [])
        ancestors = []
        if ancestors_data:
            for ancestor in ancestors_data:
                # Create simplified Content objects for ancestors
                ancestors.append(cls(
                    id=ancestor.get("id", ""),
                    title=ancestor.get("title", ""),
                    type=ContentType(ancestor.get("type", "page")),
                    space=space,  # Use same space as parent
                    creator=creator,  # This is a simplification
                    version={},  # Simplified
                    status=ancestor.get("status", None)
                ))

        # Process body in different formats
        body = {}
        if "body" in api_data:
            if isinstance(api_data["body"], dict):
                body = api_data["body"]
            else:
                # Handle case where body might be a direct value
                body = {"content": api_data["body"]}

        # Handle children data
        children_data = api_data.get("children", {})
        children = []

        # For each content type in children, create simplified Content objects
        for _content_type, content_list in children_data.items():
            if isinstance(content_list, dict) and "results" in content_list:
                for child in content_list.get("results", []):
                    children.append(cls(
                        id=child.get("id", ""),
                        title=child.get("title", ""),
                        type=ContentType(child.get("type", "page")),
                        space=space,  # Use same space as parent
                        creator=creator,  # This is a simplification
                        version={},  # Simplified
                    ))

        return cls(
            id=api_data.get("id", ""),
            title=api_data.get("title", ""),
            type=ContentType(api_data.get("type", "page")),
            space=space,
            creator=creator,
            version=api_data.get("version", {}),
            body=body,
            ancestors=ancestors if ancestors else None,
            children=children if children else None,
            labels=labels,
            status=api_data.get("status", None),
        )


@dataclass
class Page(Content):
    """Represents a Confluence page"""

    parent_id: Optional[str] = None

    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> "Page":
        """Create a Page object from API response data"""
        content = super().from_api_response(api_data)

        # Extract parent ID if ancestors exist
        ancestors = api_data.get("ancestors", [])
        parent_id = ancestors[-1].get("id") if ancestors else None

        return cls(
            id=content.id,
            title=content.title,
            type=content.type,
            space=content.space,
            creator=content.creator,
            version=content.version,
            body=content.body,
            labels=content.labels,
            parent_id=parent_id,
        )


@dataclass
class Comment(Content):
    """Represents a comment on a Confluence page"""

    container_id: str = ""

    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> "Comment":
        """Create a Comment object from API response data"""
        content = super().from_api_response(api_data)

        container = api_data.get("container", {})
        container_id = container.get("id", "") if container else ""

        return cls(
            id=content.id,
            title=content.title,
            type=content.type,
            space=content.space,
            creator=content.creator,
            version=content.version,
            body=content.body,
            labels=content.labels,
            container_id=container_id,
        )


@dataclass
class SearchResult:
    """Container for search results"""

    results: List[Content]
    start: int
    limit: int
    size: int
    total_size: Optional[int] = None

    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> "SearchResult":
        """Create a SearchResult object from API response data"""
        results = []
        for result in api_data.get("results", []):
            content_type = result.get("type", "page")
            if content_type == ContentType.PAGE:
                results.append(Page.from_api_response(result))
            elif content_type == ContentType.COMMENT:
                results.append(Comment.from_api_response(result))
            else:
                results.append(Content.from_api_response(result))

        return cls(
            results=results,
            start=api_data.get("start", 0),
            limit=api_data.get("limit", 0),
            size=api_data.get("size", 0),
            total_size=api_data.get("totalSize", None),
        )
