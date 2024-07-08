import time
import logging
import threading

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
