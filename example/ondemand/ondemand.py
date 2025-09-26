import json
import logging
import contextlib

from modules.auth.auth_client import AuthClient
from modules.api.api_client import Client, Request, Filter

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
        api_client = Client()
        api_client.set_access_token(access_token)
        
        """
        The old method of using filters is still valid
        filters = [
            Filter(field="in_language.identifier", value="en"),
            Filter(field="is_part_of.identifier", value="enwiki")]
        Below, is the new, more intuitive way to declare filters
        """
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
        except Exception as e:
            logger.fatal(f"Failed to get articles: {e}")
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
            except Exception as e:
                logger.error(f"Failed to serialize article: {e}")


if __name__ == "__main__":
    main()
