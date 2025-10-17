"""This test suite focuses on testing the auth helper"""

import time
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
    Sets up the Helper instance with a mock client and handles cleanup.
    The injectable name is 'helper', but the function name is unique.
    """
    helper = Helper(mock_auth_client, wait_seconds=1)
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
    """Tests that the background refresh thread calls for a new token."""
    time.sleep(2)
    helper.stop()
    assert mock_auth_client.get_access_token.call_count >= 2
    mock_logger.info.assert_called_with("Token refreshed successfully")


@patch('modules.auth.helper.logger')
def test_refresh_token_periodically_with_exception(mock_logger, helper, mock_auth_client):
    """Tests the error logging when the token refresh fails."""
    test_exception = Exception("Test exception")

    mock_auth_client.get_access_token.side_effect = test_exception

    time.sleep(2)

    helper.stop()

    mock_logger.error.assert_called_with("Failed to refresh token: %s", test_exception)


def test_stop(helper, mock_auth_client):
    """Tests that the stop method correctly stops the thread and cleans up."""
    assert helper.refresh_thread.is_alive()
    helper.stop()
    assert not helper.refresh_thread.is_alive()
    mock_auth_client.clear_state.assert_called_once()


def test_refresh_thread_running(helper):
    """Confirms that the refresh thread is alive after initialization."""
    assert helper.refresh_thread.is_alive()
