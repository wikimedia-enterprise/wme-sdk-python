"""
Handles user authentication and token revocation.

This script performs a login using the AuthClient, obtains a refresh token,
and then executes a main block of code (currently a placeholder). It uses a
context manager to ensure that the refresh token is revoked when the main
block finishes or if an error occurs.
"""

import logging
from contextlib import contextmanager
from modules.auth.auth_client import AuthClient
from modules.api.exceptions import APIRequestError, APIStatusError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@contextmanager
def revoke_token_on_exit(auth_client, refresh_token):
    """Manages the lifecycle of a refresh token, ensuring revocation on exit.

    This context manager yields control to the inner block and guarantees
    that a token revocation attempt is made upon exiting the block,
    whether by successful completion or due to an exception.

    Args:
        auth_client (AuthClient): The authentication client instance.
        refresh_token (str): The refresh token to be revoked.
    """
    try:
        yield
    finally:
        try:
            auth_client.revoke_token(refresh_token)
        except (APIRequestError, APIStatusError) as e:
            logger.error("Failed to revoke token: %s", e)


def main():
    """Main execution function to handle login and secure operations.

    Orchestrates the process:
    1. Initializes the AuthClient.
    2. Performs user login; exits fatally if login fails.
    3. Enters a context-managed block that will revoke the refresh token
    on exit.
    4. (Placeholder) Executes the primary logic of the application.
    """
    auth_client = AuthClient()

    try:
        login_response = auth_client.login()
    except (APIRequestError, APIStatusError) as e:
        logger.fatal("Login failed: %s", e)
        return

    refresh_token = login_response["refresh_token"]

    with revoke_token_on_exit(auth_client, refresh_token):
        # ...your code goes here...
        pass


if __name__ == "__main__":
    main()
