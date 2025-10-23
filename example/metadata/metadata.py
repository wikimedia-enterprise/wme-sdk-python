# pylint: disable=C0103, W0621, W0718, R0912, R0914, R0915

"""
Demonstrates fetching metadata for codes, languages, projects, and namespaces
using the Wikimedia Enterprise API.
"""

import sys
import os
import logging
import json

# --- Add project root to sys.path ---
try:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)
except NameError:
    PROJECT_ROOT = os.path.abspath('.')
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

# --- Import custom modules ---
try:
    from modules.auth.auth_client import AuthClient
    from modules.auth.helper import Helper
    from modules.api.api_client import Client, Request, Filter
    from modules.api.exceptions import APIRequestError, APIStatusError, APIDataError
except ImportError as e:
    print("Error: Failed to import modules. Make sure you're running from the project's root")
    print("       or that '%s' is correct.", PROJECT_ROOT)
    print("Details: %s", e)
    sys.exit(1)

# --- Setup Logging ---
# You can set the level below to DEBUG for more detail.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Runs the main demo of the Metadata API"""
    helper = None
    auth_client = None
    try:
        # --- Authentication Setup ---
        logger.info("Setting up authentication...")
        auth_client = AuthClient()
        helper = Helper(auth_client)
        api_client = Client()

        token = helper.get_access_token()
        api_client.set_access_token(token)
        logger.info("Succesfully authenticated!")

        logger.info("\nStarting Metadata API examples...")

        logger.info("\n--- Project Codes ---")
        # --- Use Case 1: Get all codes ---
        logger.info("\n --- Use Case 1: Get all codes ---")
        logger.info("\n1) Get all project codes:")
        req_empty = Request()
        all_codes = api_client.get_codes(req_empty)
        logger.info("Found %s project codes", len(all_codes))
        if all_codes:
            logger.info("First code details:")
            logger.info(json.dumps(all_codes[0], indent=2, ensure_ascii=False))

        # --- Use case 2: Select only the 'identifier' field ---
        logger.info("\n2) Get only the 'identifier' field for all codes:")
        req_fields = Request(fields=["identifier"])
        codes_identifiers = api_client.get_codes(req_fields)
        logger.info("Identifiers found:")
        logger.info(json.dumps(codes_identifiers, indent=2, ensure_ascii=False))

        # --- Use case 3: Filter for 'wiki' and select 'identifier' ---
        logger.info("\n3) Filter for code 'wiki' and select 'identifier':")
        wiki_filter = Filter("identifier", "wiki")
        req_filtered_fields = Request(fields=['identifier'], filters=[wiki_filter])
        filtered_codes = api_client.get_codes(req_filtered_fields)
        logger.info("Filtered result:")
        logger.info(json.dumps(filtered_codes, indent=2, ensure_ascii=False))

        # --- Use case 4: Query a specific code ('wikitionary') ---
        logger.info("\n4) Get details for specific code 'wiktionary':")
        req_empty_for_single = Request() # Still need a Request obj, even if empty
        wiktionary_code = api_client.get_code("wiktionary", req_empty_for_single)
        logger.info("Wiktionary details:")
        logger.info(json.dumps(wiktionary_code, indent=2, ensure_ascii=False))

        # --- Use case 5: Query 'wikitionary' and select 'identifier' ---
        logger.info("\n5) Get 'identifier' for specific code 'wiktionary':")
        req_specific_field = Request(fields=["identifier"])
        wiktionary_identifier = api_client.get_code("wiktionary", req_specific_field)
        logger.info("Wiktionary identifier only:")
        logger.info(json.dumps(wiktionary_identifier, indent=2, ensure_ascii=False))

        logger.info("\n--- Languages ---")

        # --- Use case 1: Get all languages ---
        logger.info("\n1) Get all supported languages:")
        req_empty_lang = Request()
        all_languages = api_client.get_languages(req_empty_lang)
        logger.info("Found %s languages.", len(all_languages))
        if all_languages:
            # We get English and Arabic to showcase different writing directions
            en_lang = next((lang for lang in all_languages if lang.get('identifier') == 'en'), None)
            ar_lang = next((lang for lang in all_languages if lang.get('identifier') == 'ar'), None)
            if en_lang:
                logger.info("Details for English ('en'):")
                logger.info(json.dumps(en_lang, indent=2, ensure_ascii=False))
            if ar_lang:
                logger.info("Details for Arabic ('ar'):")
                logger.info(json.dumps(ar_lang, indent=2, ensure_ascii=False))

        # --- Use Case 2: Query a specific language ('es') ---
        logger.info("\n2) Get details for specific language 'es' (Spanish):")
        req_empty_for_single_lang = Request()
        spanish_language = api_client.get_language("es", req_empty_for_single_lang)
        logger.info("Spanish details:")
        logger.info(json.dumps(spanish_language, indent=2, ensure_ascii=False))

        logger.info("\n--- Projects ---")
        # --- Use Case 1: Get all projects ---
        logger.info("\n1) Get metadata for all supported projects:")
        req_empty_proj = Request()
        all_projects = api_client.get_projects(req_empty_proj)
        logger.info("Found %s projects.", len(all_projects))
        if all_projects:
            # For example brevity, we'll focus on English Wikipedia
            enwiki_proj = next((proj for proj in all_projects if proj.get('identifier') == 'enwiki'), None)
            if enwiki_proj:
                logger.info("Details for English Wikipedia ('enwiki'):")
                logger.info(json.dumps(enwiki_proj, indent=2, ensure_ascii=False))
            else:
                logger.info("Could not find 'enwiki' in the full list. This was not supposed to happen!")

        # --- Use Case 2: Filter projects (e.g., English language) & select fields ---
        logger.info("\n2) Get 'identifier' and 'url' for English language projects:")
        en_lang_filter = Filter("in_language.identifier", "en")
        req_en_filtered = Request(fields=["identifier", "url"], filters=[en_lang_filter])
        en_projects = api_client.get_projects(req_en_filtered)
        logger.info("Found %s projects for language 'en'.", len(en_projects))
        logger.info("English project identifiers and URLs:")
        logger.info(json.dumps(en_projects, indent=2, ensure_ascii=False))

        # --- Use Case 3: Query a specific project ('eswiki') ---
        logger.info("\n3) Get details for specific project 'eswiki' (Spanish Wikipedia):")
        req_empty_single_proj = Request()
        eswiki_project = api_client.get_project("eswiki", req_empty_single_proj)
        logger.info("Spanish Wikipedia details:")
        logger.info(json.dumps(eswiki_project, indent=2, ensure_ascii=False))

        # --- Use Case 4: Query 'eswiki' and select fields ---
        logger.info("\n4) Get 'name' and 'url' for specific project 'eswiki':")
        req_eswiki_fields = Request(fields=["name", "url"])
        eswiki_project_fields = api_client.get_project("eswiki", req_eswiki_fields)
        logger.info("Spanish Wikipedia name and URL:")
        logger.info(json.dumps(eswiki_project_fields, indent=2, ensure_ascii=False))

        logger.info("\n--- Namespaces ---")

        # --- Use Case 1: Get all namespaces ---
        logger.info("\n1) Get metadata for all supported namespaces:")
        req_empty_ns = Request()
        all_namespaces = api_client.get_namespaces(req_empty_ns)
        logger.info("Found %s namespaces.", len(all_namespaces))
        logger.info("Namespace details:")
        logger.info(json.dumps(all_namespaces, indent=2, ensure_ascii=False))

        # --- Use Case 2: Query a specific namespace (ID 0) ---
        logger.info("\n2) Get details for specific namespace ID 0 (Articles):")
        req_empty_single_ns = Request()
        namespace_0 = api_client.get_namespace(0, req_empty_single_ns)
        logger.info("Namespace 0 details:")
        logger.info(json.dumps(namespace_0, indent=2, ensure_ascii=False))

        # --- End of Metadata Examples ---
        logger.info("\n--- Metadata API examples complete!")


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
        elif auth_client:
            auth_client.close()
        logger.info("Exiting!")

if __name__ == "__main__":
    main()
