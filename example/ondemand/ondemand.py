# pylint: disable=R0801

"""Fetches articles matching the query 'Montreal' from the API.

This script demonstrates how to authenticate, build a request with dictionary-based
filters (for 'en' language and 'enwiki' project), and request specific
fields including 'article_body.html'.

It then iterates through the results, truncates the HTML body for concise
display, and pretty-prints each article's JSON to the console.
It also ensures proper login and token revocation.
"""

import json
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


def main():
    """Main execution function to fetch and display articles.

    Orchestrates the entire process:
    1. Authenticates with the AuthClient; exits fatally if login fails.
    2. Sets up a context manager to revoke the token on exit.
    3. Initializes the API Client with the access token.
    4. Defines filters and builds a Request for 'Montreal' articles.
    5. Fetches the articles; exits fatally on failure.
    6. Iterates, truncates the HTML body, and pretty-prints each article
    to the console, logging any serialization errors.
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

        # pylint: disable= pointless-string-statement
        # The old method of using filters is still valid
        # filters = [
        #    Filter(field="in_language.identifier", value="en"),
        #    Filter(field="is_part_of.identifier", value="enwiki")]
        # Below, is the new, more intuitive way to declare filters
        filters = {
            "in_language.identifier": "en",
            "is_part_of.identifier": "enwiki"
        }

        request = Request(
            fields=["name", "abstract", "url", "version", "article_body.html"],
            filters=filters
        )

        articles = []
        try:
            articles = api_client.get_articles("Montreal", request)
        except (APIRequestError, APIStatusError, APIDataError, DataModelError) as e:
            logger.fatal("Failed to get articles: %s", e)
            return

        for article in articles:
            try:
                if "article_body" in article and "html" in article["article_body"]:
                    html = article["article_body"]["html"]
                    trunc_marker = "... (truncated)"
                    max_len = 200
                    if len(html) > max_len:
                        article["article_body"]["html"] = html[:max_len - len(trunc_marker)] + trunc_marker
                art_json = json.dumps(article, indent=2)
                print(art_json)
            except (APIRequestError, APIStatusError, APIDataError, DataModelError) as e:
                logger.error("Failed to serialize article: %s", e)


if __name__ == "__main__":
    main()
