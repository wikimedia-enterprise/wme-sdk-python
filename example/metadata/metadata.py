# pylint: disable=W0718, R0912, R0914, R0915

"""
Demonstrates fetching metadata for codes, languages, projects, and namespaces
using the Wikimedia Enterprise API.

This script shows how to use the refactored, type-safe client to access
metadata objects and their attributes directly.
"""

import logging

# --- Import custom modules ---
from modules.auth.auth_client import AuthClient
from modules.auth.helper import Helper
from modules.api.api_client import Client, Request, Filter
# Import the specific exceptions
from modules.api.exceptions import APIRequestError, APIStatusError, APIDataError, DataModelError

# --- Setup Logging ---
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
        logger.info("\n1) Get all project codes:")
        req_empty = Request()
        all_codes = api_client.get_codes(req_empty)
        logger.info("Found %s project codes", len(all_codes))
        if all_codes:
            first_code = all_codes[0]
            logger.info("First code details:")
            # Access attributes directly, not as a dict
            logger.info("  Identifier: %s", first_code.identifier)
            logger.info("  Name: %s", first_code.name)
            logger.info("  Description: %s", first_code.description)

        # --- Use case 2: Select only the 'identifier' field ---
        logger.info("\n2) Get only the 'identifier' field for all codes:")
        req_fields = Request(fields=["identifier"])
        codes_with_id = api_client.get_codes(req_fields)
        logger.info("Identifiers found (first 5):")
        # The objects will still be Code objects, but fields not
        # requested will be None.
        logger.info([c.identifier for c in codes_with_id[:5]])

        # --- Use case 3: Filter for 'wiki' and select 'identifier' ---
        logger.info("\n3) Filter for code 'wiki' and select 'identifier':")
        wiki_filter = Filter("identifier", "wiki")
        req_filtered_fields = Request(fields=['identifier'], filters=[wiki_filter])
        filtered_codes = api_client.get_codes(req_filtered_fields)
        logger.info("Filtered result:")
        if filtered_codes:
            logger.info("  Identifier: %s", filtered_codes[0].identifier)
        else:
            logger.info("  No code found with identifier 'wiki'.")

        # --- Use case 4: Query a specific code ('wiktionary') ---
        logger.info("\n4) Get details for specific code 'wiktionary':")
        req_empty_for_single = Request() # Still need a Request obj, even if empty
        wiktionary_code = api_client.get_code("wiktionary", req_empty_for_single)
        logger.info("Wiktionary details:")
        logger.info("  Identifier: %s", wiktionary_code.identifier)
        logger.info("  Name: %s", wiktionary_code.name)
        logger.info("  Description: %s", wiktionary_code.description)

        # --- Use case 5: Query 'wiktionary' and select 'identifier' ---
        logger.info("\n5) Get 'identifier' for specific code 'wiktionary':")
        req_specific_field = Request(fields=["identifier"])
        wiktionary_identifier = api_client.get_code("wiktionary", req_specific_field)
        logger.info("Wiktionary identifier only:")
        logger.info("  Identifier: %s", wiktionary_identifier.identifier)
        logger.info("  Name (should be None): %s", wiktionary_identifier.name)


        logger.info("\n--- Languages ---")

        # --- Use case 1: Get all languages ---
        logger.info("\n1) Get all supported languages:")
        req_empty_lang = Request()
        all_languages = api_client.get_languages(req_empty_lang)
        logger.info("Found %s languages.", len(all_languages))
        if all_languages:
            # We get English and Arabic to showcase different writing directions
            en_lang = next((lang for lang in all_languages if lang.identifier == 'en'), None)
            ar_lang = next((lang for lang in all_languages if lang.identifier == 'ar'), None)
            if en_lang:
                logger.info("Details for English ('en'):")
                logger.info("  Identifier: %s, Name: %s, Direction: %s", en_lang.identifier, en_lang.name, en_lang.direction)
            if ar_lang:
                logger.info("Details for Arabic ('ar'):")
                logger.info("  Identifier: %s, Name: %s, Direction: %s", ar_lang.identifier, ar_lang.name, ar_lang.direction)

        # --- Use Case 2: Query a specific language ('es') ---
        logger.info("\n2) Get details for specific language 'es' (Spanish):")
        req_empty_for_single_lang = Request()
        spanish_language = api_client.get_language("es", req_empty_for_single_lang)
        logger.info("Spanish details:")
        logger.info("  Identifier: %s, Name: %s, Direction: %s", spanish_language.identifier, spanish_language.name, spanish_language.direction)


        logger.info("\n--- Projects ---")
        # --- Use Case 1: Get all projects ---
        logger.info("\n1) Get metadata for all supported projects:")
        req_empty_proj = Request()
        all_projects = api_client.get_projects(req_empty_proj)
        logger.info("Found %s projects.", len(all_projects))
        if all_projects:
            enwiki_proj = next((proj for proj in all_projects if proj.identifier == 'enwiki'), None)
            if enwiki_proj:
                logger.info("Details for English Wikipedia ('enwiki'):")
                logger.info("  Identifier: %s, Name: %s, URL: %s", enwiki_proj.identifier, enwiki_proj.name, enwiki_proj.url)
            else:
                logger.info("Could not find 'enwiki' in the full list. This was not supposed to happen!")

        # --- Use Case 2: Filter projects (e.g., English language) & select fields ---
        logger.info("\n2) Get 'identifier' and 'url' for English language projects:")
        en_lang_filter = Filter("in_language.identifier", "en")
        req_en_filtered = Request(fields=["identifier", "url"], filters=[en_lang_filter])
        en_projects = api_client.get_projects(req_en_filtered)
        logger.info("Found %s projects for language 'en'.", len(en_projects))
        logger.info("English project identifiers and URLs (first 5):")
        for proj in en_projects[:5]:
            logger.info("  Identifier: %s, URL: %s", proj.identifier, proj.url)

        # --- Use Case 3: Query a specific project ('eswiki') ---
        logger.info("\n3) Get details for specific project 'eswiki' (Spanish Wikipedia):")
        req_empty_single_proj = Request()
        eswiki_project = api_client.get_project("eswiki", req_empty_single_proj)
        logger.info("Spanish Wikipedia details:")
        logger.info("  Identifier: %s, Name: %s, URL: %s", eswiki_project.identifier, eswiki_project.name, eswiki_project.url)

        # --- Use Case 4: Query 'eswiki' and select fields ---
        logger.info("\n4) Get 'name' and 'url' for specific project 'eswiki':")
        req_eswiki_fields = Request(fields=["name", "url"])
        eswiki_project_fields = api_client.get_project("eswiki", req_eswiki_fields)
        logger.info("Spanish Wikipedia name and URL:")
        logger.info("  Name: %s, URL: %s", eswiki_project_fields.name, eswiki_project_fields.url)
        logger.info("  Identifier (should be None): %s", eswiki_project_fields.identifier)


        logger.info("\n--- Namespaces ---")

        # --- Use Case 1: Get all namespaces ---
        logger.info("\n1) Get metadata for all supported namespaces:")
        req_empty_ns = Request()
        all_namespaces = api_client.get_namespaces(req_empty_ns)
        logger.info("Found %s namespaces.", len(all_namespaces))
        logger.info("Namespace details (first 5):")
        for ns in all_namespaces[:5]:
            logger.info("  ID: %s, Name: %s", ns.identifier, ns.name)

        # --- Use Case 2: Query a specific namespace (ID 0) ---
        logger.info("\n2) Get details for specific namespace ID 0 (Articles):")
        req_empty_single_ns = Request()
        # Use the correct type for the ID (int)
        namespace_0 = api_client.get_namespace(0, req_empty_single_ns)
        logger.info("Namespace 0 details:")
        logger.info("  ID: %s, Name: %s", namespace_0.identifier, namespace_0.name)

        # --- End of Metadata Examples ---
        logger.info("\n--- Metadata API examples complete!")


    except (APIRequestError, APIStatusError, APIDataError, DataModelError) as e:
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
