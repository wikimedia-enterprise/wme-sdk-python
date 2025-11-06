# pylint: disable=W0718, R0912, R0914, R0915, R0801

"""
Demonstrates fetching metadata for Wikimedia snapshots using the Wikimedia API
"""

import logging
import json
import time
import io

# --- Import custom modules ---
from modules.auth.auth_client import AuthClient
from modules.auth.helper import Helper
from modules.api.api_client import Client, Request
from modules.api.snapshot import Snapshot
from modules.api.exceptions import APIRequestError, APIStatusError, APIDataError

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Runs the snapshots demo"""
    helper = None

    with AuthClient() as auth_client:
        try:
            # --- Authentication Setup ---
            logger.info("Setting up authentication...")

            helper = Helper(auth_client)
            api_client = Client()

            token = helper.get_access_token()
            api_client.set_access_token(token)
            logger.info("Succesfully authenticated!")

            logger.info("\nStarting Snapshot examples...")

            # Define fields once to be reused
            snapshot_fields = [
                "identifier", "version", "date_modified", "is_part_of",
                "in_language", "namespace", "size"
            ]

            # --- Use case 1: Get metadata of all available Snapshots (Limit 3) ---
            logger.info("\n--- 1. Get metadata of all available Snapshots (Limit 3) ---")
            req_all = Request(fields=snapshot_fields)
            all_snapshots = api_client.get_snapshots(req_all)
            all_snapshots_limited = all_snapshots[:3]

            if all_snapshots_limited:
                all_snapshots_json = [Snapshot.to_json(s) for s in all_snapshots_limited]
                logger.info(json.dumps(all_snapshots_json, indent=2, ensure_ascii=False))

            # --- Use case 2: Get metadata of English Snapshots (Limit 3) ---
            logger.info("\n--- 2. Get metadata of English Snapshots (Limit 3) ---")
            ss_filter = {"in_language.identifier": "en"}
            req_filtered = Request(fields=snapshot_fields, filters=ss_filter)
            en_snapshots = api_client.get_snapshots(req_filtered)
            en_snapshots_limited = en_snapshots[:3]

            if en_snapshots_limited:
                en_snapshots_json = [Snapshot.to_json(s) for s in en_snapshots_limited]
                logger.info("Filtered English Snapshots:")
                logger.info(json.dumps(en_snapshots_json, indent=2, ensure_ascii=False))

            # --- Use case 3: Get metadata of a single snapshot ---
            logger.info("\n--- 3. Get metadata of a single snapshot (eswiki) ---")
            req_single_ss = Request(fields=snapshot_fields)
            es_snapshot = api_client.get_snapshot("eswiki_namespace_0", req_single_ss)
            if es_snapshot:
                es_snapshot_json = Snapshot.to_json(es_snapshot)
                logger.info("Single snapshot (eswiki_namespace_0):")
                logger.info(json.dumps(es_snapshot_json, indent=2, ensure_ascii=False))

            # --- Use case 4: Get HEAD info for a single snapshot ---
            target_snapshot_id = "eswikibooks_namespace_0"
            logger.info("\n--- 4. Get HEAD metadata for snapshot '%s' ---", target_snapshot_id)
            try:
                snapshot_headers = api_client.head_snapshot(target_snapshot_id)
                logger.info("Headers for '%s':", target_snapshot_id)
                logger.info(json.dumps(snapshot_headers, indent=2, ensure_ascii=False))
                content_length = snapshot_headers.get('Content-Length', 0)
                logger.info("Content-Length from HEAD: %s bytes", content_length)
            except APIStatusError as e:
                logger.warning("Could not get HEAD for '%s'. Maybe it's unavailable? Error: %s", target_snapshot_id, e)
                content_length = 0

            # --- Use case 5: Download and read a snapshot ---
            logger.info("\n--- 5. Download and read snapshot '%s' ---", target_snapshot_id)

            if content_length == 0:
                logger.warning("Skipping download, '%s' reported zero size or HEAD failed.", target_snapshot_id)
            else:
                logger.info("Downloading '%s' (%s bytes) into memory...", target_snapshot_id, content_length)
                start_time = time.time()
                with io.BytesIO() as buffer:
                    api_client.download_snapshot(target_snapshot_id, buffer)
                    end_time = time.time()
                    size_mb = buffer.getbuffer().nbytes / (1024 * 1024)
                    logger.info("Downloaded %.2f MB in %.2f s", size_mb, end_time - start_time)

                    logger.info("Processing the downloaded archive...")
                    buffer.seek(0)

                    articles_found_in_snapshot = []
                    def snapshot_article_callback(article_json: dict) -> bool:
                        """Simple callback to collect article names"""
                        if 'name' in article_json:
                            articles_found_in_snapshot.append(article_json['name'])
                        elif 'identifier' in article_json:
                            articles_found_in_snapshot.append(article_json['identifier'])

                        if len(articles_found_in_snapshot) >= 5:
                            return False
                        return True

                    try:
                        api_client.read_all(buffer, snapshot_article_callback)
                        logger.info("Succesfully processed %s articles from snapshot.", len(articles_found_in_snapshot))
                        if articles_found_in_snapshot:
                            logger.info("First %d article names/identifiers: %s",
                                        len(articles_found_in_snapshot),
                                        articles_found_in_snapshot)
                    except APIDataError as e:
                        logger.error("Error processing snapshot archive: %s", e)
                    except Exception as e:
                        logger.error("Unexpected error processing snapshot content: %s", e, exc_info=True)

            logger.info("\n--- Snapshot API examples complete ---")

        except (APIRequestError, APIStatusError, APIDataError) as e:
            logger.fatal("API Error encountered: %s", e)
        except ValueError as e:
            logger.fatal("Configuration Error (check .env): %s", e)
        except Exception as e:
            logger.fatal("An unexpected error ocurred: %s", e, exc_info=True)
        finally:
            # --- Graceful Shutdown ---
            if helper:
                logger.info("Shutting down helper and revoking tokens...")
                helper.stop()
            logger.info("Exiting!")

if __name__ == "__main__":
    main()
