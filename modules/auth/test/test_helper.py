"""This test suite focuses on testing the auth helper"""

import threading
from unittest.mock import MagicMock, patch
import pytest
from modules.auth.helper import Helper

@pytest.fixture(name="mock_auth_client")
def mock_auth_client_fixture():
    """Provides a MagicMock substitute for the AuthClient."""
    auth_client = MagicMock()
    auth_client.get_access_token.return_value = "test_token"
    return auth_client


@pytest.fixture(name="helper")
def helper_fixture(mock_auth_client):
    """
    Sets up the Helper instance with a mock client and a short wait time for faster testing,
    and handles cleanup.
    """
    helper = Helper(mock_auth_client, wait_seconds=0.1)
    yield helper
    if helper.refresh_thread and helper.refresh_thread.is_alive():
        helper.stop()


def test_get_access_token(helper, mock_auth_client):
    """Tests that the helper correctly calls the client's get_access_token method."""
    token = helper.get_access_token()
    assert token == "test_token"
    mock_auth_client.get_access_token.assert_called_once()


@patch('modules.auth.helper.logger')
def test_refresh_token_periodically(mock_logger, helper, mock_auth_client):
    """
    Tests that the background refresh thread calls for a new token,
    using threading.Event for reliable synchronization.
    """
     # pylint: disable=unused-argument
    refresh_call_completed = threading.Event()

    def token_side_effect():
        if mock_auth_client.get_access_token.call_count >= 2:
            refresh_call_completed.set()
        return "refreshed_token"

    mock_auth_client.get_access_token.side_effect = token_side_effect

    was_set = refresh_call_completed.wait(timeout=2)

    assert was_set, "The refresh thread did not call get_access_token twice within the timeout."

    assert mock_auth_client.get_access_token.call_count >= 2
    mock_logger.info.assert_called_with("Token refreshed successfully")


@patch('modules.auth.helper.logger')
def test_refresh_token_periodically_with_exception(mock_logger, helper, mock_auth_client):
    """
    Tests error logging on token refresh failure, using threading.Event
    for reliable synchronization.
    """
     # pylint: disable=unused-argument
    test_exception = ValueError("Test exception")
    mock_auth_client.get_access_token.side_effect = test_exception

    error_was_logged = threading.Event()

    def log_error_side_effect(*_args, **_kwargs):
        error_was_logged.set()

    mock_logger.error.side_effect = log_error_side_effect

    was_set = error_was_logged.wait(timeout=2)

    assert was_set, "The logger.error method was not called within the timeout."
    mock_logger.error.assert_called_with("Failed to refresh token: %s", test_exception)


def test_stop(helper, mock_auth_client):
    """Tests that the stop method correctly stops the thread and cleans up."""
    assert helper.refresh_thread.is_alive()
    helper.stop()
    helper.refresh_thread.join(timeout=1)
    assert not helper.refresh_thread.is_alive()
    mock_auth_client.clear_state.assert_called_once()


def test_refresh_thread_running(helper):
    """Confirms that the refresh thread is alive after initialization."""
    assert helper.refresh_thread.is_alive()
