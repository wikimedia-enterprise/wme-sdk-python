# pylint: disable=W0718, R0914, R0801, W0612

"""
Demonstrates the ability to stop a client callback midway through processing.

This script connects to the real-time article stream and uses the callback's
boolean return value to stop the stream after receiving 5 articles.
"""

import logging
import time

# --- Import custom modules ---
from modules.auth.auth_client import AuthClient
from modules.auth.helper import Helper
from modules.api.api_client import Client, Request
from modules.api.exceptions import APIRequestError, APIStatusError, APIDataError

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Configuration ---
STOP_AFTER_N_ARTICLES = 5

def main():
    """Runs the callback stop demo"""
    helper = None
    auth_client = None

    articles_received_tracker = []

    def stream_callback(article: dict) -> bool:
        """
        Callback function to process streamed articles.

        This callback will log the received article and check if it's
        time to stop the stream.

        Args:
            article (dict): The JSON object for the article.

        Returns:
            bool: True to continue processing, False to stop the stream.
        """
        try:
            article_name = article.get('name', article.get('identifier', 'Unknown'))
            event_id = article.get('event', {}).get('identifier', 'unknown_event')

            logger.info(
                "[%s] Received article (event: %s): %s",
                len(articles_received_tracker) + 1,
                event_id,
                article_name
            )

            articles_received_tracker.append(article)

            # --- The Stop Logic ---
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

    except (APIRequestError, APIStatusError, APIDataError) as e:
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
