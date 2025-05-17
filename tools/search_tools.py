from typing import Any, Dict, List, Optional

from fastmcp import Context


class SearchTools:
    """Register search-related tools with the FastMCP server."""

    @staticmethod
    async def search_confluence(
        ctx: Context,
        query: str,
        spaces: Optional[List[str]] = None,
        content_type: Optional[str] = None,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """
        Search Confluence content using CQL or text search

        Args:
            query: Search terms or CQL query (e.g., 'text ~ "project documentation"')
            spaces: Optional list of space keys to restrict search (e.g., ["DEV", "TEAM"])
            content_type: Optional content type filter (e.g., "page", "blogpost")
            limit: Maximum number of results to return (default: 10)

        Returns:
            Dictionary with search results
        """
        client = ctx.request_context.lifespan_context.confluence

        try:
            results = await client.search(
                cql_or_text=query, spaces=spaces, content_type=content_type, limit=limit
            )

            # Format the results for a more user-friendly output
            formatted_results = []
            for content in results.results:
                formatted_results.append(
                    {
                        "id": content.id,
                        "title": content.title,
                        "type": content.type.value,
                        "space": {"key": content.space.key, "name": content.space.name},
                        "created": content.created.isoformat(),
                        "updated": content.updated.isoformat(),
                        "creator": content.creator.display_name,
                    }
                )

            return {
                "status": "success",
                "results": formatted_results,
                "count": len(formatted_results),
                "limit": limit,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def get_spaces(ctx: Context, limit: int = 25) -> Dict[str, Any]:
        """
        List available Confluence spaces

        Args:
            limit: Maximum number of spaces to return (default: 25)

        Returns:
            Dictionary with spaces information
        """
        client = ctx.request_context.lifespan_context.confluence

        try:
            spaces = await client.get_spaces(limit=limit)

            return {"status": "success", "spaces": spaces, "count": len(spaces)}
        except Exception as e:
            return {"status": "error", "message": str(e)}
