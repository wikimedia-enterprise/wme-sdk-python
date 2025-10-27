# Example: Custom API Client Configuration

This script demonstrates how to configure the `Client` from the WME API SDK with custom HTTP settings. It specifically shows how to set a custom **timeout**, **max\_retries**, and **User-Agent** string.

The primary demonstration is to set an extremely low timeout (`0.1s`) and then correctly catch the `APIRequestError` (wrapping an `httpx.TimeoutException`) that this intentionally causes.

## Prerequisites

Before running this script, you must have your environment set up.

1.  **Environment Variables:** The script requires user credentials to authenticate with the API. Ensure the following environment variables are set on the .env file:

    ```bash
    WME_USERNAME="your_username"
    WME_PASSWORD="your_password"
    ```

2.  **Python Dependencies:** You must have the required packages, like `httpx` and the SDK's modules, available in your Python environment.

## How to Run

This script is designed to be run from the **virtual enviroment** of the SDK. Once within the virtual enviroment, execute the script:

```bash
python -m example.client_config.clientconfig
```

## Expected Output

The script is considered **successful** when it logs that it *caught the expected timeout error*. This proves the custom `timeout=0.1` setting was correctly applied.

You should see output similar to this:

```
INFO:__main__:Setting up authentication...
INFO:__main__:
Initializing API Client with custom settings...
INFO:__main__:Initialized Client with: timeout=0.1, max_retires=2, user_agent='clientconfig Script'
INFO:__main__:Successfully authenticated custom client!

INFO:__main__:--- Demonstrating Custom Timeout ---

INFO:__main__:Attempting an API call expected to timeout (timeout=0.1s)...
INFO:__main__:Success! Caught expected timeout error: Request Error: An error occurred while requesting POST https://api.enterprise.wikimedia.com/v2/codes (Details: Read timed out)
INFO:__main__:Shutting down helper and revoking tokens...
INFO:__main__:Exiting.
```

If you instead see `Error: The API call succeeded unexpectedly...`, it means your network connection was somehow fast enough to complete the request and get a response in under 0.1 seconds, which is highly unlikely but technically possible.
