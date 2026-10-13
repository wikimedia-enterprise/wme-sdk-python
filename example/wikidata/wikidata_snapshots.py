"""
Example script demonstrating how to interact with the Wikidata bulk endpoints
using the Wikimedia Enterprise Python SDK.
"""

import time
import logging
import json

from modules.auth.helper import Helper
from modules.auth.auth_client import AuthClient
from modules.api.api_client import Client
from modules.api.snapshot import Snapshot
from modules.api.exceptions import WikimediaAPIError
from modules.api.article import Article

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main execution function for the Wikidata snapshots example."""
    auth_client = AuthClient()
    try:
        helper = Helper(auth_client)
    except ValueError as e:
        logger.fatal("Failed to create auth helper. Missing credentials? %s", e)
        return

    try:
        token = helper.get_access_token()
        logger.info("Successfully obtained access token.")

        api_client = Client()
        api_client.set_access_token(token)

        logger.info("--- Fetching available Wikidata snapshots ---")
        snapshots = api_client.get_wikidata_snapshots()
        for snap in snapshots:
            print(f"Snapshot Identifier: {snap.identifier} | Version: {snap.version}")

        logger.info("--- Fetching 'properties' snapshot metadata ---")
        properties_snap = api_client.get_wikidata_snapshot("properties")

        print(json.dumps(Snapshot.to_json(properties_snap), indent=2))

        logger.info("--- Streaming first 3 entities from 'properties' ---")
        counter = 0

        def read_callback(entity: Article) -> bool:
            """
            Callback function to process each entity in the NDJSON stream.
            Returns True to continue reading, False to stop.
            """
            nonlocal counter
            print(json.dumps(Article.to_json(entity), indent=2))
            counter += 1
            return counter < 3

        api_client.read_wikidata_snapshot("properties", read_callback)

    except WikimediaAPIError as e:
        logger.error("A Wikimedia API error occurred: %s", e)
    finally:
        helper.stop()
        logger.info("Exiting")
        time.sleep(1)

if __name__ == "__main__":
    main()
