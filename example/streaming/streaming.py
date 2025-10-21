# pylint: disable=R0801

"""Demonstrates streaming articles from the API using a callback.

This script authenticates with the Wikimedia Enterprise API, sets up a
request for specific article fields (including 'event.*'), and then
uses the `stream_articles` method.

Each article received from the stream is passed to the `article_callback`
function, which logs its details. The script ensures the authentication
token is revoked on exit.
"""

import logging
import contextlib

from modules.auth.auth_client import AuthClient
from modules.api.api_client import Client, Request
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


def article_callback(article):
    """A callback function to process each article received from the stream.

    This function is invoked by `api_client.stream_articles` for each
    article. It logs the article's name, abstract, and event identifier.

    Args:
        article (dict): The article data dictionary received from the stream.
    """
    logger.info("----------START-----------")
    logger.info("name: %s", article.get('name'))
    logger.info("abstract: %s", article.get('abstract'))
    logger.info("event.identifiers: %s", article.get('event', {}).get('identifier'))
    logger.info("-----------END------------\n\n\n")


def main():
    """Main execution function to initiate the article stream.

    Orchestrates the entire process:
    1. Authenticates with the AuthClient; exits fatally if login fails.
    2. Sets up a context manager to revoke the token on exit.
    3. Initializes the API Client with the access token.
    4. Defines a Request for specific fields.
    5. Starts the article stream, passing the `article_callback` to process
    each article as it arrives.
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
            fields=["name", "abstract", "event.*"]
        )

        try:
            api_client.stream_articles(request, article_callback)
        except (APIRequestError, APIStatusError, APIDataError, DataModelError) as e:
            logger.fatal("Failed to get articles: %s", e)


if __name__ == "__main__":
    main()
