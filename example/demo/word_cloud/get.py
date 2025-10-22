# pylint: disable=R0801

"""Fetches and saves the structured content for a single Wikipedia article.

It handles authentication with the Wikimedia Enterprise API, fetches the
structured content for the specified 'enwiki' article, and saves the
result to a JSON file in the './data' directory. It also ensures
the authentication token is revoked on exit.

Usage:
    python get.py "Article Title"

It handles authentication with the Wikimedia Enterprise API, fetches the
structured content for the specified 'enwiki' article, and saves the
result to a JSON file in the './data' directory. It also ensures
the authentication token is revoked on exit.
"""

import logging
import sys
import os
import contextlib
import json
from modules.auth.auth_client import AuthClient
from modules.api.api_client import Client, Request, Filter
from modules.api.exceptions import APIStatusError, APIRequestError, APIDataError

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure the 'data' folder exists
if not os.path.exists('data'):
    os.makedirs('data')


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
        except (APIStatusError, APIRequestError) as e:
            logger.error("Failed to revoke token: %s", e)


def save_json_to_file(article_title, data):
    """Saves the given data to a file in the data folder with the article title as filename."""
    filename = f"data/{article_title}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info("Saved article: %s to %s", article_title, filename)


def fetch_and_save_article(api_client, article_title):
    """Fetches the article for the given year and saves it as a JSON file."""
    request = Request(
        fields=[],
        filters=[Filter(field="is_part_of.identifier", value="enwiki")]
    )

    try:
        structured_contents = api_client.get_structured_contents(article_title, request)
    except (APIStatusError, APIRequestError, APIDataError) as e:
        logger.error("Failed to get content for %s: %s", article_title, e)
        return

    if structured_contents:
        # Assuming structured_contents returns a list and we want the first item
        article_data = structured_contents[0]
        save_json_to_file(article_title, article_data)
    else:
        logger.warning("No content found for %s", article_title)


def main():
    """Main execution function for the article fetching script.

    Orchestrates the entire process:
    1. Reads the article title from the command-line arguments.
    2. Authenticates with the AuthClient.
    3. Sets up a context manager to revoke the token on exit.
    4. Initializes the API Client with the access token.
    5. Calls `fetch_and_save_article` to get and save the content.
    """
    # Check if the title is provided in command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python get.py \"Article Title\"")
        sys.exit(1)

    # Get the article title from the command line
    article_title = sys.argv[1]

    auth_client = AuthClient()
    try:
        login_response = auth_client.login()
    except (APIStatusError, APIRequestError) as e:
        logger.fatal("Login failed: %s", e)
        return

    refresh_token = login_response["refresh_token"]
    access_token = login_response["access_token"]

    with revoke_token_on_exit(auth_client, refresh_token):
        api_client = Client()
        api_client.set_access_token(access_token)

        # Fetch and save article
        fetch_and_save_article(api_client, article_title)

if __name__ == '__main__':
    main()
