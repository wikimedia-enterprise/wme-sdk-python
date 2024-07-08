import os
import json
import pytest

from unittest.mock import patch, mock_open
from datetime import datetime, timedelta
from auth_client import AuthClient  # Adjust this import to match your project structure


@pytest.fixture
def auth_client():
    with patch.dict(os.environ, {"WME_USERNAME": "test_user", "WME_PASSWORD": "test_pass"}):
        return AuthClient()


def test_init(auth_client):
    assert auth_client.username == "test_user"
    assert auth_client.password == "test_pass"
    assert auth_client.base_url == "https://auth.enterprise.wikimedia.com/v1"


@patch('requests.post')
def test_login(mock_post, auth_client):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "access_token": "access_token_value",
        "refresh_token": "refresh_token_value"
    }
    response = auth_client.login()
    assert response["access_token"] == "access_token_value"
    assert response["refresh_token"] == "refresh_token_value"


@patch('requests.post')
def test_refresh_token(mock_post, auth_client):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "access_token": "new_access_token"
    }
    response = auth_client.refresh_token("refresh_token_value")
    assert response["access_token"] == "new_access_token"


@patch('requests.post')
def test_revoke_token(mock_post, auth_client):
    mock_post.return_value.status_code = 200
    auth_client.revoke_token("refresh_token_value")
    mock_post.assert_called_with(
        "https://auth.enterprise.wikimedia.com/v1/token-revoke",
        json={"refresh_token": "refresh_token_value"}
    )


@patch('os.path.exists')
@patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
    "access_token": "stored_access_token",
    "access_token_generated_at": (datetime.now() - timedelta(hours=1)).isoformat(),
    "refresh_token": "stored_refresh_token",
    "refresh_token_generated_at": (datetime.now() - timedelta(days=1)).isoformat()
}))
def test_get_access_token_valid(mock_open, mock_exists, auth_client):
    mock_exists.return_value = True
    token = auth_client.get_access_token()
    assert token == "stored_access_token"


@patch('os.path.exists')
@patch('auth_client.AuthClient._refresh_and_store_tokens')
@patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
    "access_token": "stored_access_token",
    "access_token_generated_at": (datetime.now() - timedelta(days=2)).isoformat(),
    "refresh_token": "stored_refresh_token",
    "refresh_token_generated_at": (datetime.now() - timedelta(days=1)).isoformat()
}))
def test_get_access_token_refresh(mock_open, mock_refresh, mock_exists, auth_client):
    mock_exists.return_value = True
    mock_refresh.return_value = "new_access_token"
    token = auth_client.get_access_token()
    mock_refresh.assert_called_with("stored_refresh_token")
    assert token == "new_access_token"


@patch('os.path.exists')
@patch('auth_client.AuthClient._login_and_store_tokens')
def test_get_access_token_login(mock_login, mock_exists, auth_client):
    mock_exists.return_value = False
    mock_login.return_value = "new_access_token"
    token = auth_client.get_access_token()
    mock_login.assert_called_once()
    assert token == "new_access_token"


@patch('os.path.exists')
@patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
    "access_token": "stored_access_token",
    "access_token_generated_at": datetime.now().isoformat(),
    "refresh_token": "stored_refresh_token",
    "refresh_token_generated_at": datetime.now().isoformat()
}))
@patch('os.remove')
def test_clear_state(mock_remove, mock_open, mock_exists, auth_client):
    mock_exists.return_value = True
    with patch.object(auth_client, 'revoke_token') as mock_revoke:
        auth_client.clear_state()
        mock_revoke.assert_called_with("stored_refresh_token")
    mock_remove.assert_called_with("tokenstore.json")
