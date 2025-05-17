import re
from datetime import datetime
from typing import Any, Dict, List, Optional


def convert_to_datetime(date_string: str) -> datetime:
    """
    Convert an ISO-formatted date string to a datetime object.

    Args:
        date_string (str): ISO-formatted date string from the Confluence API

    Returns:
        datetime: The parsed datetime object
    """
    # Handle Confluence API date formats - they often end with Z for UTC
    if date_string.endswith("Z"):
        date_string = date_string[:-1] + "+00:00"
    return datetime.fromisoformat(date_string)


def format_cql_query(query: str, spaces: Optional[List[str]] = None) -> str:
    """
    Format a Confluence Query Language (CQL) query with optional space restrictions.

    Args:
        query (str): The base query string
        spaces (list, optional): List of space keys to restrict the search to

    Returns:
        str: The formatted CQL query
    """
    # If query already looks like CQL (contains boolean operators, etc.), use it directly
    if re.search(r"\b(AND|OR|NOT)\b", query, re.IGNORECASE) or "=" in query:
        base_query = query
    else:
        # Otherwise, treat it as a text search
        base_query = f'text ~ "{query}"'

    # Add space restrictions if provided
    if spaces and len(spaces) > 0:
        spaces_clause = " OR ".join([f'space = "{space}"' for space in spaces])
        return f"({base_query}) AND ({spaces_clause})"

    return base_query


def extract_content_body(
    content: Dict[str, Any], format_type: str = "view"
) -> Optional[str]:
    """
    Extract content body in the specified format from a Confluence content object.

    Args:
        content (dict): Content object from Confluence API
        format_type (str): The desired content format ('view', 'storage', etc.)

    Returns:
        str or None: The content body in the specified format, or None if not available
    """
    body = content.get("body", {})

    if not body:
        return None

    desired_format = body.get(format_type, {})
    if not desired_format:
        return None

    return desired_format.get("value", None)


def parse_markdown_to_storage(markdown_content: str) -> str:
    """
    Convert markdown content to Confluence storage format (XHTML).

    This is a basic implementation and should be extended with a proper
    markdown-to-html converter like markdown2 or mistune.

    Args:
        markdown_content (str): Markdown content

    Returns:
        str: Content in Confluence storage format (XHTML)
    """
    # In a real implementation, replace this with:
    # html_content = markdown_converter.convert(markdown_content)
    html_content = f"<p>{markdown_content}</p>"

    return f"""
    <ac:structured-macro ac:name="html">
        <ac:plain-text-body><![CDATA[{html_content}]]></ac:plain-text-body>
    </ac:structured-macro>
    """


def build_content_payload(
    title: str,
    body: str,
    space_key: str,
    content_type: str = "page",
    parent_id: Optional[str] = None,
    version_number: Optional[int] = None,
    representation: str = "storage",
) -> Dict[str, Any]:
    """
    Build a content payload for creating or updating Confluence content.

    Args:
        title (str): Content title
        body (str): Content body
        space_key (str): Space key
        content_type (str): Content type (page, blogpost, etc.)
        parent_id (str, optional): ID of the parent page for hierarchical content
        version_number (int, optional): Version number for updates
        representation (str): Body representation format (storage, wiki, etc.)

    Returns:
        dict: Confluence content payload
    """
    payload = {
        "type": content_type,
        "title": title,
        "space": {"key": space_key},
        "body": {representation: {"value": body, "representation": representation}},
    }

    # Add parent reference for hierarchical content
    if parent_id:
        payload["ancestors"] = [{"id": parent_id}]

    # Add version info for updates
    if version_number is not None:
        payload["version"] = {"number": version_number}

    return payload
