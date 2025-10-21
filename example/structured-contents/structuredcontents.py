# pylint: disable=R0801
"""Fetches structured content for the article "Squirrel".

This script authenticates with the Wikimedia Enterprise API, builds a request
for the "enwiki" version of the article "Squirrel", and specifies the
'name', 'abstract', and 'description' fields.

It logs these fields for each result found and ensures the authentication
token is revoked upon exit.
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
    """Main execution function to fetch and display structured content.

    Orchestrates the entire process:
    1. Authenticates with the AuthClient; exits fatally if login fails.
    2. Sets up a context manager to revoke the token on exit.
    3. Initializes the API Client with the access token.
    4. Defines and executes a request for the "Squirrel" article.
    5. Logs the name, abstract, and description of each result.
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

        request = Request(
            fields=["name", "abstract", "description"],
            filters=[Filter(field="is_part_of.identifier", value="enwiki")]
        )

        try:
            structured_contents = api_client.get_structured_contents("Squirrel", request)
        except (APIRequestError, APIStatusError, APIDataError, DataModelError) as e:
            logger.fatal("Failed to get structured contents: %s", e)
            return

        for content in structured_contents:
            logger.info("Name: %s", content['name'])
            logger.info("Abstract: %s", content['abstract'])
            logger.info("Description: %s", content['description'])


if __name__ == "__main__":
    main()
