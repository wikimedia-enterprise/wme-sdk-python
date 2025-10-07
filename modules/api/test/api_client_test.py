"""
Unit tests for the `api_client` module.

This file contains test suites for the Client, Request, and Filter classes,
ensuring their methods and initializers behave as expected. Mocks are used
to isolate the tests from actual network calls.
"""

import unittest
import httpx
from unittest.mock import MagicMock, patch, ANY
from datetime import datetime
from io import BytesIO
from typing import cast
from modules.api.api_client import Client, Request, Filter


class TestClient(unittest.TestCase):
    """Test suite for the Client class in the api_client module."""
    
    def setUp(self):
        """Set up a test client and mock the HTTP client before each test."""
        self.client = Client(access_token="test_access_token")
        self.client.http_client = MagicMock(spec=httpx.Client)

    def test_init(self):
        """Tests that the Client initializes with correct values."""
        client = Client()
        self.assertEqual(client.user_agent, "WME Python SDK")
        self.assertEqual(client.base_url, "https://api.enterprise.wikimedia.com/")
        self.assertIsInstance(client.http_client, httpx.Client)
        self.assertEqual(client.http_client.headers['User-Agent'], "WME Python SDK")
        self.assertEqual(client.http_client.timeout.read, 30.0)

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
        self.assertEqual(client.http_client.headers['Authorization'], "Bearer my_access_token")
        self.assertEqual(client.download_chunk_size, 2048)
        self.assertEqual(client.download_concurrency, 5)

    def test_request(self):
        """
        Verifies the internal `_request` method correctly calls the httpx client,
        invokes `raise_for_status`, and returns the response.
        """
        mock_http_client = cast(MagicMock, self.client.http_client)
        mock_response = MagicMock(spec=httpx.Response)
        mock_http_client.request.return_value = mock_response

        result = self.client._request("GET", "http://test.com/path", json={"data": 1})

        mock_http_client.request.assert_called_once_with(
            "GET", "http://test.com/path", json={"data": 1}
        )
        
        mock_response.raise_for_status.assert_called_once()
        
        self.assertEqual(result, mock_response)

    def test_get_entity(self):
        """
        Tests the `_get_entity` method's logic for fetching and updating data.
        It patches `_request` to isolate the method's own logic.
        """
        req = Request()
        path = "test_path"
        val = {}
        
        with patch.object(self.client, '_request', autospec=True) as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {"key": "value"}
            mock_request.return_value = mock_response

            self.client._get_entity(req, path, val)

            expected_url = f"{self.client.base_url}v2/{path}"
            mock_request.assert_called_once_with('POST', expected_url, json=req.to_json())
            
            self.assertEqual(val, {"key": "value"})

    def test_read_loop(self):
        """
        Tests the `_read_loop` helper for processing newline-delimited JSON
        from a byte stream and invoking a callback for each line.
        """
        data = b'{"article1": "content1"}\n{"article2": "content2"}'
        mock_rdr = BytesIO(data)
        mock_cbk = MagicMock()
        self.client._read_loop(mock_rdr, mock_cbk)
        mock_cbk.assert_any_call({"article1": "content1"})
        mock_cbk.assert_any_call({"article2": "content2"})

    def test_read_entity(self):
        """
        Tests that `_read_entity` correctly fetches content via `_request` and processes it.
        """
        mock_cbk = MagicMock()

        with patch.object(self.client, '_request', autospec=True) as mock_request:
            mock_response = MagicMock()
            mock_response.content = b'{"key": "value"}'
            mock_request.return_value = mock_response

            self.client._read_entity("test_path", mock_cbk)

            expected_url = f"{self.client.base_url}v2/test_path"
            mock_request.assert_called_once_with('GET', expected_url)
            mock_cbk.assert_called_once_with({"key": "value"})


class TestRequest(unittest.TestCase):
    """Test suite for the Request class."""
    def test_init(self):
        """Tests that the Request object initializes correctly, and that its `to_json` method works as expected."""
        req = Request()
        self.assertIsNone(req.since)
        self.assertEqual(req.fields, [])
        self.assertNotIn('filters', req.to_json())
        self.assertIsNone(req.limit)
        self.assertEqual(req.parts, [])
        self.assertEqual(req.offsets, {})
        self.assertEqual(req.since_per_partition, {})

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
    """Test suite for the Filter class."""
    def test_init(self):
        """Tests basic instantiation and attribute assignment of the Filter class."""
        field = "test_field"
        value = "test_value"
        filter_obj = Filter(field, value)
        self.assertEqual(filter_obj.field, field)
        self.assertEqual(filter_obj.value, value)


if __name__ == '__main__':
    unittest.main()