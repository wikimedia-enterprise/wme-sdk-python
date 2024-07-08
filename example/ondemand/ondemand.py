import json
import logging
import contextlib

from auth_client import AuthClient
from api_client import ApiClient, Request, Filter

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
        api_client = ApiClient()
        api_client.set_access_token(access_token)

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


if __name__ == "__main__":
    main()
