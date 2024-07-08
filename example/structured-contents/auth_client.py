import os
import requests
from threading import Lock
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta

load_dotenv()


class AuthClient:
    def __init__(self):
        self.base_url = "https://auth.enterprise.wikimedia.com/v1"
        self.lock = Lock()
        self.username = os.getenv("WME_USERNAME")
        self.password = os.getenv("WME_PASSWORD")

    def _post(self, url, data):
        response = requests.post(f"{self.base_url}{url}", json=data)
        response.raise_for_status()
        return response.json()

    def login(self):
        data = {"username": self.username, "password": self.password}
        return self._post("/login", data)

    def revoke_token(self, refresh_token):
        data = {"refresh_token": refresh_token}
        self._post("/token-revoke", data)


class Helper:
    def __init__(self, auth_client):
        self.auth_client = auth_client
        self.lock = Lock()
        self.token_store_file = "tokenstore.json"

    def get_access_token(self):
        with self.lock:
            if not os.path.exists(self.token_store_file):
                return self._login_and_store_tokens()

            with open(self.token_store_file, 'r') as f:
                token_store = json.load(f)

            access_token_generated_at = datetime.fromisoformat(token_store["access_token_generated_at"])
            refresh_token_generated_at = datetime.fromisoformat(token_store["refresh_token_generated_at"])

            if datetime.now() - access_token_generated_at < timedelta(hours=24):
                return token_store["access_token"]

            if datetime.now() - refresh_token_generated_at < timedelta(days=30):
                return self._refresh_and_store_tokens(token_store["refresh_token"])

            return self._login_and_store_tokens()

    def _login_and_store_tokens(self):
        response = self.auth_client.login()
        token_store = {
            "access_token": response["access_token"],
            "access_token_generated_at": datetime.now().isoformat(),
            "refresh_token": response["refresh_token"],
            "refresh_token_generated_at": datetime.now().isoformat()
        }
        self._store_tokens(token_store)
        return response["access_token"]

    def _refresh_and_store_tokens(self, refresh_token):
        response = self.auth_client.refresh_token(refresh_token)
        token_store = {
            "access_token": response["access_token"],
            "access_token_generated_at": datetime.now().isoformat(),
            "refresh_token": refresh_token,
            "refresh_token_generated_at": datetime.now().isoformat()
        }
        self._store_tokens(token_store)
        return response["access_token"]

    def _store_tokens(self, token_store):
        with open(self.token_store_file, 'w') as f:
            json.dump(token_store, f)
