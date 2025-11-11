# pylint: disable=R0801, C0103, W0718

"""Fetches articles matching the query 'Montreal' from the API.

This script demonstrates how to authenticate using the AuthClient's
managed lifecycle, build a request with dictionary-based filters,
and request specific fields.

It then iterates through the resulting Article objects, truncates the
HTML body for concise display, and pretty-prints each article's JSON
to the console.
"""

import json
import logging
from httpx import RequestError, HTTPStatusError

from modules.auth.auth_client import AuthClient
from modules.api.api_client import Client, Request, Article
from modules.api.exceptions import APIRequestError, APIStatusError, APIDataError, DataModelError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Main execution function to fetch and display articles.

    Orchestrates the entire process:
    1. Authenticates with the AuthClient, which handles the full token lifecycle.
    2. Initializes the API Client with the access token.
    3. Defines filters and builds a Request for 'Montreal' articles.
    4. Fetches the articles; exits fatally on failure.
    5. Iterates, truncates the HTML body, and pretty-prints each article
       to the console, logging any serialization errors.
    6. Clears the authentication state (revokes token, deletes file) on exit.
    """

    with AuthClient() as auth_client:
        try:
            logger.info("Getting access token...")
            access_token = auth_client.get_access_token()
            logger.info("Access token retrieved.")

            api_client = Client()
            api_client.set_access_token(access_token)

            # --- Main API Logic ---
            filters = {
                "in_language.identifier": "en",
                "is_part_of.identifier": "enwiki"
            }

            request = Request(
                fields=["name", "abstract", "url", "version", "article_body.html"],
                filters=filters
            )

            logger.info("Fetching articles for 'Montreal'...")
            articles = api_client.get_articles("Montreal", request)
            logger.info("Found %s articles.", len(articles))

            for article in articles:
                try:
                    max_len = 200
                    trunc_marker = "... (truncated)"

                    if (article.article_body and
                        article.article_body.html and
                        len(article.article_body.html) > max_len):

                        html = article.article_body.html
                        article.article_body.html = html[:max_len - len(trunc_marker)] + trunc_marker

                    art_json = json.dumps(Article.to_json(article), indent=2)
                    print(art_json)

                except (TypeError, AttributeError, DataModelError) as e:
                    logger.error("Failed to process or serialize article: %s", e)

        except (RequestError, HTTPStatusError) as e:
            logger.fatal("Authentication failed: %s", e)
        except (APIRequestError, APIStatusError, APIDataError, DataModelError) as e:
            logger.fatal("Failed to get articles: %s", e)
        except Exception as e:
            logger.fatal("An unexpected error occurred: %s", e, exc_info=True)
        finally:
            logger.info("Cleaning up authentication state...")
            auth_client.clear_state()
            logger.info("Cleanup complete.")


if __name__ == "__main__":
    main()
