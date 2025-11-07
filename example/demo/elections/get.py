# pylint: disable=R0801, C0413

"""Fetches structured content for US presidential election articles."""

import logging
import contextlib
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from modules.auth.auth_client import AuthClient
from modules.api.api_client import Client, Request, Filter
from modules.api.exceptions import APIRequestError, APIStatusError, APIDataError, DataModelError
from modules.api.structuredcontent import StructuredContent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

START_YEAR = 1980  # 1788
END_YEAR = 2024

US_ELECTION_YEARS = list(range(START_YEAR, END_YEAR + 1, 4))

if not os.path.exists('data'):
    os.makedirs('data')

@contextlib.contextmanager
def revoke_token_on_exit(auth_client, refresh_token):
    """This function revokes token on script's exit"""
    try:
        yield
    finally:
        try:
            auth_client.revoke_token(refresh_token)
        except (APIRequestError, APIStatusError) as e:
            logger.error("Failed to revoke token: %s", e)


def save_json_to_file(article_title, data):
    """Saves the given data (a dict) to a file in the data folder."""
    filename = f"data/{article_title}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info("Saved data to %s", filename)


def fetch_and_save_article(api_client, year):
    """Fetches the article for the given year and saves it as a JSON file."""
    article_title = f"{year}_United_States_presidential_election"
    request = Request(
        fields=[],
        filters=[Filter(field="is_part_of.identifier", value="enwiki")]
    )

    try:
        structured_contents = api_client.get_structured_contents(article_title, request)
    except (APIRequestError, APIStatusError, APIDataError, DataModelError) as e:
        logger.error("Failed to get content for %s: %s", article_title, e)
        return

    if structured_contents:
        article_data = structured_contents[0]

        logger.info(
            "Fetched: %s (Modified: %s)",
            article_data.name,
            article_data.date_modified
        )

        article_dict = StructuredContent.to_json(article_data)
        save_json_to_file(article_title, article_dict)
    else:
        logger.warning("No content found for %s", article_title)


def main():
    """Main execution function for the article fetching script."""
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

        for year in US_ELECTION_YEARS:
            fetch_and_save_article(api_client, year)


if __name__ == "__main__":
    main()
