"""This test suite focuses on testing AuthClient and all its capabilities"""

import os
import json
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime, timedelta
import pytest
import httpx
from modules.auth.auth_client import AuthClient


@pytest.fixture(name="auth_client")
def auth_client_fixture():
    """
    Fixture to set up and tear down the AuthClient instance for each test.
    The injectable name is 'auth_client', but the function name is unique.
    """
    with patch.dict(os.environ, {"WME_USERNAME": "test_user", "WME_PASSWORD": "test_pass"}):
        client = AuthClient()
        yield client
        client.close()


def test_init(auth_client):
    """Test that the client initializes correctly with environment variables."""
    assert auth_client.username == "test_user"
    assert auth_client.password == "test_pass"
    assert str(auth_client.client.base_url) == "https://auth.enterprise.wikimedia.com/v1/"


def test_login(auth_client):
    """Test the login method by mocking the httpx client's post method."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.text = '{"access_token": "access_token_value", "refresh_token": "refresh_token_value"}'
    mock_response.json.return_value = {
        "access_token": "access_token_value",
        "refresh_token": "refresh_token_value"
    }
    with patch.object(auth_client.client, 'post', return_value=mock_response) as mock_post:
        response = auth_client.login()
        mock_post.assert_called_once_with("/login", json={"username": "test_user", "password": "test_pass"})
        assert response["access_token"] == "access_token_value"
        assert response["refresh_token"] == "refresh_token_value"


def test_refresh_token(auth_client):
    """Test the refresh_token method."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.text = '{"access_token": "new_access_token"}'
    mock_response.json.return_value = {"access_token": "new_access_token"}
    with patch.object(auth_client.client, 'post', return_value=mock_response) as mock_post:
        response = auth_client.refresh_token("refresh_token_value")
        mock_post.assert_called_once_with(
            "/token-refresh",
            json={"username": "test_user", "refresh_token": "refresh_token_value"}
        )
        assert response["access_token"] == "new_access_token"


def test_revoke_token(auth_client):
    """Test the revoke_token method."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.text = ""
    with patch.object(auth_client.client, 'post', return_value=mock_response) as mock_post:
        auth_client.revoke_token("refresh_token_value")
        mock_post.assert_called_once_with(
            "/token-revoke",
            json={"refresh_token": "refresh_token_value"}
        )
        mock_response.raise_for_status.assert_called_once()


@patch('os.path.exists', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
    "access_token": "stored_access_token",
    "access_token_generated_at": (datetime.now() - timedelta(hours=1)).isoformat(),
    "refresh_token": "stored_refresh_token",
    "refresh_token_generated_at": (datetime.now() - timedelta(days=1)).isoformat()
}))
def test_get_access_token_valid(_mock_open, _mock_exists, auth_client):
    """Test getting a valid, non-expired access token from the store."""
    token = auth_client.get_access_token()
    assert token == "stored_access_token"


@patch('os.path.exists', return_value=True)
@patch('modules.auth.auth_client.AuthClient._refresh_and_store_tokens', return_value="new_access_token")
@patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
    "access_token": "expired_access_token",
    "access_token_generated_at": (datetime.now() - timedelta(days=2)).isoformat(),
    "refresh_token": "stored_refresh_token",
    "refresh_token_generated_at": (datetime.now() - timedelta(days=1)).isoformat()
}))
def test_get_access_token_needs_refresh(_mock_open, mock_refresh, _mock_exists, auth_client):
    """Test that an expired access token triggers a refresh."""
    token = auth_client.get_access_token()
    mock_refresh.assert_called_with("stored_refresh_token")
    assert token == "new_access_token"


@patch('os.path.exists', return_value=False)
@patch('modules.auth.auth_client.AuthClient._login_and_store_tokens', return_value="new_access_token")
def test_get_access_token_needs_login(mock_login, _mock_exists, auth_client):
    """Test that a missing token file triggers a new login."""
    token = auth_client.get_access_token()
    mock_login.assert_called_once()
    assert token == "new_access_token"


@patch('os.path.exists', return_value=True)
@patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
    "refresh_token": "stored_refresh_token",
}))
@patch('os.remove')
def test_clear_state(_mock_remove, _mock_open_file, _mock_exists, auth_client):
    """Test clearing the local token store and revoking the token."""
    with patch.object(auth_client, 'revoke_token') as mock_revoke:
        auth_client.clear_state()
        mock_revoke.assert_called_with("stored_refresh_token")
    _mock_remove.assert_called_with("tokenstore.json")
