# pylint: disable=R0801, C0103, W0718

"""Demonstrates fetching metadata for structured content snapshots.

This script authenticates with the Wikimedia Enterprise API and performs
two actions:
1. Fetches metadata for all available structured content snapshots.
2. Fetches metadata for a single, specific snapshot ("enwiki_namespace_0")
   using a request filter.

It logs the modification date, identifier, and size for the results of
both calls. The script also ensures the authentication state is cleared
upon exit.
"""

import logging
from httpx import RequestError, HTTPStatusError

# --- Import custom modules ---
from modules.auth.auth_client import AuthClient
from modules.api.api_client import Client, Request
from modules.api.exceptions import APIRequestError, APIStatusError, APIDataError, DataModelError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Main execution function to fetch and display snapshot metadata.

    Orchestrates the entire process:
    1. Authenticates with the AuthClient, which handles the full token lifecycle.
    2. Initializes the API Client with the access token.
    3. Fetches and logs metadata for *all* available snapshots.
    4. Defines a filter and fetches and logs metadata for a *single*
       specific snapshot ("enwiki_namespace_0").
    5. Clears the authentication state (revokes token, deletes file) on exit.
    """
    with AuthClient() as auth_client:
        try:
            logger.info("Authenticating...")
            access_token = auth_client.get_access_token()

            api_client = Client()
            api_client.set_access_token(access_token)
            logger.info("Authentication successful. Fetching content...")

            logger.info("\n--- All Structured Snapshots ---")

            request_all = Request(fields=["identifier", "name", "date_modified"])

            structured_snapshots = api_client.get_structured_snapshots(request_all)

            logger.info("Found %d total structured snapshots.", len(structured_snapshots))

            for content in structured_snapshots[:3]:
                logger.info("  Identifier: %s", content.identifier)
                logger.info("  Name: %s", content.name)
                logger.info("  Date Modified: %s", content.date_modified)
                logger.info("  ---")
            if len(structured_snapshots) > 3:
                logger.info("  (and %d more...)", len(structured_snapshots) - 3)

            logger.info("\n--- Single Structured Snapshot ---")

            filters = {
                "in_language.identifier": "en"
            }

            request_single = Request(
                fields=["identifier", "name", "date_modified"],
                filters=filters
            )
            snapshot_id = "enwiki_namespace_0"

            structured_snapshot = api_client.get_structured_snapshot(snapshot_id, request_single)

            if structured_snapshot:
                logger.info("Identifier: %s", structured_snapshot.identifier)
                logger.info("Name: %s", structured_snapshot.name)
                logger.info("Date Modified: %s", structured_snapshot.date_modified)
            else:
                logger.info("Could not find snapshot with ID: %s", snapshot_id)

        except (RequestError, HTTPStatusError) as e:
            logger.fatal("Authentication failed: %s", e)
        except (APIRequestError, APIStatusError, APIDataError, DataModelError) as e:
            logger.fatal("Failed to get structured content snapshots: %s", e)
        except Exception as e:
            logger.fatal("An unexpected error occurred: %s", e, exc_info=True)
        finally:
            logger.info("\nCleaning up authentication state...")
            auth_client.clear_state()
            logger.info("Cleanup complete.")


if __name__ == "__main__":
    main()
