import logging
import contextlib
import os
import json
import requests

from modules.auth.auth_client import AuthClient
from modules.api.api_client import Client, Request, Filter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Start and end year for the election
START_YEAR = 1980
END_YEAR = 2020

# Generate the US election years dynamically (every 4 years)
US_ELECTION_YEARS = list(range(START_YEAR, END_YEAR + 1, 4))

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


def fetch_and_save_article(api_client, year):
    """Fetches the article for the given year and saves it as a JSON file."""
    article_title = f"{year}_United_States_presidential_election"
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

        # Fetch and save articles for each year
        for year in US_ELECTION_YEARS:
            fetch_and_save_article(api_client, year)


if __name__ == "__main__":
    main()
