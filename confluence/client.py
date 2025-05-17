import logging
from typing import Any, Dict, List, Optional

import backoff
import httpx
from atlassian import Confluence

from config import ConfluenceConfig
from confluence.models import Comment, Page, SearchResult
from confluence.utils import build_content_payload, format_cql_query

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("confluence_client.log")
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class ConfluenceClient:
    """
    Client for interacting with the Confluence API.

    This client provides a high-level interface to the Confluence REST API,
    using the atlassian-python-api library for the actual communication.
    """

    def __init__(self, config: Optional[ConfluenceConfig] = None):
        """
        Initialize the Confluence client.

        Args:
            config (ConfluenceConfig, optional): Configuration for the client.
                If not provided, will try to load from environment variables.
        """
        if config is None:
            from config import get_confluence_config

            config = get_confluence_config()

        self.config = config
        self._client = self._initialize_client()
        logger.info(f"Initialized Confluence client for URL: {config.url}")

    def _initialize_client(self) -> Confluence:
        """
        Initialize the underlying Confluence client.

        Returns:
            Confluence: An initialized Confluence client from atlassian-python-api

        Raises:
            ValueError: If the configuration is invalid or authentication fails
        """
        try:
            # if self.config.personal_access_token:
            #     return Confluence(
            #         url=self.config.url,
            #         username=self.config.personal_access_token,
            #         password=self.config.personal_access_token,
            #     )
            # else:
            #     return Confluence(
            #         url=self.config.url,
            #         username=self.config.username,
            #         password=self.config.personal_access_token
            #     )
            return Confluence(
                url=self.config.url,
                username=self.config.username,
                password=self.config.personal_access_token,
            )
        except Exception as e:
            logger.error(f"Failed to initialize Confluence client: {str(e)}")
            raise ValueError(f"Failed to initialize Confluence client: {str(e)}") from e

    @backoff.on_exception(
        backoff.expo,
        (httpx.HTTPError, ConnectionError),
        max_tries=3,
        on_backoff=lambda details: logger.warning(
            f"API request failed. Retrying in {details.get('wait', 0):.1f} seconds..."
        ),
    )
    async def search(
        self,
        cql_or_text: str,
        spaces: Optional[List[str]] = None,
        content_type: Optional[str] = None,
        limit: int = 10,
        start: int = 0,
        expand: Optional[List[str]] = None,
    ) -> SearchResult:
        """
        Search Confluence content using CQL or text search.

        Args:
            cql_or_text (str): CQL query or text search
            spaces (list, optional): Space keys to restrict the search to
            content_type (str, optional): Content type to filter by (page, blogpost, etc.)
            limit (int): Maximum number of results to return
            start (int): Starting index for pagination
            expand (list, optional): Fields to expand in the response

        Returns:
            SearchResult: Object containing search results
        """
        # Format the query with space restrictions if needed
        query = format_cql_query(cql_or_text, spaces)

        # Add content type restriction if specified
        if content_type:
            query = f"({query}) AND type={content_type}"

        # Format the expand parameter
        expand_str = ",".join(expand) if expand else "body.view,space,version,creator"

        try:
            logger.info(f"Searching with CQL: {query}")
            response = self._client.cql(
                cql=query, limit=limit, start=start, expand=expand_str
            )

            if not response:
                raise ValueError("Search returned empty response")

            logger.debug(f"Search returned {len(response.get('results', []))} results")
            return SearchResult.from_api_response(response)

        except Exception as e:
            logger.error(f"Failed to search Confluence: {str(e)}")
            raise

    async def get_page(self, page_id: str, expand: Optional[List[str]] = None) -> Page:
        """
        Get a page by ID.

        Args:
            page_id (str): The ID of the page to retrieve
            expand (list, optional): Fields to expand in the response

        Returns:
            Page: The requested page

        Raises:
            ValueError: If the page could not be found
        """
        expand_str = (
            ",".join(expand)
            if expand
            else "body.view,body.storage,space,version,ancestors,children.page,creator"
        )

        try:
            logger.info(f"Fetching page with ID: {page_id}")
            response = self._client.get_page_by_id(page_id=page_id, expand=expand_str)
            logger.info(f"Response for page {page_id}: {response}")
            if response is None:
                raise ValueError(f"Page with ID {page_id} not found")
            else:
                return Page.from_api_response(response)

        except Exception as e:
            logger.error(f"Failed to get page {page_id}: {str(e)}")
            raise

    async def create_page(
        self,
        title: str,
        body: str,
        space_key: str,
        parent_id: Optional[str] = None,
        representation: str = "storage",
    ) -> Page:
        """
        Create a new page in Confluence.

        Args:
            title (str): The title of the page
            body (str): The content of the page
            space_key (str): The key of the space to create the page in
            parent_id (str, optional): The ID of the parent page
            representation (str): The format of the content (storage, wiki, etc.)

        Returns:
            Page: The created page
        """
        build_content_payload(
            title=title,
            body=body,
            space_key=space_key,
            parent_id=parent_id,
            representation=representation,
        )

        try:
            logger.info(f"Creating page '{title}' in space {space_key}")
            response = self._client.create_page(
                space=space_key,
                title=title,
                body=body,
                parent_id=parent_id,
                representation=representation,
            )
            logger.info(f"Response for page creation: {response}")

            if response is None:
                raise ValueError("Create page returned empty response")

            return Page.from_api_response(response)

        except Exception as e:
            logger.error(f"Failed to create page '{title}': {str(e)}")
            raise

    async def update_page(
        self,
        page_id: str,
        title: str,
        body: str,
        minor_edit: bool = False,
        representation: str = "storage",
        version_comment: Optional[str] = None,
    ) -> Page:
        """
        Update an existing page in Confluence.

        Args:
            page_id (str): The ID of the page to update
            title (str): The new title of the page
            body (str): The new content of the page
            minor_edit (bool): Whether this is a minor edit
            representation (str): The format of the content (storage, wiki, etc.)
            version_comment (str, optional): Comment for this version

        Returns:
            Page: The updated page
        """
        try:
            # First, get the current page to determine its version
            current_page = await self.get_page(page_id)
            current_version = current_page.version.get("number", 1)

            logger.info(f"Updating page {page_id} from version {current_version}")
            response = self._client.update_page(
                page_id=page_id,
                title=title,
                body=body,
                minor_edit=minor_edit,
                version_comment=version_comment,
                representation=representation,
            )

            if response is None:
                raise ValueError("Update page returned empty response")

            return Page.from_api_response(response)

        except Exception as e:
            logger.error(f"Failed to update page {page_id}: {str(e)}")
            raise

    async def delete_page(self, page_id: str) -> bool:
        """
        Delete a page from Confluence.

        Args:
            page_id (str): The ID of the page to delete

        Returns:
            bool: True if the page was deleted successfully
        """
        try:
            logger.info(f"Deleting page {page_id}")
            self._client.remove_page(page_id=page_id)
            return True

        except Exception as e:
            logger.error(f"Failed to delete page {page_id}: {str(e)}")
            raise

    async def get_page_children(
        self, page_id: str, expand: Optional[List[str]] = None, limit: int = 25
    ) -> List[Page]:
        """
        Get the child pages of a specific page.

        Args:
            page_id (str): The ID of the parent page
            expand (list, optional): Fields to expand in the response
            limit (int): Maximum number of children to return

        Returns:
            list: List of child pages
        """
        expand_str = ",".join(expand) if expand else "version"

        try:
            logger.info(f"Fetching children of page {page_id}")
            response = self._client.get_page_child_by_type(
                page_id=page_id, type="page", start=0, limit=limit, expand=expand_str
            )

            children = []
            # Ensure response is a dict and not None or a generator
            if response and isinstance(response, dict):
                for child in response.get("results", []):
                    children.append(Page.from_api_response(child))
            else:
                logger.error(
                    f"Unexpected response type for get_page_child_by_type: {type(response)}"
                )
                raise ValueError("Failed to fetch children: Unexpected response type")

            return children

        except Exception as e:
            logger.error(f"Failed to get children of page {page_id}: {str(e)}")
            raise

    async def get_page_ancestors(self, page_id: str) -> List[Page]:
        """
        Get the ancestors (parent pages) of a specific page.

        Args:
            page_id (str): The ID of the page

        Returns:
            list: List of ancestor pages
        """
        try:
            # Get the page with ancestors expanded
            await self.get_page(page_id, expand=["ancestors"])

            # Extract and convert ancestors to Page objects
            ancestors = []
            ancestor_data = self._client.get_page_ancestors(page_id)

            if ancestor_data and isinstance(ancestor_data, dict):
                for ancestor in ancestor_data.get("results", []):
                    ancestors.append(Page.from_api_response(ancestor))
            else:
                logger.error(
                    f"Failed to get ancestors: Unexpected response type {type(ancestor_data)}"
                )
                raise ValueError("Failed to fetch ancestors: Unexpected response type")

            return ancestors

        except Exception as e:
            logger.error(f"Failed to get ancestors of page {page_id}: {str(e)}")
            raise

    async def get_comments(
        self, page_id: str, depth: str = "all", expand: Optional[List[str]] = None
    ) -> List[Comment]:
        """
        Get comments for a specific page.

        Args:
            page_id (str): The ID of the page
            depth (str): Comment depth to retrieve ('all', 'root', or a specific level)
            expand (list, optional): Fields to expand in the response

        Returns:
            list: List of comments
        """
        expand_str = ",".join(expand) if expand else "body.view,version,creator"

        try:
            logger.info(f"Fetching comments for page {page_id}")
            response = self._client.get_page_comments(
                content_id=page_id, depth=depth, expand=expand_str
            )

            comments = []
            if response is not None:
                for comment_data in response.get("results", []):
                    comments.append(Comment.from_api_response(comment_data))
            else:
                logger.error(f"get_page_comments returned None for page {page_id}")
                raise ValueError("Failed to get comments: response is None")

            return comments

        except Exception as e:
            logger.error(f"Failed to get comments for page {page_id}: {str(e)}")
            raise

    async def add_comment(self, page_id: str, comment_text: str) -> Comment:
        """
        Add a comment to a page.

        Args:
            page_id (str): The ID of the page to comment on
            comment_text (str): The text of the comment

        Returns:
            Comment: The created comment
        """
        try:
            logger.info(f"Adding comment to page {page_id}")
            response = self._client.add_comment(page_id=page_id, text=comment_text)

            if response is None:
                logger.error(f"add_comment returned None for page {page_id}")
                raise ValueError("Failed to add comment: response is None")

            return Comment.from_api_response(response)

        except Exception as e:
            logger.error(f"Failed to add comment to page {page_id}: {str(e)}")
            raise

    async def get_labels(self, page_id: str) -> List[Dict[str, str]]:
        """
        Get labels for a specific page.

        Args:
            page_id (str): The ID of the page

        Returns:
            list: List of labels
        """
        try:
            logger.info(f"Fetching labels for page {page_id}")
            response = self._client.get_page_labels(page_id=page_id)

            labels = []
            if response is not None:
                for label_data in response.get("results", []):
                    labels.append(
                        {
                            "id": label_data.get("id"),
                            "name": label_data.get("name"),
                            "prefix": label_data.get("prefix", "global"),
                        }
                    )
            else:
                logger.error(f"get_page_labels returned None for page {page_id}")
                raise ValueError("Failed to get labels: response is None")

            return labels

        except Exception as e:
            logger.error(f"Failed to get labels for page {page_id}: {str(e)}")
            raise

    async def add_label(self, page_id: str, label: str) -> Dict[str, Any]:
        """
        Add a label to a page.

        Args:
            page_id (str): The ID of the page
            label (str): The label to add

        Returns:
            dict: The created label
        """
        try:
            logger.info(f"Adding label '{label}' to page {page_id}")
            response = self._client.set_page_label(page_id=page_id, label=label)

            if response is None:
                logger.error(f"set_page_label returned None for page {page_id}")
                raise ValueError("Failed to add label: response is None")

            return response

        except Exception as e:
            logger.error(f"Failed to add label '{label}' to page {page_id}: {str(e)}")
            raise

    async def get_spaces(self, limit: int = 25, start: int = 0) -> List[Dict[str, Any]]:
        """
        Get available Confluence spaces.

        Args:
            limit (int): Maximum number of spaces to return
            start (int): Starting index for pagination

        Returns:
            list: List of spaces
        """
        try:
            logger.info("Fetching Confluence spaces")
            response = self._client.get_all_spaces(
                start=start, limit=limit, expand="description.plain"
            )

            spaces = []
            if response is not None:
                for space_data in response.get("results", []):
                    spaces.append(
                        {
                            "id": space_data.get("id"),
                            "key": space_data.get("key"),
                            "name": space_data.get("name"),
                            "type": space_data.get("type"),
                            "description": space_data.get("description", {})
                            .get("plain", {})
                            .get("value", ""),
                        }
                    )
            else:
                logger.error("get_all_spaces returned None")
                raise ValueError("Failed to get spaces: response is None")

            return spaces

        except Exception as e:
            logger.error(f"Failed to get Confluence spaces: {str(e)}")
            raise

    async def disconnect(self) -> None:
        """
        Disconnect and cleanup resources.

        This method should be called when the client is no longer needed
        to free up resources and close connections properly.
        """
        # The atlassian-python-api client doesn't have an explicit disconnect method,
        # but we'll add this as a placeholder for future extensions or cleanup.
        # In a real-world implementation, you might need to clean up connection pools, etc.
        logger.info("Disconnecting Confluence client")
