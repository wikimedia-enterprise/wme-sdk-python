import requests


class ApiClient:
    def __init__(self):
        self.base_url = "https://api.example.com/v1"
        self.access_token = None

    def set_access_token(self, access_token):
        self.access_token = access_token

    def _get_headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    def get_structured_contents(self, query, request):
        url = f"{self.base_url}/structured_contents/{query}"
        response = requests.post(url, json=request.to_dict(), headers=self._get_headers())
        response.raise_for_status()
        return response.json()


class Request:
    def __init__(self, fields, filters):
        self.fields = fields
        self.filters = filters

    def to_dict(self):
        return {
            "fields": self.fields,
            "filters": [f.to_dict() for f in self.filters]
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
