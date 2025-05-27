"""Tools for comment operations in Confluence."""

from typing import Any, Dict

from fastmcp import Context


class CommentTools:
    """Tools for managing comments on Confluence pages."""

    @staticmethod
    async def get_comments(
        ctx: Context,
        page_id: str,
        depth: str = "all",
    ) -> Dict[str, Any]:
        """
        Get comments for a Confluence page.

        Args:
            page_id: ID of the page
            depth: Comment depth ('all', 'root', or specific level)

        Returns:
            Dictionary with comments information
        """
        client = ctx.request_context.lifespan_context.confluence

        try:
            comments = await client.get_comments(page_id=page_id, depth=depth)
            return {
                "status": "success",
                "comments": [comment.__dict__ for comment in comments],
                "count": len(comments),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    @staticmethod
    async def add_comment(
        ctx: Context,
        page_id: str,
        content: str,
    ) -> Dict[str, Any]:
        """
        Add a comment to a Confluence page.

        Args:
            page_id: ID of the page to comment on
            content: The comment text

        Returns:
            Dictionary with created comment information
        """
        client = ctx.request_context.lifespan_context.confluence

        try:
            comment = await client.add_comment(page_id=page_id, content=content)
            return {
                "status": "success",
                "comment": comment.__dict__,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    @staticmethod
    async def get_labels(
        ctx: Context,
        page_id: str,
    ) -> Dict[str, Any]:
        """
        Get labels for a Confluence page.

        Args:
            page_id: ID of the page

        Returns:
            Dictionary with labels information
        """
        client = ctx.request_context.lifespan_context.confluence

        try:
            labels = await client.get_labels(page_id=page_id)
            return {
                "status": "success",
                "labels": [label.__dict__ for label in labels],
                "count": len(labels),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    @staticmethod
    async def add_label(
        ctx: Context,
        page_id: str,
        label: str,
    ) -> Dict[str, Any]:
        """
        Add a label to a Confluence page.

        Args:
            page_id: ID of the page
            label: Label to add

        Returns:
            Dictionary with operation result
        """
        client = ctx.request_context.lifespan_context.confluence

        try:
            result = await client.add_label(page_id=page_id, label=label)
            # Ensure we return a Dict[str, Any]
            if isinstance(result, dict):
                return result
            else:
                return {"status": "success", "result": result}
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }
