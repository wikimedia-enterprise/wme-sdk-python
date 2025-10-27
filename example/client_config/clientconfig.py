# pylint: disable=C0103, W0621, W0718, E1206, R0801
"""
Demonstrates configuring the API Client with custom timeout, max_retries,
and user_agent settings.
"""

import sys
import os
import logging
import httpx

# --- Add project root to sys.path ---
try:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)
except NameError:
    PROJECT_ROOT = os.path.abspath('.')
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

# --- Import our custom modules ---
try:
    from modules.auth.auth_client import AuthClient
    from modules.auth.helper import Helper
    from modules.api.api_client import Client, Request
    from modules.api.exceptions import APIRequestError, APIStatusError, APIDataError
except ImportError as e:
    print("Error: Failed to import modules. Make sure you are running from the project root")
    print("       or that '{PROJECT_ROOT}' is correct.")
    print("Details: {e}")
    sys.exit(1)

# --- Setup logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Main Function ---
def main():
    """Runs the demonstration of custom client configurations."""
    helper = None
    auth_client = None
    api_client_custom = None
    try:
        # --- Authentication Setup ---
        logger.info("Setting up authentication...")
        auth_client = AuthClient()
        helper = Helper(auth_client)

        logger.info("\nInitializing API Client with custom settings...")

        # Define custom settings
        # They can be defined within the api_client declaration.
        # However, for the example's clarity, they're declared as variables.
        custom_timeout = 0.1
        custom_retries = 2
        custom_ua = "clientconfig Script"

        api_client_custom = Client(
            timeout=custom_timeout,
            max_retries=custom_retries,
            user_agent=custom_ua
        )
        logger.info("Initialized Client with: timeout=%s, max_retires=%s, user_agent='%s'", custom_timeout, custom_retries, custom_ua)

        token = helper.get_access_token()
        api_client_custom.set_access_token(token)
        logger.info("Successfully authenticated custom client!")

        logger.info("\n--- Demonstrating Custom Timeout ---")

        # --- Demonstrate Timeout ---
        logger.info("\nAttempting an API call expected to timeout (timeout=0.1s)...")
        try:
            req_empty_codes = Request()
            _ = api_client_custom.get_codes(req_empty_codes)
            logger.error("Error: The API call succeeded unexpectedly with a 0.1s timeout!")
        except APIRequestError as e:
            if isinstance(e.__cause__, httpx.TimeoutException):
                logger.info("Success! Caught expected timeout error: %s", e)
            else:
                logger.warning("Caught an APIRequestError, but it wasn't a timeout: %s", e, exc_info=True)
        except httpx.TimeoutException as e:
            logger.info("Success! Caught expected httpx.TimeoutException directly: %s", e)
        except Exception as e:
            logger.error("Caught an unexpected error during the timeout test: %s", exc_info=True)

    except (APIRequestError, APIStatusError, APIDataError) as e:
        logger.warning("API Error occurred (might be expected): %s", e)
    except ValueError as e:
        logger.fatal("Configuration Error (check .env?): %s", e)
    except Exception as e:
        logger.fatal("An unexpected error occurred: %s", e, exc_info=True)
    finally:
        # --- Graceful Shutdown ---
        if helper:
            logger.info("Shutting down helper and revoking tokens...")
            helper.stop()
        elif auth_client:
            auth_client.close()
        logger.info("Exiting.")

if __name__ == "__main__":
    main()
