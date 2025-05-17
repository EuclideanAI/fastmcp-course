import logging
from typing import Any, Dict, Optional

from fastmcp import Context


class PageTools:
    @staticmethod
    async def get_page(
        ctx: Context,
        page_id: str,
        include_body: bool = True,
    ) -> Dict[str, Any]:
        """
        Get Confluence page content and metadata by ID

        Args:
            page_id: The ID of the Confluence page
            include_body: Whether to include the full page content (default: True)

        Returns:
            Dictionary with page information
        """
        client = ctx.request_context.lifespan_context.confluence

        try:
            expand = ["space", "version", "ancestors", "children.page", "creator"]
            if include_body:
                expand.extend(["body.view", "body.storage"])

            page = await client.get_page(page_id=page_id, expand=expand)
            logger = logging.getLogger(__name__)
            logger.info(f"Fetched page: {page}")
            result = {
                "id": page.id,
                "title": page.title,
                "type": page.type.value,
                "space": {"key": page.space.key, "name": page.space.name},
                "creator": {
                    "id": page.creator.id,
                    "display_name": page.creator.display_name,
                },
                "version": page.version.get("number", 1),
            }

            if include_body and page.body:
                if "storage" in page.body:
                    result["body_storage"] = page.body.get("storage", {}).get(
                        "value", ""
                    )

            return {"status": "success", "page": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}

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
        Create a new Confluence page

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
                title=title,
                body=content,
                space_key=space_key,
                parent_id=parent_id,
                representation=content_format,
            )

            return {
                "status": "success",
                "page": {
                    "id": page.id,
                    "title": page.title,
                    "space_key": page.space.key,
                    "url": f"{client.config.url}/wiki/spaces/{page.space.key}/pages/{page.id}/{page.title.replace(' ', '+')}",
                },
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

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
        Update an existing Confluence page

        Args:
            page_id: ID of the page to update
            title: New title of the page
            content: New content of the page
            minor_edit: Whether this is a minor edit (default: False)
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
                body=content,
                minor_edit=minor_edit,
                representation=content_format,
                version_comment=version_comment,
            )

            return {
                "status": "success",
                "page": {
                    "id": page.id,
                    "title": page.title,
                    "space_key": page.space.key,
                    "version": page.version.get("number", 1),
                    "url": f"{client.config.url}/wiki/spaces/{page.space.key}/pages/{page.id}/{page.title.replace(' ', '+')}",
                },
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def delete_page(ctx: Context, page_id: str) -> Dict[str, Any]:
        """
        Delete a Confluence page

        Args:
            page_id: ID of the page to delete

        Returns:
            Dictionary with operation result
        """
        client = ctx.request_context.lifespan_context.confluence

        try:
            success = await client.delete_page(page_id=page_id)

            if success:
                return {
                    "status": "success",
                    "message": f"Page {page_id} was deleted successfully",
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to delete page {page_id}",
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def get_page_children(
        ctx: Context, page_id: str, limit: int = 25
    ) -> Dict[str, Any]:
        """
        Get child pages of a Confluence page

        Args:
            page_id: ID of the parent page
            limit: Maximum number of children to return (default: 25)

        Returns:
            Dictionary with child pages information
        """
        client = ctx.request_context.lifespan_context.confluence

        try:
            children = await client.get_page_children(page_id=page_id, limit=limit)

            formatted_children = []
            for child in children:
                formatted_children.append(
                    {
                        "id": child.id,
                        "title": child.title,
                        "type": child.type.value,
                        "space_key": child.space.key,
                    }
                )

            return {
                "status": "success",
                "children": formatted_children,
                "count": len(formatted_children),
                "parent_id": page_id,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def get_page_ancestors(ctx: Context, page_id: str) -> Dict[str, Any]:
        """
        Get ancestor (parent) pages of a Confluence page

        Args:
            page_id: ID of the page

        Returns:
            Dictionary with ancestor pages information
        """
        client = ctx.request_context.lifespan_context.confluence

        try:
            ancestors = await client.get_page_ancestors(page_id=page_id)

            formatted_ancestors = []
            for ancestor in ancestors:
                formatted_ancestors.append(
                    {
                        "id": ancestor.id,
                        "title": ancestor.title,
                        "type": ancestor.type.value,
                        "space_key": ancestor.space.key,
                    }
                )

            return {
                "status": "success",
                "ancestors": formatted_ancestors,
                "count": len(formatted_ancestors),
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
