"""
Unit tests for the `api_client` module.

This file contains test suites for the Client, Request, and Filter classes,
ensuring their methods and initializers behave as expected. Mocks are used
to isolate the tests from actual network calls.
"""

import unittest
import httpx
from unittest.mock import MagicMock, patch
from datetime import datetime
from io import BytesIO
from typing import cast
from modules.api.api_client import Client, Request, Filter
from modules.api.exceptions import APIStatusError, APIDataError

CLIENT_LOGGER_NAME = 'modules.api.api_client'


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
        mock_response.status_code = 200
        mock_http_client.request.return_value = mock_response
        
        with self.assertLogs(CLIENT_LOGGER_NAME, level='DEBUG') as cm:
            result = self.client._request("GET", "http://test.com/path", json={"data": 1})
            self.assertIn("Request successful: GET http://test.com/path -> 200", cm.output[0])

        mock_http_client.request.assert_called_once_with(
            "GET", "http://test.com/path", json={"data": 1}
        )
    
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(result, mock_response)
        
    def test_request_raises_for_status_on_error(self):
        """Tests that _request propagates HTTP errors from raise_for_status."""
        mock_http_client = cast(MagicMock, self.client.http_client)
        mock_request = MagicMock()
        mock_request.url = "http://test.com/path"
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 404
        mock_response.reason_phrase = "Not Found"
        
        http_error = httpx.HTTPStatusError(
            "Not Found", request=mock_request, response=mock_response
        )
        mock_response.raise_for_status.side_effect = http_error
        mock_http_client.request.return_value = mock_response
        
        with self.assertLogs(CLIENT_LOGGER_NAME, level='ERROR') as cm:
            with self.assertRaises(APIStatusError):
                self.client._request("GET", "http://test.com/path")
                
            self.assertIn("HTTP Status Error: 404 for url http://test.com/path", cm.output[0])

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
        
    def test_read_loop_logs_warning_on_malformed_json_and_continues(self):
        """
        Tests that `_read_loop` logs a warning for malformed JSON but continues
        to process subsequent valid lines.
        """
        data = b'{"article1": "content1"}\n{"invalid" json}\n{"article2": "content2"}'
        mock_rdr = BytesIO(data)
        mock_cbk = MagicMock()
        
        with self.assertLogs(CLIENT_LOGGER_NAME, level='WARNING') as cm:
            self.client._read_loop(mock_rdr, mock_cbk)
            self.assertIn("Skipping line due to JSON decode error", cm.output[0])

        mock_cbk.assert_any_call({"article1": "content1"})
        mock_cbk.assert_any_call({"article2": "content2"})
        self.assertEqual(mock_cbk.call_count, 2)

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
            
    @patch('modules.api.api_client.time.sleep')
    @patch('modules.api.api_client.time.monotonic')
    def test_rate_limit_waits_correctly(self, mock_monotonic, mock_sleep):
        """Tests that rate_limit_wait enforces the delay between calls"""
        self.client.rate_limit_period = 0.5
        self.client.last_request_time = 0
        
        mock_monotonic.side_effect = [100.0, 100.0, 100.2, 100.2]
        
        mock_request_method = cast(MagicMock, self.client.http_client.request)
        mock_request_method.side_effect = [MagicMock(), MagicMock()]
        
        self.client._request("GET", "url1")
        mock_sleep.assert_not_called()
        
        self.client._request("GET", "url12")
        
        mock_sleep.assert_called_once()
        self.assertAlmostEqual(mock_sleep.call_args[0][0], 0.3)
        
    def test_download_entity_calculates_chunks_correctly(self):
        """
        Tests that _download_entity creates the correct Range requests
        based on the Content-Length and chunk size.
        """
        with patch.object(self.client, '_head_entity') as mock_head, \
            patch.object(self.client, '_request') as mock_request:

            self.client.download_chunk_size = 1000
            mock_head.return_value = {'Content-Length': 2500}
        
            mock_response = MagicMock(spec=httpx.Response)
            mock_response.content = b''
            mock_request.return_value = mock_response
        
            mock_writer = BytesIO()

            self.client._download_entity("some/path", mock_writer)

            mock_head.assert_called_once_with("some/path")

            self.assertEqual(mock_request.call_count, 3)
        
        actual_ranges = {call.kwargs['headers']['Range'] for call in mock_request.call_args_list}
        expected_ranges = {'bytes=0-999', 'bytes=1000-1999', 'bytes=2000-2499'}
        self.assertSetEqual(actual_ranges, expected_ranges)

    def test_head_entity_raises_on_invalid_content_length(self):
        """
        Tests that _head_entity raises APIDataError for a non-integer Content-Length.
        """
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.headers = {'Content-Length': 'invalid-size'}
    
        with patch.object(self.client, '_request', return_value=mock_response):
            with self.assertRaisesRegex(APIDataError, "Invalid 'Content-Length' header"):
                self.client._head_entity("some/path")
                
    def test_get_entity_raises_on_type_mismatch(self):
        """
        Tests _get_entity raises APIDataError if the API returns a list
        but a dict was expected.
        """
        with patch.object(self.client, '_request') as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = [{"key": "value"}]
            mock_request.return_value = mock_response
            
            val = {}
            with self.assertRaisesRegex(APIDataError, "Mismatched types"):
                self.client._get_entity(Request(), "path", val)


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
        
    def test_init_with_dict_filters(self):
        """Tests that Request correctly converts a dictionary of filters."""
        filters_dict = {'project': 'enwiki', 'namespace': '0'}
        req = Request(filters=filters_dict)
    
        expected_json = [
            {'field': 'project', 'value': 'enwiki'},
            {'field': 'namespace', 'value': '0'}
        ]
        
        self.assertCountEqual(req.to_json()['filters'], expected_json)


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