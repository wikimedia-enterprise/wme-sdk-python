import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from io import BytesIO

from api_client import Client, Request, Filter


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.http_client = MagicMock()
        self.client.access_token = "test_access_token"

    def test_init(self):
        # Test default values
        client = Client()
        self.assertEqual(client.user_agent, "")
        self.assertEqual(client.base_url, "https://api.enterprise.wikimedia.com/")
        self.assertEqual(client.realtime_url, "https://realtime.enterprise.wikimedia.com/")
        self.assertEqual(client.access_token, "")
        self.assertEqual(client.download_min_chunk_size, 5242880)
        self.assertEqual(client.download_chunk_size, 5242880 * 5)
        self.assertEqual(client.download_concurrency, 10)
        self.assertEqual(client.scanner_buffer_size, 20971520)

        # Test custom values
        client = Client(
            user_agent="My User Agent",
            base_url="https://example.com",
            realtime_url="https://realtime.example.com",
            access_token="my_access_token",
            download_min_chunk_size=1024,
            download_chunk_size=2048,
            download_concurrency=5,
            scanner_buffer_size=10000,
        )
        self.assertEqual(client.user_agent, "My User Agent")
        self.assertEqual(client.base_url, "https://example.com")
        self.assertEqual(client.realtime_url, "https://realtime.example.com")
        self.assertEqual(client.access_token, "my_access_token")
        self.assertEqual(client.download_min_chunk_size, 1024)
        self.assertEqual(client.download_chunk_size, 2048)
        self.assertEqual(client.download_concurrency, 5)
        self.assertEqual(client.scanner_buffer_size, 10000)

    def test_new_request(self):
        req = Request(since=datetime(2024, 1, 1))
        url = "https://api.example.com"
        method = "POST"
        path = "test_path"

        expected_data = '{"since": "2024-01-01T00:00:00", "fields": [], "filters": [], "limit": null, "parts": [], "offsets": {}, "since_per_partition": {}}'
        expected_headers = {
            'User-Agent': '',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test_access_token'
        }

        request = self.client._new_request(url, method, path, req)

        self.assertEqual(request.url, f"{url}v2/{path}")
        self.assertEqual(request.method, method)
        self.assertEqual(request.data, expected_data)
        self.assertEqual(request.headers, expected_headers)

    def test_do(self):
        request = MagicMock()
        response = MagicMock()
        self.client.http_client.prepare_request.return_value = request
        self.client.http_client.send.return_value = response

        result = self.client._do(request)

        self.assertEqual(result, response)
        self.client.http_client.prepare_request.assert_called_once_with(request)
        self.client.http_client.send.assert_called_once_with(request)

    def test_get_entity(self):
        req = Request()
        path = "test_path"
        val = {}

        response = MagicMock()
        response.json.return_value = {"key": "value"}
        self.client.http_client.send.return_value = response

        self.client._get_entity(req, path, val)

        self.assertEqual(val, {"key": "value"})
        self.client.http_client.send.assert_called_once()

    # Add more tests for other methods in the Client class

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

        # Patch the _read_loop method to mock its behavior
        with patch.object(self.client, '_read_loop', autospec=True) as mock_read_loop:
            self.client._read_entity("test_path", mock_cbk)

            # Assertions
            mock_read_loop.assert_called_once()
            self.assertEqual(mock_read_loop.call_args[0][0], self.client.base_url + "v2/test_path")
            self.assertEqual(mock_read_loop.call_args[0][1], mock_cbk)

    # Add similar tests for other methods

class TestRequest(unittest.TestCase):
    def test_init(self):
        # Test default values
        req = Request()
        self.assertIsNone(req.since)
        self.assertEqual(req.fields, [])
        self.assertEqual(req.filters, [])
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
        req = Request(since, fields, filters, limit, parts, offsets, since_per_partition)
        self.assertEqual(req.since, since)
        self.assertEqual(req.fields, fields)
        self.assertEqual(req.filters, filters)
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
