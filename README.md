# Wikimedia Enterprise SDK: Python

Draft Wikimedia Enterprise SDK for the Python programming language. This SDK is supposed to serve as an example Python SDK for Wikimedia Enterprise APIs. The SDK is not fully working yet.

See our [api documentation](https://enterprise.wikimedia.com/docs/) and [website](https://enterprise.wikimedia.com/) for more information about the APIs.

## Getting started

- Install the SDK:

```bash
$ git clone https://github.com/wikimedia-enterprise/wme-sdk-python.git
$ cd wme-sdk-python

# Edit the `sample.env` file with your credentials and save it as `.env`. Don't give your WME credentials to anyone!
# By the end of this step, you'll have a .env file that looks like, with your username and password:
#   WME_USERNAME=username
#   WME_PASSWORD=password
#   PYTHONPATH=.


# Set up the virtual environment
$ python3 -m venv sdk
$ . sdk/bin/activate

# Install the dependencies
$ pip install -r requirements.txt

# Run the on-demand example
$ python3 -m example.ondemand.ondemand

# Run the structured contents example
$ python3 -m example.structured-contents.structuredcontents

# Exit the virtual environment
$ deactivate
```

- Expose your credentials (if you don't have credentials yet, [sign up](https://dashboard.enterprise.wikimedia.com/signup/)) without a `.env` file:

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
