import unittest
import requests
from unittest.mock import MagicMock, patch
from datetime import datetime
from io import BytesIO
from typing import cast
from modules.api.api_client import Client, Request, Filter


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.access_token = "test_access_token"
        self.client.http_client = MagicMock(spec=requests.Session)

    def test_init(self):
        # Test default values
        client = Client()
        self.assertEqual(client.user_agent, "WME Python SDK")
        self.assertEqual(client.base_url, "https://api.enterprise.wikimedia.com/")
        self.assertEqual(client.realtime_url, "https://realtime.enterprise.wikimedia.com/")
        self.assertEqual(client.access_token, "")
        self.assertEqual(client.download_chunk_size, -1)
        self.assertEqual(client.download_concurrency, 10)
        self.assertEqual(client.scanner_buffer_size, 20971520)

        # Test custom values
        client = Client(
            user_agent="My User Agent",
            base_url="https://example.com",
            realtime_url="https://realtime.example.com",
            access_token="my_access_token",
            download_chunk_size=2048,
            download_concurrency=5,
            scanner_buffer_size=10000,
        )
        self.assertEqual(client.user_agent, "My User Agent")
        self.assertEqual(client.base_url, "https://example.com")
        self.assertEqual(client.realtime_url, "https://realtime.example.com")
        self.assertEqual(client.access_token, "my_access_token")
        self.assertEqual(client.download_chunk_size, 2048)
        self.assertEqual(client.download_concurrency, 5)
        self.assertEqual(client.scanner_buffer_size, 10000)

    def test_new_request(self):
        req = Request(since=datetime(2024, 1, 1))
        url = "https://api.example.com"
        method = "POST"
        path = "test_path"

        expected_data = '{"since": "2024-01-01T00:00:00"}'
        expected_headers = {
            'User-Agent': 'WME Python SDK',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test_access_token',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }

        request = self.client._new_request(url, method, path, req)

        self.assertEqual(request.url, f"{url}v2/{path}")
        self.assertEqual(request.method, method)
        self.assertEqual(request.data, expected_data)
        self.assertEqual(request.headers, expected_headers)

    def test_do(self):
        mock_http_client = cast(MagicMock, self.client.http_client)
        original_request = MagicMock(name="OriginalRequest")
        prepared_request = MagicMock(name="PreparedRequest")
        mock_response = MagicMock(name="MockResponse")
        
        mock_http_client.prepare_request.return_value = prepared_request
        mock_http_client.send.return_value = mock_response

        result = self.client._do(original_request)

        self.assertEqual(result, mock_response)
        mock_http_client.prepare_request.assert_called_once_with(original_request)
        mock_http_client.send.assert_called_once_with(
            prepared_request,
            timeout=self.client.timeout
        )

    def test_get_entity(self):
        mock_http_client = cast(MagicMock, self.client.http_client)
        req = Request()
        path = "test_path"
        val = {}

        response = MagicMock()
        response.json.return_value = {"key": "value"}
        mock_http_client.send.return_value = response

        self.client._get_entity(req, path, val)

        self.assertEqual(val, {"key": "value"})
        mock_http_client.send.assert_called_once()

    def test_read_loop(self):
        # Create a mock BytesIO object with sample data
        data = b'{"article1": "content1"}\n{"article2": "content2"}'
        mock_rdr = BytesIO(data)

        # Create a mock callback function
        mock_cbk = MagicMock()

        # Call the _read_loop method
        self.client._read_loop(mock_rdr, mock_cbk)

        # Assertions
        mock_cbk.assert_any_call({"article1": "content1"})
        mock_cbk.assert_any_call({"article2": "content2"})

    def test_read_entity(self):
        # Create a mock callback function
        mock_cbk = MagicMock()

        # Patch the _do method to return a mock response with byte content
        with patch.object(self.client, '_do', autospec=True) as mock_do:
            mock_response = MagicMock()
            mock_response.content = b'{"key": "value"}'
            mock_do.return_value = mock_response

            # Call the _read_entity method
            self.client._read_entity("test_path", mock_cbk)

            # Assertions
            mock_cbk.assert_any_call({"key": "value"})


class TestRequest(unittest.TestCase):
    def test_init(self):
        # Test default values
        req = Request()
        self.assertIsNone(req.since)
        self.assertEqual(req.fields, [])
        self.assertNotIn('filters', req.to_json())
        self.assertIsNone(req.limit)
        self.assertEqual(req.parts, [])
        self.assertEqual(req.offsets, {})
        self.assertEqual(req.since_per_partition, {})

        # Test custom values
        since = datetime(2024, 1, 1)
        fields = ["field1", "field2"]
        filters = [Filter("field", "value")]
        limit = 10
        parts = [1, 2, 3]
        offsets = {1: 10, 2: 20}
        since_per_partition = {1: datetime(2024, 1, 1), 2: datetime(2024, 1, 2)}
        req = Request(since, 
                      fields, 
                      filters=filters, 
                      limit=limit, 
                      parts=parts, 
                      offsets=offsets, 
                      since_per_partition=since_per_partition)
        self.assertEqual(req.since, since)
        self.assertEqual(req.fields, fields)
        expected_filters_json = [{"field": "field", "value": "value"}]
        self.assertEqual(req.to_json().get('filters'), expected_filters_json)
        self.assertEqual(req.limit, limit)
        self.assertEqual(req.parts, parts)
        self.assertEqual(req.offsets, offsets)
        self.assertEqual(req.since_per_partition, since_per_partition)


class TestFilter(unittest.TestCase):
    def test_init(self):
        field = "test_field"
        value = "test_value"
        filter = Filter(field, value)
        self.assertEqual(filter.field, field)
        self.assertEqual(filter.value, value)


if __name__ == '__main__':
    unittest.main()
