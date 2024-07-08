import pytest
from unittest.mock import MagicMock, patch
from helper import Helper  # Assuming the class is saved in helper.py
import time


@pytest.fixture
def mock_auth_client():
    auth_client = MagicMock()
    auth_client.get_access_token.return_value = "test_token"
    return auth_client


@pytest.fixture
def helper(mock_auth_client):
    helper = Helper(mock_auth_client, wait_seconds=1)  # Setting wait time to 1 second for faster tests
    yield helper
    helper.stop()


def test_get_access_token(helper, mock_auth_client):
    token = helper.get_access_token()
    assert token == "test_token"
    mock_auth_client.get_access_token.assert_called_once()


@patch('helper.logger')
def test_refresh_token_periodically(mock_logger, helper, mock_auth_client):
    # Mock the get_access_token method to do nothing
    mock_auth_client.get_access_token.return_value = None

    # Wait for 2 seconds to allow multiple refresh attempts
    time.sleep(2)

    if helper.refresh_thread.is_alive():
        helper.stop_event.set()

    mock_logger.info.assert_called_with("Token refreshed successfully")


@patch('helper.logger')
def test_refresh_token_periodically_with_exception(mock_logger, helper, mock_auth_client):
    # Mock the get_access_token method to raise an exception
    mock_auth_client.get_access_token.side_effect = Exception("Test exception")

    # Wait for 2 seconds to allow multiple refresh attempts
    time.sleep(2)

    if helper.refresh_thread.is_alive():
        helper.stop_event.set()

    mock_logger.error.assert_called_with("Failed to refresh token: Test exception")


def test_stop(helper, mock_auth_client):
    helper.stop()
    assert not helper.refresh_thread.is_alive()
    mock_auth_client.revoke_token.assert_called_once()


def test_refresh_thread_running(helper):
    assert helper.refresh_thread.is_alive()
