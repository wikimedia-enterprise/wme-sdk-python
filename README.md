# Wikimedia Enterprise SDK: Python

Official Wikimedia Enterprise SDK for Go programming language.

See our [api documentation](https://enterprise.wikimedia.com/docs/) and [website](https://enterprise.wikimedia.com/) for more information about the APIs.

## Getting started

- installing the SDK:

```bash
git clone https://github.com/wikimedia-enterprise/wme-sdk-python.git
cd wme-sdk-python
pip install -r requirements.txt
```

- expose your credentials (if you don't have credentials already, [sign up](https://dashboard.enterprise.wikimedia.com/signup/)):

```bash
export WME_USERNAME="...your username...";
export WME_PASSWORD="...your password...";
```

- obtain your access token:

```python
import time
import logging
import threading
// find the auth_client module in the sdk, file: modules/auth/auth_client.py
from auth_client import AuthClient, Helper

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

Auth APIs
The following are the main authentication APIs provided by the SDK:

Login
RefreshToken
RevokeToken
Helper APIs
These helper APIs provide reference implementations for clients on how token state management can be done and how tokens can be used in concurrent processes using WME APIs:

GetAccessToken
ClearState
Example Usage

- putting it all together and making your first API call (we will be querying the Structured Contents endpoint, which is part of the [On-demand API](https://enterprise.wikimedia.com/docs/on-demand/))

```python
import requests
from dotenv import load_dotenv
from wme_sdk import api, auth

def main():
    load_dotenv()
    ath = auth.Client()

    try:
        lgn = ath.login(username=os.getenv("WME_USERNAME"), password=os.getenv("WME_PASSWORD"))
    except Exception as err:
        logging.fatal(err)
        return

    try:
        acl = api.Client()
        acl.set_access_token(lgn['access_token'])

        req = {
            "fields": ["name", "abstract"],
            "filters": [
                {
                    "field": "in_language.identifier",
                    "value": "en",
                }
            ]
        }

        scs = acl.get_structured_contents("Squirrel", req)
        for sct in scs:
            logging.info(sct['name'])
            logging.info(sct['abstract'])
    except Exception as err:
        logging.fatal(err)
    finally:
        try:
            ath.revoke_token(refresh_token=lgn['refresh_token'])
        except Exception as err:
            logging.error(err)

if __name__ == "__main__":
    main()


```

- additional examples, such as connecting to the [streaming API](/example/streaming/), can be found [here](/example/)
