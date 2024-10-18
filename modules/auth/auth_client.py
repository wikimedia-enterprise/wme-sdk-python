import os
import json
import requests
from dotenv import load_dotenv
from threading import Lock
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()


class AuthClient:
    def __init__(self):
        self.base_url = "https://auth.enterprise.wikimedia.com/v1"
        self.token_store_file = "tokenstore.json"
        self.lock = Lock()
        self.username = os.getenv("WME_USERNAME")
        self.password = os.getenv("WME_PASSWORD")
        if not self.username or not self.password:
            raise ValueError("Username or password not set in .env file")

    def _post(self, url, data):
        response = requests.post(f"{self.base_url}{url}", json=data)
        response.raise_for_status()
        if len(response.text) > 0:
            return response.json()
        return {}

    def login(self):
        data = {"username": self.username, "password": self.password}
        return self._post("/login", data)

    def refresh_token(self, refresh_token):
        data = {"username": self.username, "refresh_token": refresh_token}
        return self._post("/token-refresh", data)

    def revoke_token(self, refresh_token):
        data = {"refresh_token": refresh_token}
        self._post("/token-revoke", data)

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
        with open(self.token_store_file, 'w') as f:
            json.dump(token_store, f)

    def clear_state(self):
        with self.lock:
            if not os.path.exists(self.token_store_file):
                return

            with open(self.token_store_file, 'r') as f:
                token_store = json.load(f)

            refresh_token = token_store.get("refresh_token")
            if refresh_token:
                self.revoke_token(refresh_token)

            os.remove(self.token_store_file)
