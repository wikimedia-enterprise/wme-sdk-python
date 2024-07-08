import time
import logging
import json
import sys
from auth_client import AuthClient
from helper import Helper
from api_client import ApiClient, Request, Filter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    auth_client = AuthClient()
    try:
        helper = Helper(auth_client)
    except Exception as e:
        logger.fatal(f"Failed to create helper: {e}")
        return

    try:
        token = helper.get_access_token()
        logger.info(f"Access token: {token}")

        # Use the token to get articles from the API
        api_client = ApiClient()
        api_client.set_access_token(token)

        request = Request(
            fields=["name", "abstract", "url", "version"],
            filters=[Filter(field="in_language.identifier", value="en")]
        )

        try:
            articles = api_client.get_articles("Montreal", request)
        except Exception as e:
            logger.fatal(f"Failed to get articles: {e}")
            return

        for article in articles:
            try:
                art_json = json.dumps(article, indent=2)
                print(art_json)
            except Exception as e:
                logger.error(f"Failed to serialize article: {e}")

    except Exception as e:
        logger.error(f"Failed to get access token: {e}")
    finally:
        helper.stop()
        logger.info("Exiting")
        time.sleep(1)


def usage():
    print(f"""Usage: {sys.argv[0]}""")


if __name__ == "__main__":
    main()
