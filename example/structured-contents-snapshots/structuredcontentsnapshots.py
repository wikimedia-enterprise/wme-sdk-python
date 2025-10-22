# pylint: disable=R0801

"""Demonstrates fetching metadata for structured content snapshots.

This script authenticates with the Wikimedia Enterprise API and performs
two actions:
1. Fetches metadata for all available structured content snapshots.
2. Fetches metadata for a single, specific snapshot ("enwiki_namespace_0")
   using a request filter.

It logs the modification date, identifier, and size for the results of
both calls. The script also ensures the authentication token is
revoked upon exit.
"""

import logging
import contextlib
from modules.auth.auth_client import AuthClient
from modules.api.api_client import Client, Request, Filter
from modules.api.exceptions import APIRequestError, APIStatusError, APIDataError, DataModelError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@contextlib.contextmanager
def revoke_token_on_exit(auth_client, refresh_token):
    """Manages the lifecycle of a refresh token, ensuring revocation on exit.

    This context manager yields control to the inner block and guarantees
    that a token revocation attempt is made upon exiting the block,
    whether by successful completion or due to an exception.

    Args:
        auth_client (AuthClient): The authentication client instance.
        refresh_token (str): The refresh token to be revoked.
    """
    try:
        yield
    finally:
        try:
            auth_client.revoke_token(refresh_token)
        except (APIRequestError, APIStatusError) as e:
            logger.error("Failed to revoke token: %s", e)


def main():
    """Main execution function to fetch and display snapshot metadata.

    Orchestrates the entire process:
    1. Authenticates with the AuthClient; exits fatally if login fails.
    2. Sets up a context manager to revoke the token on exit.
    3. Initializes the API Client with the access token.
    4. Fetches and logs metadata for *all* available snapshots.
    5. Defines a filter and fetches and logs metadata for a *single*
    specific snapshot ("enwiki_namespace_0").
    """
    auth_client = AuthClient()
    try:
        login_response = auth_client.login()
    except (APIRequestError, APIStatusError) as e:
        logger.fatal("Login failed: %s", e)
        return

    refresh_token = login_response["refresh_token"]
    access_token = login_response["access_token"]

    with revoke_token_on_exit(auth_client, refresh_token):
        api_client = Client()
        api_client.set_access_token(access_token)

       #to get metadata of all available structured contents snapshots

        try:
            request = Request()
            structured_snapshots = api_client.get_structured_snapshots(request)
        except (APIRequestError, APIStatusError, APIDataError, DataModelError) as e:
            logger.fatal("Failed to get structured contents snapshots: %s", e)
            return

        for content in structured_snapshots:
            logger.info("Name: %s", content.get('date_modified'))
            logger.info("Abstract: %s", content.get('identifier'))
            logger.info("Description: %s", content.get('size'))

        # To get metadata on an single SC snapshot using request parameters
        request = Request(
            filters=[Filter(field="in_language.identifier", value="en")]
        )

        try:
            structured_snapshot = api_client.get_structured_snapshot("enwiki_namespace_0", request)
        except (APIRequestError, APIStatusError, APIDataError, DataModelError) as e:
            logger.fatal("Failed to get structured contents snpshot: %s", e)
            return

        for content in structured_snapshot:
            logger.info("Name: %s", content.get('date_modified'))
            logger.info("Abstract: %s", content.get('identifier'))
            logger.info("Description: %s", content.get('size'))


if __name__ == "__main__":
    main()
