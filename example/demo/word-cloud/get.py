import logging
import requests
import sys
import os
import contextlib
import json

from modules.auth.auth_client import AuthClient
from modules.api.api_client import Client, Request, Filter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure the 'data' folder exists
if not os.path.exists('data'):
    os.makedirs('data')


@contextlib.contextmanager
def revoke_token_on_exit(auth_client, refresh_token):
    try:
        yield
    finally:
        try:
            auth_client.revoke_token(refresh_token)
        except Exception as e:
            logger.error(f"Failed to revoke token: {e}")


def save_json_to_file(article_title, data):
    """Saves the given data to a file in the data folder with the article title as filename."""
    filename = f"data/{article_title}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info(f"Saved article: {article_title} to {filename}")


def fetch_and_save_article(api_client, article_title):
    """Fetches the article for the given year and saves it as a JSON file."""
    request = Request(
        fields=[],
        filters=[Filter(field="is_part_of.identifier", value="enwiki")]
    )

    try:
        structured_contents = api_client.get_structured_contents(article_title, request)
    except Exception as e:
        logger.error(f"Failed to get content for {article_title}: {e}")
        return

    if structured_contents:
        # Assuming structured_contents returns a list and we want the first item
        article_data = structured_contents[0]
        save_json_to_file(article_title, article_data)
    else:
        logger.warning(f"No content found for {article_title}")


def main():
    # Check if the title is provided in command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python get.py \"Article Title\"")
        sys.exit(1)

    # Get the article title from the command line
    article_title = sys.argv[1]

    auth_client = AuthClient()
    try:
        login_response = auth_client.login()
    except Exception as e:
        logger.fatal(f"Login failed: {e}")
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
