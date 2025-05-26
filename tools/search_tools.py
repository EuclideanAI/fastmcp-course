"""Tools for search operations in Confluence."""

from typing import Any, Dict, List, Optional

from fastmcp import Context


class SearchTools:
    """Tools for searching content in Confluence."""

    @staticmethod
    async def search_confluence(
        ctx: Context,
        query: str,
        spaces: Optional[List[str]] = None,
        content_type: Optional[str] = None,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """
        Search Confluence content using CQL or text search.

        Args:
            query: Search terms or CQL query (e.g., 'text ~ "project documentation"')
            spaces: Optional list of space keys to restrict search (e.g., ["DEV", "TEAM"])
            content_type: Optional content type filter (e.g., "page", "blogpost")
            limit: Maximum number of results to return

        Returns:
            Dictionary with search results
        """
        client = ctx.request_context.lifespan_context.confluence

        try:
            results = await client.search(
                query=query, spaces=spaces, content_type=content_type, limit=limit
            )

            return {
                "status": "success",
                "results": [result.__dict__ for result in results],
                "count": len(results),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    @staticmethod
    async def get_spaces(
        ctx: Context,
        limit: int = 25,
    ) -> Dict[str, Any]:
        """
        List available Confluence spaces.

        Args:
            limit: Maximum number of spaces to return

        Returns:
            Dictionary with spaces information
        """
        client = ctx.request_context.lifespan_context.confluence

        try:
            spaces = await client.get_spaces(limit=limit)
            return {
                "status": "success",
                "spaces": [space.__dict__ for space in spaces],
                "count": len(spaces),
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }
