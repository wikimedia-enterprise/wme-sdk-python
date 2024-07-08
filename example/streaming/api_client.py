import requests


class ApiClient:
    def __init__(self):
        self.base_url = "https://api.example.com/v1"
        self.access_token = None

    def set_access_token(self, access_token):
        self.access_token = access_token

    def _get_headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    def get_articles(self, request, callback):
        url = f"{self.base_url}/articles"
        response = requests.post(url, json=request.to_dict(), headers=self._get_headers())
        response.raise_for_status()
        articles = response.json()

        for article in articles:
            callback(article)


class Request:
    def __init__(self, fields):
        self.fields = fields

    def to_dict(self):
        return {
            "fields": self.fields
        }


class Filter:
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def to_dict(self):
        return {
            "field": self.field,
            "value": self.value
        }
