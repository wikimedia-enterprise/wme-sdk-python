# Wikimedia Enterprise Python SDK

This document outlines the features and usage of the Python client for the Wikimedia Enterprise API. This client provides a convenient, high-performance interface for all API v2 endpoints, handling authentication, parallel downloads, data processing, and real-time streaming.

It is built using httpx for a modern, high-performance HTTP experience, including support for HTTP/2.

See our [api documentation](https://enterprise.wikimedia.com/docs/) and [website](https://enterprise.wikimedia.com/) for more information about the APIs.

## Key Features

  * **Comprehensive API Coverage**: Provides methods for all major API entities, including:
      * Projects, Languages, Namespaces, and Codes
      * Daily Batches
      * Article Snapshots (full and structured)
      * Snapshot Chunks
      * Real-time Article Streams
  * **High-Performance Downloads**:
      * **Parallel Chunked Downloads**: Large files (like snapshots or batches) are downloaded in parallel chunks using a thread pool for maximum speed.
      * **Configurable Concurrency**: You can set the chunk size (`download_chunk_size`) and number of concurrent workers (`download_concurrency`).
  * **Efficient Archive Processing**:
      * **Multi-threaded Decompression**: Uses the high-performance `zlib-ng` library to decompress `.tar.gz` archives using multiple threads.
      * **Streaming Archive Reader**: Reads and processes NDJSON files directly from the archive stream without needing to extract them to disk first.
  * **Real-time Event Streaming**:
      * Includes a `stream_articles` method to connect to the real-time event stream endpoint (`realtime.enterprise.wikimedia.com`) and process articles as they are published.
  * **Robust Request Handling**:
      * **Automatic Retries**: Automatically retries failed requests (e.g., 5xx errors, 429 rate limits) up to a configurable `max_retries` count.
      * **Client-Side Rate Limiting**: Can be configured with `rate_limit_per_second` to avoid hitting server-side rate limits.
      * **Custom Exceptions**: Raises clear, specific exceptions (`APIStatusError`, `APIRequestError`, `APIDataError`) for easy error handling.
  * **Flexible Query Building**:
      * Includes `Request` and `Filter` helper classes to easily construct complex API request payloads for filtering, field selection, and pagination (`since`, `limit`, `offsets`, etc.).

## Getting started

Before starting, ensure Python is installed in your system. We recommend using a stable Python version such as 3.13 as of the time of writing.

- Install the SDK:

```bash
$ git clone https://github.com/wikimedia-enterprise/wme-sdk-python.git
$ cd wme-sdk-python
```

Edit the `sample.env` file with your credentials and save it as `.env`. Don't give your WME credentials to anyone! By the end of this step, you'll have a .env file that looks like, with your username and password:

```bash
WME_USERNAME=username
WME_PASSWORD=password
PYTHONPATH=.
```

- Set up the virtual environment
```bash
python3 -m venv sdk
```

- Activate the virtual enviroment
```bash
. sdk/bin/activate (On Mac or Linux systems)
.\sdk\Scripts\Activate.ps1 (On Windows PowerShell)
sdk\Scripts\activate (On Windows CMD)
```

- Install the dependencies
  
After activating the virtual enviroment, execute this command to install all dependencies:
```bash
pip install -r requirements.txt
```

- To exit the virtual environment
```
deactivate
```

# Expose your credentials without a `.env` file:
If you don't have credentials yet, [sign up](https://dashboard.enterprise.wikimedia.com/signup/)
```bash
export WME_USERNAME="...your username...";
export WME_PASSWORD="...your password...";
export PYTHONPATH=.
```

- Obtain your access token:

```python
import time
import logging
import threading
# find the auth_client module in the sdk, file: modules/auth/auth_client.py
from modules.auth.auth_client import AuthClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def refresh_token_periodically(helper, stop_event):
    while not stop_event.is_set():
        if stop_event.wait(23 * 3600 + 59):
            continue
        with helper.lock:
            try:
                helper.get_access_token()
                logger.info("Token refreshed successfully")
            except Exception as e:
                logger.error(f"Failed to refresh token: {e}")


def main():
    auth_client = AuthClient()
    try:
        helper = Helper(auth_client)
    except Exception as e:
        logger.fatal(f"Failed to create helper: {e}")
        return

    stop_event = threading.Event()
    refresh_thread = threading.Thread(target=refresh_token_periodically, args=(helper, stop_event))
    refresh_thread.start()

    try:
        while True:
            with helper.lock:
                try:
                    token = helper.get_access_token()
                    logger.info(f"Access token: {token}")
                except Exception as e:
                    logger.fatal(f"Failed to get token: {e}")
                    return

            stop_event.set()  # Signal the refresh routine to reset the timer
            time.sleep(60)
            stop_event.clear()
    finally:
        stop_event.set()
        refresh_thread.join()


if __name__ == "__main__":
    main()
```

## Auth APIs
The following are the main authentication APIs provided by the SDK:

- Login
- RefreshToken
- RevokeToken

## Helper APIs

These helper APIs provide reference implementations for clients on how token state management can be done and how tokens can be used in concurrent processes using WME APIs:

- GetAccessToken
- ClearState

### Example Usage

Putting it all together and making your first API call (we will be querying the Structured Contents endpoint, which is part of the [On-demand API](https://enterprise.wikimedia.com/docs/on-demand/))

```python
import time
import logging
import json
import sys

from modules.auth.helper import Helper
from modules.auth.auth_client import AuthClient
from modules.api.api_client import Client, Request, Filter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    auth_client = AuthClient()
    try:
        helper = Helper(auth_client)
    except Exception as e:
        logger.fatal(f"Failed to create helper: {e}")
        return

    try:
        token = helper.get_access_token()
        logger.info(f"Access token: {token}")

        # Use the token to get articles from the API
        api_client = Client()
        api_client.set_access_token(token)

        request = Request(
            fields=["name", "abstract", "url", "version"],
            filters=[Filter(field="in_language.identifier", value="en")]
        )

        try:
            articles = api_client.get_articles("Montreal", request)
        except Exception as e:
            logger.fatal(f"Failed to get articles: {e}")
            return

        for article in articles:
            try:
                art_json = json.dumps(article, indent=2)
                print(art_json)
            except Exception as e:
                logger.error(f"Failed to serialize article: {e}")

    except Exception as e:
        logger.error(f"Failed to get access token: {e}")
    finally:
        helper.stop()
        logger.info("Exiting")
        time.sleep(1)


def usage():
    print(f"""Usage: {sys.argv[0]}""")


if __name__ == "__main__":
    main()
```

Additional examples, such as connecting to the [streaming API](/example/streaming/), can be found [here](/example/)


## Additional parameters

`api_client.Client` can be configured to download snapshots or chunks in multiple requests, see its implementation for more details. Be aware that doing so will likely consume more quota, compared to downloading one entity per request.
