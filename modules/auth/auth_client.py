"""
Provides the AuthClient for handling authentication with the Wikimedia Enterprise API.

This module manages the full token lifecycle, including initial login,
token storage, automatic refresh, and revocation.
"""

import os
import json
from threading import Lock
from datetime import datetime, timedelta
from dotenv import load_dotenv
import httpx

# Load environment variables from .env file
load_dotenv()


class AuthClient:
    """Manages authentication and token lifecycle for the Wikimedia Enterprise API."""
    def __init__(self):
        """
        Initializes the AuthClient.

        Loads WME_USERNAME and WME_PASSWORD from environment variables
        and sets up the httpx client.

        Raises:
            ValueError: If WME_USERNAME or WME_PASSWORD are not set.
        """
        self.client = httpx.Client(base_url="https://auth.enterprise.wikimedia.com/v1")
        self.token_store_file = "tokenstore.json"
        self.lock = Lock()
        self.username = os.getenv("WME_USERNAME")
        self.password = os.getenv("WME_PASSWORD")
        if not self.username or not self.password:
            raise ValueError("Username or password not set in .env file")

    def __enter__(self):
        """Allows the class to be used in a 'with' statement."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensures the httpx client is closed when the 'with' block is exited."""
        self.close()

    def _post(self, url, data):
        """
        Internal helper for making POST requests.

        Args:
            url (str): The endpoint path to post to.
            data (dict): The JSON payload.

        Returns:
            dict: The JSON response dictionary, or an empty dict if no content.

        Raises:
            httpx.HTTPStatusError: If the API returns an error status.
        """
        response = self.client.post(url, json=data)
        response.raise_for_status()
        if len(response.text) > 0:
            return response.json()
        return {}

    def login(self):
        """Performs a primary login to the API using username and password."""
        data = {"username": self.username, "password": self.password}
        return self._post("/login", data)

    def refresh_token(self, refresh_token):
        """Obtains a new access token using a valid refresh token."""
        data = {"username": self.username, "refresh_token": refresh_token}
        return self._post("/token-refresh", data)

    def revoke_token(self, refresh_token):
        """Revokes a refresh token, invalidating the current session."""
        data = {"refresh_token": refresh_token}
        self._post("/token-revoke", data)

    def get_access_token(self):
        """
        Retrieves a valid access token, handling the full lifecycle.

        This is the primary method for consumers. It follows this logic:
        1.  Checks for a locally stored token (`tokenstore.json`).
        2.  If no token exists, performs a new login.
        3.  If a token exists, checks its access token expiry (24h).
        4.  If valid, returns the access token.
        5.  If access token is expired, checks refresh token expiry (30d).
        6.  If refresh token is valid, refreshes the access token.
        7.  If refresh token is expired, performs a new login.

        All file access is thread-safe.

        Returns:
            str: A valid access token.
        """
        with self.lock:
            if not os.path.exists(self.token_store_file):
                return self._login_and_store_tokens()

            with open(self.token_store_file, 'r', encoding="utf-8") as f:
                token_store = json.load(f)

            access_token_generated_at = datetime.fromisoformat(token_store["access_token_generated_at"])
            refresh_token_generated_at = datetime.fromisoformat(token_store["refresh_token_generated_at"])

            if datetime.now() - access_token_generated_at < timedelta(hours=24):
                return token_store["access_token"]

            if datetime.now() - refresh_token_generated_at < timedelta(days=30):
                return self._refresh_and_store_tokens(token_store["refresh_token"])

            return self._login_and_store_tokens()

    def _login_and_store_tokens(self):
        """
        Performs a new login, stores all tokens, and returns the access token.

        This is called when no valid tokens are available.

        Returns:
            str: The new access token.
        """
        response = self.login()
        token_store = {
            "access_token": response["access_token"],
            "access_token_generated_at": datetime.now().isoformat(),
            "refresh_token": response["refresh_token"],
            "refresh_token_generated_at": datetime.now().isoformat()
        }
        self._store_tokens(token_store)
        return response["access_token"]

    def _refresh_and_store_tokens(self, refresh_token):
        """
        Refreshes the access token, updates the stored tokens, and returns the new token.

        This is called when the access token is expired but the refresh token is still valid.

        Args:
            refresh_token (str): The valid refresh token to use.

        Returns:
            str: The new access token.
        """
        response = self.refresh_token(refresh_token)
        token_store = {
            "access_token": response["access_token"],
            "access_token_generated_at": datetime.now().isoformat(),
            "refresh_token": refresh_token,
            "refresh_token_generated_at": datetime.now().isoformat()
        }
        self._store_tokens(token_store)
        return response["access_token"]

    def _store_tokens(self, token_store):
        """
        Saves the token dictionary to the local file store.

        Args:
            token_store (dict): The dictionary containing token and timestamp info.
        """
        with open(self.token_store_file, 'w', encoding="utf-8") as f:
            json.dump(token_store, f)

    def clear_state(self):
        """Revokes active tokens and deletes the local token file."""
        with self.lock:
            if not os.path.exists(self.token_store_file):
                return

            with open(self.token_store_file, 'r', encoding="utf-8") as f:
                token_store = json.load(f)

            refresh_token = token_store.get("refresh_token")
            if refresh_token:
                self.revoke_token(refresh_token)

            os.remove(self.token_store_file)

    def close(self):
        """A dedicated method to close the client."""
        self.client.close()
