# pylint: disable=R0801,C0103,W0621, W0718, R0914, R0915
"""
Demonstrates the five main use cases for the Batches API:
    i)   Get metadata for all available batches for a given hour.
    ii)  Get metadata for filtered batches (e.g., by language).
    iii) Get metadata for a single, specific batch.
    iv)  Get HEAD metadata for a single batch.
    v)   Download and read the contents of a batch.

This script uses the AuthClient and Helper for automatic,
thread-safe token management and revocation.
"""

import logging
import json
import io
import time
from datetime import datetime, timedelta, timezone

# --- Import our custom modules ---
from modules.auth.auth_client import AuthClient
from modules.auth.helper import Helper
from modules.api.api_client import Client, Request, Filter
from modules.api.exceptions import APIRequestError, APIStatusError, APIDataError

# --- Setup logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Runs the main demonstration of the Batches API."""
    helper = None
    auth_client = None
    try:
        # --- Authentication Setup ---
        auth_client = AuthClient()

        helper = Helper(auth_client)

        api_client = Client()

        token = helper.get_access_token()
        api_client.set_access_token(token)
        logger.info("Successfully authenticated.")

        # --- Define Batch Timestamp ---
        batch_time = datetime.now(timezone.utc) - timedelta(days=1)
        batch_time = batch_time.replace(hour=10, minute=0, second=0, microsecond=0)
        logger.info("--- Targeting batches for %s ---", batch_time.strftime('%Y-%m-%d %H:00 UTC'))

        # --- Use Case (i): Get metadata for all available batches ---
        logger.info("\n--- i) Get metadata for all available batches ---")
        req_empty = Request()
        all_batches = api_client.get_batches(batch_time, req_empty)
        logger.info("Found %s total batches.", len(all_batches))
        if all_batches:
            logger.info("Metadata for the first batch:")
            logger.info(json.dumps(all_batches[0], indent=2))
        else:
            logger.warning("No batches found for this time.")

        # --- Use Case (ii): Get filtered metadata (English) ---
        logger.info("\n--- ii) Get metadata for 'en' (English) batches ---")
        en_filter = Filter(field="in_language.identifier", value="en")
        req_filtered = Request(filters=[en_filter])
        en_batches = api_client.get_batches(batch_time, req_filtered)
        logger.info("Found %s 'en' batches.", len(en_batches))
        if en_batches:
            logger.info("Metadata for the first 'en' batch:")
            logger.info(json.dumps(en_batches[0], indent=2))

        target_batch_id = "enwiki_namespace_0"

        # --- Use Case (iii): Get metadata for a single batch ---
        logger.info("\n--- iii) Get metadata for a single batch (%s) ---", target_batch_id)
        req_empty = Request()
        single_batch_meta = api_client.get_batch(batch_time, target_batch_id, req_empty)
        logger.info("Metadata for '%s':", target_batch_id)
        logger.info(json.dumps(single_batch_meta, indent=2))

        # --- Use Case (iv): Get HEAD info for a single batch ---
        logger.info("\n--- iv) Get HEAD metadata for a single batch (%s) ---", target_batch_id)
        headers = api_client.head_batch(batch_time, target_batch_id)
        logger.info("Headers for '%s':", target_batch_id)
        logger.info(json.dumps(headers, indent=2))
        content_length = headers.get('Content-Length', 0)
        logger.info("Content-Length from HEAD: %s bytes", content_length)

        # --- Use Case (v): Download and read a batch ---
        logger.info("\n--- v) Download and read a batch (%s) ---", target_batch_id)
        if content_length == 0:
            logger.warning("Skipping download, batch '%s' has no content.", target_batch_id)
            return

        logger.info("Downloading '%s' into an in-memory buffer...", target_batch_id)
        start_time = time.time()

        with io.BytesIO() as buffer:
            api_client.download_batch(batch_time, target_batch_id, buffer)
            end_time = time.time()
            size_mb = buffer.getbuffer().nbytes / (1024 * 1024)
            logger.info("Downloaded %.2f MB in %.2f s", size_mb, end_time - start_time)

            logger.info("Processing the downloaded archive...")
            buffer.seek(0)

            articles_found = []

            def article_callback(article_json):
                """A simple callback to process one article from the batch."""
                if 'identifier' in article_json:
                    articles_found.append(article_json['identifier'])

            api_client.read_all(buffer, article_callback)

            logger.info("Successfully processed %s articles from the batch.", len(articles_found))
            if articles_found:
                logger.info("First 5 article identifiers: %s", articles_found[:5])

    except (APIRequestError, APIStatusError, APIDataError) as e:
        logger.fatal("API Error encountered: %s", e)
    except ValueError as e:
        logger.fatal("Configuration Error: %s", e)
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
