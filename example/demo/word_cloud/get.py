# pylint: disable=R0801, C0413

"""Fetches and saves the structured content for a single Wikipedia article.

It handles authentication with the Wikimedia Enterprise API, fetches the
structured content for the specified 'enwiki' article, and saves the
result to a JSON file in the './data' directory. It also ensures
the authentication token is revoked on exit.

Usage:
    python get.py "Article Title"
"""

import logging
import sys
import os
import contextlib
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from modules.auth.auth_client import AuthClient
from modules.api.api_client import Client, Request, Filter
from modules.api.exceptions import APIStatusError, APIRequestError, APIDataError, DataModelError
from modules.api.structuredcontent import StructuredContent


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not os.path.exists('data'):
    os.makedirs('data')


@contextlib.contextmanager
def revoke_token_on_exit(auth_client, refresh_token):
    """Manages the lifecycle of a refresh token, ensuring revocation on exit."""
    try:
        yield
    finally:
        try:
            auth_client.revoke_token(refresh_token)
        except (APIStatusError, APIRequestError) as e:
            logger.error("Failed to revoke token: %s", e)


def save_json_to_file(article_title, data):
    """Saves the given data (a dict) to a file in the data folder."""
    safe_title = article_title.replace(" ", "_").replace("/", "_")
    filename = f"data/{safe_title}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info("Saved data to %s", filename)


def fetch_and_save_article(api_client: Client, article_title: str):
    """Fetches the article's structured content and saves it as a JSON file."""

    request = Request(
        filters=[Filter(field="is_part_of.identifier", value="enwiki")]
    )

    try:
        structured_contents = api_client.get_structured_contents(article_title, request)
    except (APIStatusError, APIRequestError, APIDataError, DataModelError) as e:
        logger.error("Failed to get content for %s: %s", article_title, e)
        return

    if structured_contents:
        article_data = structured_contents[0]

        logger.info(
            "Successfully fetched: %s (Identifier: %s)",
            article_data.name,
            article_data.identifier
        )

        article_dict_to_save = StructuredContent.to_json(article_data)

        save_json_to_file(article_title, article_dict_to_save)
    else:
        logger.warning("No content found for %s", article_title)


def main():
    """Main execution function for the article fetching script."""
    if len(sys.argv) < 2:
        print("Usage: python get.py \"Article Title\"")
        sys.exit(1)

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

        fetch_and_save_article(api_client, article_title)

if __name__ == '__main__':
    main()
