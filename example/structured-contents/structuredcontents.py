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

        request = Request(
            fields=["name", "abstract", "description"],
            filters=[Filter(field="is_part_of.identifier", value="enwiki")]
        )

        try:
            structured_contents = api_client.get_structured_contents("Squirrel", request)
        except Exception as e:
            logger.fatal(f"Failed to get structured contents: {e}")
            return

        for content in structured_contents:
            logger.info(f"Name: {content['name']}")
            logger.info(f"Abstract: {content['abstract']}")
            logger.info(f"Description: {content['description']}")


if __name__ == "__main__":
    main()
