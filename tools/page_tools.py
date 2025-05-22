"""Tools for page operations in Confluence."""
import logging
from typing import Any, Dict, Optional

from fastmcp import Context


class PageTools:
    """Tools for interacting with Confluence pages."""

    @staticmethod
    async def get_page(
        ctx: Context,
        page_id: str,
        include_body: bool = True,
    ) -> Dict[str, Any]:
        """
        Get Confluence page content and metadata by ID.

        Args:
            page_id: The ID of the Confluence page
            include_body: Whether to include the full page content

        Returns:
            Dictionary with page information
        """
        client = ctx.request_context.lifespan_context.confluence

        try:
            page = await client.get_page(page_id=page_id, include_body=include_body)
            # Log the payload to a local log file
            logging.basicConfig(filename='confluence_client.log', level=logging.INFO)
            logging.info("Payload for page_id %s: %s", page_id, page.__dict__)
            print(page)

            return {
                "status": "success",
                "page": page.__dict__,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    @staticmethod
    async def create_page(
        ctx: Context,
        title: str,
        content: str,
        space_key: str,
        parent_id: Optional[str] = None,
        content_format: str = "storage",
    ) -> Dict[str, Any]:
        """
        Create a new Confluence page.

        Args:
            title: Title of the page
            content: Content of the page (in the specified format)
            space_key: Key of the space where the page will be created
            parent_id: Optional ID of the parent page for hierarchical content
            content_format: Content format ('storage' for XHTML, 'wiki' for wiki markup)

        Returns:
            Dictionary with created page information
        """
        client = ctx.request_context.lifespan_context.confluence

        try:
            page = await client.create_page(
                space_key=space_key,
                title=title,
                content=content,
                parent_id=parent_id,
                content_format=content_format
            )
            return {
                "status": "success",
                "page": page.__dict__,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    @staticmethod
    async def update_page(
        ctx: Context,
        page_id: str,
        title: str,
        content: str,
        minor_edit: bool = False,
        content_format: str = "storage",
        version_comment: Optional[str] = None,
    ) -> Dict[str, Any]:
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
            Dictionary with updated page information
        """
        client = ctx.request_context.lifespan_context.confluence

        try:
            page = await client.update_page(
                page_id=page_id,
                title=title,
                content=content,
                minor_edit=minor_edit,
                content_format=content_format,
                version_comment=version_comment
            )
            return {
                "status": "success",
                "page": page.__dict__,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    @staticmethod
    async def delete_page(
        ctx: Context,
        page_id: str,
    ) -> Dict[str, Any]:
        """
        Delete a Confluence page.

        Args:
            page_id: ID of the page to delete

        Returns:
            Dictionary with operation result
        """
        client = ctx.request_context.lifespan_context.confluence

        try:
            result = await client.delete_page(page_id=page_id)
            return result
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    @staticmethod
    async def get_page_children(
        ctx: Context,
        page_id: str,
        limit: int = 25,
    ) -> Dict[str, Any]:
        """
        Get child pages of a Confluence page.

        Args:
            page_id: ID of the parent page
            limit: Maximum number of children to return

        Returns:
            Dictionary with child pages information
        """
        client = ctx.request_context.lifespan_context.confluence

        try:
            pages = await client.get_page_children(page_id=page_id, limit=limit)
            return {
                "status": "success",
                "children": [page.__dict__ for page in pages],
                "count": len(pages),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    @staticmethod
    async def get_page_ancestors(
        ctx: Context,
        page_id: str,
    ) -> Dict[str, Any]:
        """
        Get ancestor (parent) pages of a Confluence page.

        Args:
            page_id: ID of the page

        Returns:
            Dictionary with ancestor pages information
        """
        client = ctx.request_context.lifespan_context.confluence

        try:
            pages = await client.get_page_ancestors(page_id=page_id)
            return {
                "status": "success",
                "ancestors": [page.__dict__ for page in pages],
                "count": len(pages),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }
