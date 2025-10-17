"""Provides a helper class for automatic, background refreshing of auth tokens."""

import logging
import threading
import json
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Helper:
    """Manages an authentication client with automatic token refreshing."""
    def __init__(self, auth_client, wait_seconds=None):
        self.auth_client = auth_client
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        # default is 23 hours and 59 minutes
        self.wait_seconds = wait_seconds if wait_seconds is not None else 23 * 3600 + 59 * 60
        self.refresh_thread = threading.Thread(target=self._refresh_token_periodically)
        self.refresh_thread.start()

    def get_access_token(self):
        """Retrieves the current access token in a thread-safe manner."""
        with self.lock:
            return self.auth_client.get_access_token()

    def _refresh_token_periodically(self):
        """The target function for the background refresh thread."""
        while not self.stop_event.is_set():
            if self.stop_event.wait(self.wait_seconds):
                break
            try:
                self.get_access_token()
                logger.info("Token refreshed successfully")
            except (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError, ValueError) as e:
                logger.error("Failed to refresh token: %s", e)

    def stop(self):
        """Gracefully stops the background refresh thread and cleans up."""
        self.stop_event.set()
        self.refresh_thread.join()
        self.auth_client.revoke_token()
