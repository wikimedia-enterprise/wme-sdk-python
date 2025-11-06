# pylint: disable=R0801, C0103, W0718

"""Fetches structured content for the article "Squirrel".

This script demonstrates how to authenticate using the AuthClient's
managed lifecycle, build a request with dictionary-based filters,
and request specific fields for structured content.

It logs these fields for each result found and ensures the authentication
token is revoked upon exit.
"""

import logging
from httpx import RequestError, HTTPStatusError

# --- Import custom modules ---
from modules.auth.auth_client import AuthClient
from modules.api.api_client import Client, Request
# Import the model to know how to handle the object
from modules.api.structuredcontent import StructuredContent
from modules.api.exceptions import APIRequestError, APIStatusError, APIDataError, DataModelError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Main execution function to fetch and display structured content.

    Orchestrates the entire process:
    1. Authenticates with the AuthClient, which handles the full token lifecycle.
    2. Initializes the API Client with the access token.
    3. Defines and executes a request for the "Squirrel" article.
    4. Logs the name, abstract, and description of each result object.
    5. Clears the authentication state (revokes token, deletes file) on exit.
    """

    # FIX: Use AuthClient as a context manager *outside* the try/finally
    with AuthClient() as auth_client:
        try:
            # FIX: Use the managed get_access_token() method
            logger.info("Authenticating...")
            access_token = auth_client.get_access_token()

            api_client = Client()
            api_client.set_access_token(access_token)
            logger.info("Authentication successful. Fetching content...")

            # FIX: Use modern dictionary-based filter
            filters = {
                "is_part_of.identifier": "enwiki"
            }

            request = Request(
                fields=["name", "abstract", "description"],
                filters=filters
            )

            structured_contents = api_client.get_structured_contents("Squirrel", request)
            logger.info("Found %d content item(s).", len(structured_contents))

            # FIX: Use attribute access (content.name) instead of dict keys
            for content in structured_contents:
                logger.info("--- Content Item ---")
                logger.info("Name: %s", content.name)
                logger.info("Abstract: %s", content.abstract)
                logger.info("Description: %s", content.description)

        except (RequestError, HTTPStatusError) as e:
            # Handles auth-related HTTP errors
            logger.fatal("Authentication failed: %s", e)
        except (APIRequestError, APIStatusError, APIDataError, DataModelError) as e:
            logger.fatal("Failed to get structured contents: %s", e)
        except Exception as e:
            logger.fatal("An unexpected error occurred: %s", e, exc_info=True)
        finally:
            # FIX: Use clear_state() to revoke token and delete file
            logger.info("Cleaning up authentication state...")
            auth_client.clear_state()
            logger.info("Cleanup complete.")


if __name__ == "__main__":
    main()
