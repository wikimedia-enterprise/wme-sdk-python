import logging
from contextlib import contextmanager

from auth_client import AuthClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@contextmanager
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

    with revoke_token_on_exit(auth_client, refresh_token):
        # ...your code goes here...
        pass


if __name__ == "__main__":
    main()
