"""Confluence client implementation."""
import asyncio
import logging
from typing import Any, Dict, List, Optional

import backoff
from atlassian import Confluence
from httpx import HTTPError

from confluence.models import Comment, Label, Page, SearchResult, Space
from confluence.utils import parse_confluence_response

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="confluence_client.log",
)

logger = logging.getLogger(__name__)


class ConfluenceClient:
    """Client for interacting with Atlassian Confluence."""

    def __init__(self, url: str, username: str, api_token: str):
        """
        Initialize the Confluence client.

        Args:
            url: Base URL for Confluence instance
            username: Username for authentication
            api_token: API token for authentication
        """
        self.url = url
        self.username = username
        self.api_token = api_token

        # Initialize the Atlassian Python API client
        self.client = Confluence(
            url=url,
            username=username,
            password=api_token,
            cloud=True,  # Assuming cloud instance; set to False if on-prem
        )

        logger.info("Initialized Confluence client for %s", url)

    async def disconnect(self) -> None:
        """Clean up resources when shutting down."""
        # The Atlassian Python API client doesn't have a specific disconnect method
        # but we include this for future-proofing and consistency
        logger.info("Disconnecting from Confluence")

    @backoff.on_exception(
        backoff.expo,
        (HTTPError, ConnectionError),
        max_tries=3,
        max_time=30,
    )
    async def get_page(self, page_id: str, include_body: bool = True) -> Page:
        """
        Get Confluence page content and metadata by ID.

        Args:
            page_id: The ID of the Confluence page
            include_body: Whether to include the full page content

        Returns:
            Page object with page information
        """
        # Run in executor since Atlassian API is synchronous
        expand = "body.storage,version,space" if include_body else "version,space"

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.get_page_by_id(
                page_id=page_id,
                expand=expand
            )
        )

        # Log more safely with specific fields rather than the entire response
        logger.info(f"Confluence get_page response for page_id {page_id}: status={'success' if response else 'failure'}")
        if response:
            try:
                # Log a few key fields for debugging, not the entire response
                logger.info(f"Page title: {response.get('title', 'N/A')}, ID: {response.get('id', 'N/A')}")
            except Exception as e:
                logger.error(f"Error while logging response: {str(e)}")

        if response is None:
            raise ValueError(f"Page with id {page_id} not found or response is None")
        return parse_confluence_response(response, Page)

    @backoff.on_exception(
        backoff.expo,
        (HTTPError, ConnectionError),
        max_tries=3,
        max_time=30,
    )
    async def create_page(
        self,
        space_key: str,
        title: str,
        content: str,
        parent_id: Optional[str] = None,
        content_format: str = "storage"
    ) -> Page:
        """
        Create a new Confluence page.

        Args:
            space_key: Key of the space where the page will be created
            title: Title of the page
            content: Content of the page
            parent_id: Optional ID of the parent page for hierarchical content
            content_format: Content format ('storage' for XHTML, 'wiki' for wiki markup)

        Returns:
            Page object with created page information
        """
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.create_page(
                space=space_key,
                title=title,
                body=content,
                parent_id=parent_id,
                type="page",
                representation=content_format
            )
        )

        if response is None:
            raise ValueError(f"Failed to create page '{title}' in space '{space_key}' or response is None")
        return parse_confluence_response(response, Page)

    @backoff.on_exception(
        backoff.expo,
        (HTTPError, ConnectionError),
        max_tries=3,
        max_time=30,
    )
    async def update_page(
        self,
        page_id: str,
        title: str,
        content: str,
        minor_edit: bool = False,
        content_format: str = "storage",
        version_comment: Optional[str] = None,
    ) -> Page:
        """
        Update an existing Confluence page.

        Args:
            page_id: ID of the page to update
            title: New title of the page
            content: New content of the page
            minor_edit: Whether this is a minor edit
            content_format: Content format ('storage' for XHTML, 'wiki' for wiki markup)
            version_comment: Optional comment for this version

        Returns:
            Page object with updated page information
        """
        # Get page info for version if needed in the future
        # The commented-out code shows we might need the version later
        # current_page = await self.get_page(page_id, include_body=False)

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.update_page(
                page_id=page_id,
                title=title,
                body=content,
                type="page",
                representation=content_format,
                # version=current_page.version + 1,
                minor_edit=minor_edit,
                version_comment=version_comment
            )
        )
        # Log the response status for debugging
        logger.info(f"Confluence update_page response for page_id {page_id}: status={'success' if response else 'failure'}")

        if response is None:
            raise ValueError(f"Failed to update page with id {page_id} or response is None")
        return parse_confluence_response(response, Page)

    @backoff.on_exception(
        backoff.expo,
        (HTTPError, ConnectionError),
        max_tries=3,
        max_time=30,
    )
    async def delete_page(self, page_id: str) -> Dict[str, Any]:
        """
        Delete a Confluence page.

        Args:
            page_id: ID of the page to delete

        Returns:
            Dictionary with operation result
        """
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.remove_page(page_id=page_id)
        )

        # This typically returns a boolean or None
        return {"status": "success" if response else "error", "page_id": page_id}

    @backoff.on_exception(
        backoff.expo,
        (HTTPError, ConnectionError),
        max_tries=3,
        max_time=30,
    )
    async def get_page_children(
        self,
        page_id: str,
        limit: int = 25
    ) -> List[Page]:
        """
        Get child pages of a Confluence page.

        Args:
            page_id: ID of the parent page
            limit: Maximum number of children to return

        Returns:
            List of Page objects for child pages
        """
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.get_page_child_by_type(
                page_id=page_id,
                type="page",
                limit=limit
            )
        )

        if response is None:
            raise ValueError(f"Failed to get child pages for page with id {page_id} or response is None")
        return [parse_confluence_response(child, Page) for child in response]

    @backoff.on_exception(
        backoff.expo,
        (HTTPError, ConnectionError),
        max_tries=3,
        max_time=30,
    )
    async def get_page_ancestors(self, page_id: str) -> List[Page]:
        """
        Get ancestor (parent) pages of a Confluence page.

        Args:
            page_id: ID of the page

        Returns:
            List of Page objects for ancestor pages
        """
        # Get page with ancestors expanded
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.get_page_by_id(
                page_id=page_id,
                expand="ancestors"
            )
        )

        if response is None:
            raise ValueError(f"Page with id {page_id} not found or response is None")

        # Extract and parse ancestors from the response
        ancestors = response.get("ancestors", [])
        return [parse_confluence_response(ancestor, Page) for ancestor in ancestors]

    @backoff.on_exception(
        backoff.expo,
        (HTTPError, ConnectionError),
        max_tries=3,
        max_time=30,
    )
    async def search(
        self,
        query: str,
        spaces: Optional[List[str]] = None,
        content_type: Optional[str] = None,
        limit: int = 10,
    ) -> List[SearchResult]:
        """
        Search Confluence content using CQL or text search.

        Args:
            query: Search terms or CQL query
            spaces: Optional list of space keys to restrict search
            content_type: Optional content type filter (e.g., "page", "blogpost")
            limit: Maximum number of results to return

        Returns:
            List of search results
        """
        # Construct CQL query if simple text search
        if " " in query and not any(op in query for op in ["~", "=", "<", ">"]):
            # This is a simple text search, convert to CQL
            cql = f'text ~ "{query}"'

            # Add space restrictions if provided
            if spaces:
                space_clause = " OR ".join([f'space = "{space}"' for space in spaces])
                cql = f"({cql}) AND ({space_clause})"

            # Add content type restriction if provided
            if content_type:
                cql = f"({cql}) AND type = {content_type}"
        else:
            # This appears to be a CQL query already
            cql = query

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.cql(
                cql=cql,
                limit=limit,
                expand="body.view,space"
            )
        )

        if response is None:
            raise ValueError("Search query failed or response is None")
        results = response.get("results", [])
        return [parse_confluence_response(result, SearchResult) for result in results]

    @backoff.on_exception(
        backoff.expo,
        (HTTPError, ConnectionError),
        max_tries=3,
        max_time=30,
    )
    async def get_spaces(self, limit: int = 25) -> List[Space]:
        """
        List available Confluence spaces.

        Args:
            limit: Maximum number of spaces to return

        Returns:
            List of Space objects
        """
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.get_all_spaces(
                limit=limit,
                expand="description.plain"
            )
        )

        if response is None:
            raise ValueError("Failed to get spaces or response is None")
        spaces = response.get("results", [])
        return [parse_confluence_response(space, Space) for space in spaces]

    @backoff.on_exception(
        backoff.expo,
        (HTTPError, ConnectionError),
        max_tries=3,
        max_time=30,
    )
    async def get_comments(
        self,
        page_id: str,
        depth: str = "all"
    ) -> List[Comment]:
        """
        Get comments for a Confluence page.

        Args:
            page_id: ID of the page
            depth: Comment depth ('all', 'root', or specific level)

        Returns:
            List of Comment objects
        """
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.get_page_comments(
                content_id=page_id,
                expand="body.storage",
                depth=depth
            )
        )

        if response is None:
            raise ValueError(f"Failed to get comments for page with id {page_id} or response is None")
        comments = response.get("results", [])
        return [parse_confluence_response(comment, Comment) for comment in comments]

    @backoff.on_exception(
        backoff.expo,
        (HTTPError, ConnectionError),
        max_tries=3,
        max_time=30,
    )
    async def add_comment(self, page_id: str, content: str) -> Comment:
        """
        Add a comment to a Confluence page.

        Args:
            page_id: ID of the page to comment on
            content: The comment text

        Returns:
            Comment object for the created comment
        """
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.add_comment(
                page_id=page_id,
                text=content
            )
        )

        if response is None:
            raise ValueError(f"Failed to add comment to page with id {page_id} or response is None")
        return parse_confluence_response(response, Comment)

    @backoff.on_exception(
        backoff.expo,
        (HTTPError, ConnectionError),
        max_tries=3,
        max_time=30,
    )
    async def get_labels(self, page_id: str) -> List[Label]:
        """
        Get labels for a Confluence page.

        Args:
            page_id: ID of the page

        Returns:
            List of Label objects
        """
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.get_page_labels(
                page_id=page_id
            )
        )

        if response is None:
            raise ValueError(f"Failed to get labels for page with id {page_id} or response is None")
        labels = response.get("results", [])
        return [parse_confluence_response(label, Label) for label in labels]

    @backoff.on_exception(
        backoff.expo,
        (HTTPError, ConnectionError),
        max_tries=3,
        max_time=30,
    )
    async def add_label(self, page_id: str, label: str) -> Dict[str, Any]:
        """
        Add a label to a Confluence page.

        Args:
            page_id: ID of the page
            label: Label to add

        Returns:
            Dictionary with operation result
        """
        loop = asyncio.get_event_loop()
        try:
            # The Atlassian Python API might have a different method name or signature
            # This is corrected based on the actual API
            await loop.run_in_executor(
                None,
                lambda: self.client.set_page_label(
                    page_id=page_id,
                    label=label
                )
            )
            return {"status": "success", "label": label, "page_id": page_id}
        except Exception as e:
            logger.error("Failed to add label: %s", str(e))
            return {"status": "error", "message": str(e), "label": label, "page_id": page_id}
