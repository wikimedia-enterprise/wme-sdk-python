# Auth Helper Example

This repository contains an example Python application that demonstrates how to use an authentication helper to manage access and refresh tokens for making authenticated API calls easier. The `auth.py` script logs in, checks the validity of tokens, and refreshes the token periodically using a background goroutine.

## Prerequisites

- Python installed on your machine.
- Environment variables for your username and password stored in a `.env` file.

## Setup

### 1. Clone the Repository

```sh
git clone https://github.com/wikimedia-enterprise/wme-sdk-python.git
cd wme-sdk-python

```

### 2. Environment Variables

There is a sample environment file `sample.env` provided in the repository. Rename it to `.env` and add your username and password.

```sh
mv sample.env .env
```

Edit the `.env` file to include your credentials:

```bash
WME_USERNAME=your_username
WME_PASSWORD=your_password
```

### 3. Install Dependencies

Install the necessary Python dependencies:

```sh
pip install -r requirements.txt
```

## Running the Application

To run the application, use the following command:

```sh
cd example/auth
python3 auth.py
```

This will start the application, log in, and display the access token. It will also start a background goroutine that refreshes the token every 23 hours and 59 seconds, or whenever an API call is made.

## Project Structure

- `auth.py`: The main application file that logs in and handles token refresh.
- `modules/auth/auth_client.py`: Directory containing the authentication helper code.
  - `auth_client.py`: Contains the authentication client and helper methods for managing tokens.

## `AuthClient` Class

The `AuthClient` Class provides a client and helper for managing authentication tokens. Below are the key components:

### Auth Package Components

- `Client`: HTTP client for making authentication requests.
- `Helper`: Manages the state and validity of tokens.
- `Tokenstore`: storing token data.
- `LoginRequest`, `LoginResponse`, `RefreshTokenRequest`, `RefreshTokenResponse`, `RevokeTokenRequest`: API requests and handling responses.

### Helper Methods

- `AuthClient()`: Manages the low level token state.
- `Helper(auth_client)`: Managers access and refreshing of tokens, uses a 2nd thread to renew expiring refresh tokens (every 24 hours).
- `helper.get_access_token()`: Give you a valid access token.

## Example Usage in `auth.py`

```python3
import time
import logging
from auth_client import AuthClient
from helper import Helper

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
        while True:
            with helper.lock:
                try:
                    token = helper.get_access_token()
                    logger.info(f"Access token: {token}")

                    ### Do something with the token here :)

                except Exception as e:
                    logger.fatal(f"Failed to get token: {e}")
                    return

            time.sleep(3600)
    finally:
        helper.stop()

if __name__ == "__main__":
    main()

```
