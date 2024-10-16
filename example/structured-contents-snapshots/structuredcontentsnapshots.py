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

       #to get metadata of all available structured contents snapshots

        try:
            structured_snapshots = api_client.get_structured_snapshots(Request)
        except Exception as e:
            logger.fatal(f"Failed to get structured contents snapshots: {e}")
            return

        for content in structured_snapshots:
            logger.info(f"Name: {content['date_modified']}")
            logger.info(f"Abstract: {content['identifier']}")
            logger.info(f"Description: {content['size']}")
        
        # To get metadata on an single SC snapshot using request parameters   
        request = Request(
            filters=[Filter(field="in_language.identifier", value="en")]
        )

        try:
            structured_snapshot = api_client.get_structured_snapshot("enwiki_namespace_0", request)
        except Exception as e:
            logger.fatal(f"Failed to get structured contents snpshot: {e}")
            return

        for content in structured_snapshot:
            logger.info(f"Name: {content['date_modified']}")
            logger.info(f"Abstract: {content['identifier']}")
            logger.info(f"Description: {content['size']}")  


if __name__ == "__main__":
    main()