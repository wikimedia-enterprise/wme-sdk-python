"""This example demonstrates the authentication process, and once authorized, fetching an article"""

import time
import logging
import json

from modules.auth.helper import Helper
from modules.auth.auth_client import AuthClient
from modules.api.api_client import Client, Request, Filter
from modules.api.exceptions import APIRequestError, APIStatusError, APIDataError, DataModelError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """This is the main script that demonstrates the principles described above"""
    auth_client = AuthClient()
    try:
        helper = Helper(auth_client)
    except (APIRequestError, APIStatusError) as e:
        logger.fatal("Failed to create helper: %s", e)
        return

    try:
        token = helper.get_access_token()
        logger.info("Access token: %s", token)

        # Use the token to get articles from the API
        api_client = Client()
        api_client.set_access_token(token)

        request = Request(
            fields=["name", "abstract", "url", "version"],
            filters=[Filter(field="in_language.identifier", value="en")]
        )

        try:
            articles = api_client.get_articles("Montreal", request)
        except (APIRequestError, APIStatusError) as e:
            logger.fatal("Failed to get articles: %s", e)
            return

        for article in articles:
            try:
                art_json = json.dumps(article, indent=2)
                print(art_json)
            except (APIDataError, DataModelError) as e:
                logger.error("Failed to serialize article: %s", e)

    except (APIRequestError, APIStatusError) as e:
        logger.error("Failed to get access token: %s", e)
    finally:
        helper.stop()
        logger.info("Exiting")
        time.sleep(1)

if __name__ == "__main__":
    main()
