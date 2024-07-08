import logging
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Helper:
    def __init__(self, auth_client, wait_seconds=None):
        self.auth_client = auth_client
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        # default is 23 hours and 59 minutes
        self.wait_seconds = wait_seconds if wait_seconds is not None else 23 * 3600 + 59 * 60
        self.refresh_thread = threading.Thread(target=self._refresh_token_periodically)
        self.refresh_thread.start()

    def get_access_token(self):
        with self.lock:
            return self.auth_client.get_access_token()

    def _refresh_token_periodically(self):
        while not self.stop_event.is_set():
            if self.stop_event.wait(self.wait_seconds):
                continue
            try:
                self.get_access_token()
                logger.info("Token refreshed successfully")
            except Exception as e:
                logger.error(f"Failed to refresh token: {e}")

    def stop(self):
        self.stop_event.set()
        self.refresh_thread.join()
        self.auth_client.revoke_token()
