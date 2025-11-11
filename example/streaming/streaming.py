# pylint: disable=R0801, C0103, W0718

"""Demonstrates streaming articles from the API using a callback.

This script demonstrates how to authenticate using the AuthClient's
managed lifecycle, build a request for specific article fields,
and then use the `stream_articles` method.

Each Article object received from the stream is passed to the
`article_callback` function, which logs its details. The script
handles graceful shutdown on (Ctrl+C) and cleans up the auth state.
"""

import logging
from httpx import RequestError, HTTPStatusError

# --- Import custom modules ---
from modules.auth.auth_client import AuthClient
from modules.api.api_client import Client, Request
from modules.api.article import Article
from modules.api.exceptions import APIRequestError, APIStatusError, APIDataError, DataModelError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def article_callback(article: Article) -> bool:
    """A callback function to process each article received from the stream.

    This function is invoked by `api_client.stream_articles` for each
    Article object. It logs the article's name, abstract, and event identifier.

    Args:
        article (Article): The Article data object received from the stream.

    Returns:
        bool: True to continue streaming, False to stop.
    """
    logger.info("----------START-----------")

    logger.info("name: %s", article.name)
    logger.info("abstract: %s", article.abstract)

    event_id = article.event.identifier if article.event else "N/A"
    logger.info("event.identifiers: %s", event_id)

    logger.info("-----------END------------\n\n\n")

    return True


def main():
    """Main execution function to initiate the article stream.

    Orchestrates the entire process:
    1. Authenticates with the AuthClient, which handles the full token lifecycle.
    2. Initializes the API Client with the access token.
    3. Defines a Request for specific fields.
    4. Starts the article stream, passing the `article_callback`.
    5. Listens for KeyboardInterrupt (Ctrl+C) to stop.
    6. Clears the authentication state (revokes token, deletes file) on exit.
    """

    with AuthClient() as auth_client:
        try:
            logger.info("Authenticating...")
            access_token = auth_client.get_access_token()

            api_client = Client()
            api_client.set_access_token(access_token)
            logger.info("Authentication successful. Starting stream... (Press Ctrl+C to stop)")

            request = Request(
                fields=["name", "abstract", "event.*"]
            )

            api_client.stream_articles(request, article_callback)

        except KeyboardInterrupt:
            logger.info("\nStream stopped by user.")
        except (RequestError, HTTPStatusError) as e:
            logger.fatal("Authentication failed: %s", e)
        except (APIRequestError, APIStatusError, APIDataError, DataModelError) as e:
            logger.fatal("Error during stream: %s", e)
        except Exception as e:
            logger.fatal("An unexpected error occurred: %s", e, exc_info=True)
        finally:
            logger.info("Cleaning up authentication state...")
            auth_client.clear_state()
            logger.info("Cleanup complete.")


if __name__ == "__main__":
    main()
