import logging
import contextlib

from modules.auth.auth_client import AuthClient
from modules.api.api_client import Client, Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@contextlib.contextmanager
def revoke_token_on_exit(auth_client, refresh_token):
    try:
        yield
    finally:
        try:
            auth_client.revoke_token(refresh_token)
        except Exception as e:
            logger.error(f"Failed to revoke token: {e}")


def article_callback(article):
    logger.info("----------START-----------")
    logger.info(f"name: {article.get('name')}")
    logger.info(f"abstract: {article.get('abstract')}")
    logger.info(f"event.identifiers: {article.get('event', {}).get('identifier')}")
    logger.info("-----------END------------\n\n\n")


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

        request = Request(
            fields=["name", "abstract", "event.*"]
        )

        try:
            articles = api_client.get_articles(request, article_callback)
            print(articles)
        except Exception as e:
            logger.fatal(f"Failed to get articles: {e}")


if __name__ == "__main__":
    main()
