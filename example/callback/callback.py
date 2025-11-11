# pylint: disable=R0801,C0103,W0621, W0718, R0914, R0915

"""
Demonstrates streaming articles from the API using a typed callback.

This script authenticates with the Wikimedia Enterprise API, sets up a
request for specific article fields (including 'event.*'), and then
uses the `stream_articles` method.

Each strongly-typed `Article` object received from the stream is passed
to the `article_callback` function, which logs its details. The script
uses the callback's boolean return value to stop the stream after
receiving 5 articles.
"""

import logging
import time
import contextlib

# --- Import custom modules ---
from modules.auth.auth_client import AuthClient
from modules.auth.helper import Helper
from modules.api.api_client import Client, Request
from modules.api.article import Article
from modules.api.exceptions import APIRequestError, APIStatusError, APIDataError, DataModelError

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Configuration ---
STOP_AFTER_N_ARTICLES = 5

@contextlib.contextmanager
def revoke_token_on_exit(auth_client, refresh_token):
    """Manages the lifecycle of a refresh token, ensuring revocation on exit."""
    try:
        yield
    finally:
        try:
            auth_client.revoke_token(refresh_token)
        except (APIRequestError, APIStatusError) as e:
            logger.error("Failed to revoke token: %s", e)


def main():
    """Runs the callback stop demo"""
    helper = None
    auth_client = None

    articles_received_tracker = []

    def stream_callback(article: Article) -> bool:
        """
        Callback function to process each article received from the stream.

        This function is invoked by `api_client.stream_articles` for each
        article. It logs the article's name, abstract, and event identifier.

        Args:
            article (Article): The article received from the stream.

        Returns:
            bool: True to continue processing, False to stop the stream.
        """
        try:
            article_name = article.name or article.identifier or 'Unknown'

            event_id = 'unknown_event'
            if article.event:
                event_id = article.event.identifier or 'unknown_event'

            logger.info(
                "[%s] Received article (event: %s): %s",
                len(articles_received_tracker) + 1,
                event_id,
                article_name
            )

            articles_received_tracker.append(article)

            if len(articles_received_tracker) >= STOP_AFTER_N_ARTICLES:
                logger.warning(
                    "Reached stop limit of %s articles. Returning False to stop stream.",
                    STOP_AFTER_N_ARTICLES
                )
                return False

        except Exception as e:
            logger.error("Error within callback function: %s", e)
            return False

        return True

    try:
        # --- Authentication Setup ---
        logger.info("Setting up authentication...")
        auth_client = AuthClient()
        helper = Helper(auth_client)

        api_client = Client(timeout=3600.0)

        token = helper.get_access_token()
        api_client.set_access_token(token)
        logger.info("Succesfully authenticated!")

        # --- Stream Demonstration ---
        logger.info("\nStarting real-time stream callback demo...")

        stream_req = Request(
            fields=["name", "abstract", "event.*"]
        )

        logger.info(
            "Connecting to real-time article stream (will stop after %s articles)...",
            STOP_AFTER_N_ARTICLES
        )

        start_time = time.time()

        api_client.stream_articles(stream_req, stream_callback)

        end_time = time.time()

        logger.info(
            "Stream processing finished. Total articles received: %s",
            len(articles_received_tracker)
        )
        logger.info("Stream was active for %.2f seconds.", end_time - start_time)
        logger.info("\n--- Callback stop demo complete ---")

    except (APIRequestError, APIStatusError, APIDataError, DataModelError) as e:
        logger.fatal("API Error encountered: %s", e)
        if isinstance(e, APIStatusError) and e.response and e.response.status_code == 401:
            logger.error("Got 401 Unauthorized. Check your token permissions for the real-time stream.")
    except ValueError as e:
        logger.fatal("Configuration Error (check .env): %s", e)
    except KeyboardInterrupt:
        logger.info("\nUser interrupted stream. Shutting down.")
    except Exception as e:
        logger.fatal("An unexpected error ocurred: %s", e, exc_info=True)
    finally:
        # --- Graceful Shutdown ---
        if helper:
            logger.info("Shutting down helper and revoking tokens...")
            helper.stop()
        elif auth_client:
            auth_client.close()
        logger.info("Exiting!")

if __name__ == "__main__":
    main()
