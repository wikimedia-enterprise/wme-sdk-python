# pylint: disable=W0212, too-many-locals, too-many-public-methods, C0302

"""
Unit tests for the api_client module.

This file contains test suites for the Client, Request, and Filter classes,
ensuring their methods and initializers behave as expected. Mocks are used
to isolate the tests from actual network calls.
"""

import unittest
import json
import tarfile
from unittest.mock import MagicMock, patch, call
from datetime import datetime
from io import BytesIO
from typing import cast
import httpx

# --- Import all SDK components under test ---
from modules.api.api_client import Client, Request, Filter, _TarfileStreamWrapper
from modules.api.exceptions import APIStatusError, APIDataError, APIRequestError, DataModelError
from modules.api.code import Code
from modules.api.language import Language
from modules.api.project import Project
from modules.api.namespace import Namespace
from modules.api.batch import Batch
from modules.api.snapshot import Snapshot
from modules.api.article import Article
from modules.api.structuredcontent import StructuredContent

CLIENT_LOGGER_NAME = 'modules.api.api_client'


class TestClient(unittest.TestCase):
    """Test suite for the Client class in the api_client module."""

    def setUp(self):
        """Set up a test client and mock the HTTP client before each test."""
        self.client = Client()
        self.client.http_client = MagicMock(spec=httpx.Client)

    @patch('modules.api.api_client.httpx.Client')
    @patch('modules.api.api_client.httpx.HTTPTransport')
    def test_init_defaults_and_overrides(self, mock_transport, mock_client):
        """Tests that the Client initializes correctly, passing correct args to httpx."""

        mock_transport.reset_mock()
        mock_client.reset_mock()

        default_client = Client()

        self.assertEqual(default_client.user_agent, "WME Python SDK")
        self.assertEqual(default_client.base_url, "https://api.enterprise.wikimedia.com/")
        self.assertEqual(default_client.access_token, "")

        mock_transport.assert_called_once_with(retries=3)

        mock_client.assert_called_once()
        client_call_args = mock_client.call_args[1]

        self.assertEqual(client_call_args['headers']['User-Agent'], "WME Python SDK")
        self.assertEqual(client_call_args['headers']['Authorization'], "Bearer ")
        self.assertEqual(client_call_args['timeout'], 30.0)
        self.assertEqual(client_call_args['transport'], mock_transport.return_value)
        self.assertTrue(client_call_args['http2'])
        self.assertTrue(client_call_args['follow_redirects'])

        mock_transport.reset_mock()
        mock_client.reset_mock()

        custom_client = Client(
            user_agent="Integration Test",
            base_url="https://example.com",
            realtime_url="https://realtime.example.com",
            max_retries=5,
            timeout=10.0,
            access_token="my_access_token",
            download_chunk_size=2048,
            download_concurrency=5,
            scanner_buffer_size=10000,
        )

        self.assertEqual(custom_client.user_agent, "Integration Test")
        self.assertEqual(custom_client.base_url, "https://example.com")
        self.assertEqual(custom_client.realtime_url, "https://realtime.example.com")
        self.assertEqual(custom_client.access_token, "my_access_token")
        self.assertEqual(custom_client.download_chunk_size, 2048)
        self.assertEqual(custom_client.download_concurrency, 5)
        self.assertEqual(custom_client.scanner_buffer_size, 10000)

        mock_transport.assert_called_once_with(retries=5)

        mock_client.assert_called_once()
        custom_call_args = mock_client.call_args[1]

        self.assertEqual(custom_call_args['headers']['User-Agent'], "Integration Test")
        self.assertEqual(custom_call_args['headers']['Authorization'], "Bearer my_access_token")
        self.assertEqual(custom_call_args['timeout'], 10.0)
        self.assertEqual(custom_call_args['transport'], mock_transport.return_value)

    def test_request(self):
        """
        Verifies the internal _request method correctly calls the httpx client,
        invokes raise_for_status, and returns the response.
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
        """Tests that _request catches httpx.HTTPStatusError and re-raises it as APIStatusError."""
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
        Tests that _get_entity correctly calls _request with the proper URL and
        JSON payload, and updates the passed-in val dictionary with the response.
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
        Tests the _read_loop helper for processing newline-delimited JSON
        from a byte stream and invoking a callback for each line.
        """
        data = b'{"article1": "content1"}\n{"article2": "content2"}'
        mock_rdr = BytesIO(data)
        mock_cbk = MagicMock(return_value=True)
        self.client._read_loop(mock_rdr, mock_cbk)

        self.assertEqual(mock_cbk.call_count, 2)
        mock_cbk.assert_has_calls([
            call({"article1": "content1"}),
            call({"article2": "content2"})
        ])

    def test_read_loop_stops_when_callback_returns_false(self):
        """Tests that _read_loop correctly stops processing when the callback returns False."""
        data = b'{"a": 1}\n{"b": 2}\n{"c": 3}'
        mock_rdr = BytesIO(data)

        mock_cbk = MagicMock(side_effect=[True, False, True])

        result = self.client._read_loop(mock_rdr, mock_cbk)

        self.assertFalse(result)
        self.assertEqual(mock_cbk.call_count, 2)
        mock_cbk.assert_has_calls([
            call({"a": 1}),
            call({"b": 2})
        ])

    def test_read_loop_logs_warning_on_malformed_json_and_continues(self):
        """
        Tests that _read_loop logs a warning for malformed JSON but continues
        to process subsequent valid lines.
        """
        data = b'{"article1": "content1"}\n{"invalid" json}\n{"article2": "content2"}'
        mock_rdr = BytesIO(data)
        mock_cbk = MagicMock(return_value=True)

        with self.assertLogs(CLIENT_LOGGER_NAME, level='WARNING') as cm:
            self.client._read_loop(mock_rdr, mock_cbk)
            self.assertIn("Skipping line due to JSON decode error", cm.output[0])

        mock_cbk.assert_any_call({"article1": "content1"})
        mock_cbk.assert_any_call({"article2": "content2"})
        self.assertEqual(mock_cbk.call_count, 2)

    def test_read_entity(self):
        """
        Tests _read_entity calls _request with the correct URL
        and passes the decoded JSON response content to the callback.
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
        """
        Tests that the rate-limiting logic within _request correctly calculates
        and applies time.sleep when calls are made within the rate_limit_period.
        """
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
        """Tests that _head_entity raises APIDataError for a non-integer Content-Length."""
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

    def test_request_logs_warning_on_429(self):
        """Tests that _request logs a specific warning when a 429 status code is received."""
        mock_http_client = cast(MagicMock, self.client.http_client)
        mock_req = MagicMock(spec=httpx.Request)
        mock_req.url = "http://test.com/path"
        mock_res = MagicMock(spec=httpx.Response)
        mock_res.status_code = 429
        mock_res.reason_phrase = "Too Many Requests"

        http_error = httpx.HTTPStatusError(
            "Too Many Requests", request=mock_req, response=mock_res
        )
        mock_res.raise_for_status.side_effect = http_error
        mock_http_client.request.return_value = mock_res

        with self.assertLogs(CLIENT_LOGGER_NAME, level='WARNING') as cm:
            with self.assertRaises(APIStatusError):
                self.client._request("GET", "http://test.com/path")

            self.assertIn("Received 429 Too Many Requests. Client may retry.", cm.output[0])

    def test_request_handles_request_error(self):
        """Tests that a generic httpx.RequestError is caught, logged, and re-raised as an APIRequestError."""
        mock_http_client = cast(MagicMock, self.client.http_client)

        mock_req = MagicMock(spec=httpx.Request)
        mock_req.url = "http://unreachable.host/path"

        request_error = httpx.RequestError("Connection refused", request=mock_req)
        mock_http_client.request.side_effect = request_error

        with self.assertLogs(CLIENT_LOGGER_NAME, level='ERROR') as cm:
            with self.assertRaises(APIRequestError):
                self.client._request("GET", "http://unreachable.host/path")
            self.assertIn("Request Error: Connection refused for url http://unreachable.host/path", cm.output[0])

    def test_get_entity_extends_list_correctly(self):
        """Tests that _get_entity correctly extends a list when the API returns a list."""
        req = Request()
        path = "items"
        val = []
        api_response_data = [{"id": 1, "name": "foo"}, {"id": 2, "name": "bar"}]

        with patch.object(self.client, '_request', autospec=True) as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = api_response_data
            mock_request.return_value = mock_response

            self.client._get_entity(req, path, val)

            self.assertEqual(val, api_response_data)

    def test_get_entity_raises_on_json_decode_error(self):
        """Tests that _get_entity raises APIDataError if the response is not valid JSON."""
        with patch.object(self.client, '_request') as mock_request:
            mock_response = MagicMock()
            mock_response.json.side_effect = json.JSONDecodeError(
                "Expecting value", "doc text", 0
            )
            mock_request.return_value = mock_response

            val = {}
            with self.assertRaisesRegex(APIDataError, "Failed to decode JSON from response: Expecting value"):
                self.client._get_entity(Request(), "path", val)

    def test_read_loop_skips_empty_lines(self):
        """Tests that _read_loop correctly skips empty lines or lines with only whitespace."""
        data = b'{"a": 1}\n\n{"b": 2}\n   \n\t\n{"c": 3}'
        mock_rdr = BytesIO(data)
        mock_cbk = MagicMock(return_value=True)

        self.client._read_loop(mock_rdr, mock_cbk)

        self.assertEqual(mock_cbk.call_count, 3)
        mock_cbk.assert_any_call({"a": 1})
        mock_cbk.assert_any_call({"b": 2})
        mock_cbk.assert_any_call({"c": 3})

    def test_head_entity_returns_parsed_headers(self):
        """
        Tests _head_entity correctly parses headers, converting 'Content-Length'
        to an int and stripping quotes from 'ETag'.
        """
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.headers = {
            'Content-Length': '12345',
            'ETag': '"abc-def-123"',
            'Content-Type': 'application/json',
            'Accept-Ranges': 'bytes',
            'Last-Modified': 'Mon, 15 Jan 2001 08:00:00 GMT'
        }

        expected_headers = {
            'Content-Length': 12345,
            'ETag': 'abc-def-123',
            'Content-Type': 'application/json',
            'Accept-Ranges': 'bytes',
            'Last-Modified': 'Mon, 15 Jan 2001 08:00:00 GMT'
        }

        with patch.object(self.client, '_request', return_value=mock_response) as mock_request_method:
            result = self.client._head_entity("some/path")

            expected_url = f"{self.client.base_url}v2/some/path"
            mock_request_method.assert_called_once_with('HEAD', expected_url)

            self.assertDictEqual(result, expected_headers)

    def test_download_entity_returns_early_for_zero_content_length(self):
        """
        Tests _download_entity performs a HEAD request but makes no subsequent
        GET requests if 'Content-Length' is 0.
        """
        with patch.object(self.client, '_head_entity') as mock_head, \
             patch.object(self.client, '_request') as mock_request:

            mock_head.return_value = {'Content-Length': 0}

            self.client._download_entity("some/path", BytesIO())

            mock_head.assert_called_once_with("some/path")
            mock_request.assert_not_called()

    def test_download_entity_without_chunking(self):
        """Tests that _download_entity downloads in a single chunk when chunk size is not positive."""
        self.client.download_chunk_size = -1

        with patch.object(self.client, '_head_entity') as mock_head, \
             patch.object(self.client, '_request') as mock_request:

            mock_head.return_value = {'Content-Length': 2500}
            mock_response = MagicMock(spec=httpx.Response)
            mock_response.content = b'a' * 2500
            mock_request.return_value = mock_response

            mock_writer = BytesIO()
            self.client._download_entity("some/path", mock_writer)

            mock_head.assert_called_once_with("some/path")
            mock_request.assert_called_once()

            called_range = mock_request.call_args.kwargs['headers']['Range']
            self.assertEqual(called_range, 'bytes=0-2499')

    @patch('modules.api.api_client.logger.critical')
    def test_download_entity_handles_api_error_during_chunk_download(self, mock_logger_critical):
        """
        Tests _download_entity catches APIStatusError during a chunk download,
        logs a critical error, and re-raises it as APIRequestError.
        """
        self.client.download_chunk_size = 1000

        mock_request_obj = MagicMock(spec=httpx.Request)
        api_error = APIStatusError("Server Error", request=mock_request_obj, response=MagicMock())

        with patch.object(self.client, '_head_entity', return_value={'Content-Length': 3000}), \
             patch.object(self.client, '_request', side_effect=api_error):

            with self.assertRaises(APIRequestError):
                self.client._download_entity("some/path", BytesIO())

            mock_logger_critical.assert_called_once_with(
                "A download chunk failed, cancelling remaining downloads."
            )

    @patch('modules.api.api_client.logger.critical')
    def test_download_entity_handles_generic_exception_during_chunk_download(self, mock_logger_critical):
        """
        Tests _download_entity catches a generic Exception during a chunk download,
        logs a critical error, and re-raises it as APIDataError.
        """
        self.client.download_chunk_size = 1000
        generic_error = ValueError("Something went wrong")

        with patch.object(self.client, '_head_entity', return_value={'Content-Length': 3000}), \
             patch.object(self.client, '_request', side_effect=generic_error):

            with self.assertRaises(APIDataError):
                self.client._download_entity("some/path", BytesIO())

            mock_logger_critical.assert_called_once_with(
                "A download chunk failed with an unexpected error, cancelling remaining downloads."
            )

    def test_subscribe_to_entity_processes_stream_correctly(self):
        """
        Tests the happy path for _subscribe_to_entity, ensuring it processes a
        stream of newline-delimited JSON and calls the callback. Also checks
        that empty lines are skipped.
        """
        mock_http_client = cast(MagicMock, self.client.http_client)
        mock_response = MagicMock(spec=httpx.Response)

        stream_content = [
            b'{"id": 1, "data": "first"}',
            b'{"id": 2, "data": "second"}',
            b'',
            b'{"id": 3, "data": "third"}'
        ]
        mock_response.iter_lines.return_value = stream_content

        mock_stream_context = MagicMock()
        mock_stream_context.__enter__.return_value = mock_response
        mock_http_client.stream.return_value = mock_stream_context

        mock_cbk = MagicMock(return_value=True)
        req = Request(filters={"project": "enwiki"})

        self.client._subscribe_to_entity("articles", req, mock_cbk)

        expected_url = f"{self.client.realtime_url}v2/articles"
        mock_http_client.stream.assert_called_once()
        call_args = mock_http_client.stream.call_args
        self.assertEqual(call_args.args[0], 'GET')
        self.assertEqual(call_args.args[1], expected_url)
        self.assertIn('json', call_args.kwargs)
        self.assertIn('headers', call_args.kwargs)

        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(mock_cbk.call_count, 3)
        mock_cbk.assert_any_call({"id": 1, "data": "first"})
        mock_cbk.assert_any_call({"id": 2, "data": "second"})
        mock_cbk.assert_any_call({"id": 3, "data": "third"})

    @patch('modules.api.api_client.logger.warning')
    def test_subscribe_to_entity_handles_malformed_json(self, mock_logger_warning):
        """Tests that malformed JSON lines in a stream are skipped and a warning is logged."""
        mock_http_client = cast(MagicMock, self.client.http_client)
        mock_response = MagicMock(spec=httpx.Response)

        stream_content = [
            b'{"id": 1, "data": "good"}',
            b'{"id": 2, "data": "bad" oops}',
            b'{"id": 3, "data": "good again"}'
        ]
        mock_response.iter_lines.return_value = stream_content

        mock_stream_context = MagicMock()
        mock_stream_context.__enter__.return_value = mock_response
        mock_http_client.stream.return_value = mock_stream_context

        mock_cbk = MagicMock(return_value=True)
        self.client._subscribe_to_entity("articles", Request(), mock_cbk)

        self.assertEqual(mock_cbk.call_count, 2)
        mock_logger_warning.assert_called_once_with(
            "Skipping malformed JSON line in stream: %s",
            stream_content[1]
        )

    def test_subscribe_to_entity_raises_on_http_status_error(self):
        """
        Tests that an httpx.HTTPStatusError during streaming is caught and
        re-raised as an APIStatusError.
        """
        mock_http_client = cast(MagicMock, self.client.http_client)
        mock_request = MagicMock(spec=httpx.Request)

        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 500
        mock_response.reason_phrase = "Internal Server Error"

        status_error = httpx.HTTPStatusError(
            "Server Error", request=mock_request, response=mock_response
        )

        mock_http_client.stream.side_effect = status_error

        with self.assertRaises(APIStatusError):
            self.client._subscribe_to_entity("articles", Request(), MagicMock())

    def test_subscribe_to_entity_raises_on_request_error(self):
        """
        Tests that an httpx.RequestError during streaming is caught and
        re-raised as an APIRequestError.
        """
        mock_http_client = cast(MagicMock, self.client.http_client)
        mock_request = MagicMock(spec=httpx.Request)
        request_error = httpx.RequestError("Connection failed", request=mock_request)

        mock_http_client.stream.side_effect = request_error

        with self.assertRaises(APIRequestError):
            self.client._subscribe_to_entity("articles", Request(), MagicMock())

    def test_read_all_processes_valid_tar_gz_archive(self):
        """
        Tests that read_all correctly extracts and processes multiple NDJSON files
        from a valid in-memory .tar.gz archive.
        """
        file1_content = b'{"id": 1, "source": "file1"}\n{"id": 2, "source": "file1"}'
        file2_content = b'{"id": 3, "source": "file2"}'

        tar_buffer = BytesIO()
        with tarfile.open(fileobj=tar_buffer, mode='w:gz') as tar:
            tarinfo1 = tarfile.TarInfo(name='file1.json')
            tarinfo1.size = len(file1_content)
            tar.addfile(tarinfo1, BytesIO(file1_content))

            tarinfo2 = tarfile.TarInfo(name='file2.json')
            tarinfo2.size = len(file2_content)
            tar.addfile(tarinfo2, BytesIO(file2_content))

            dir_info = tarfile.TarInfo(name='a_directory/')
            dir_info.type = tarfile.DIRTYPE
            tar.addfile(dir_info)

        tar_buffer.seek(0)

        mock_cbk = MagicMock(return_value=True)
        self.client.read_all(tar_buffer, mock_cbk)

        self.assertEqual(mock_cbk.call_count, 3)
        mock_cbk.assert_any_call({"id": 1, "source": "file1"})
        mock_cbk.assert_any_call({"id": 2, "source": "file1"})
        mock_cbk.assert_any_call({"id": 3, "source": "file2"})

    def test_read_all_raises_on_corrupt_tar_archive(self):
        """
        Tests that read_all raises an APIDataError when provided with a
        corrupt or invalid .tar.gz file.
        """
        corrupt_data = BytesIO(b"this is definitely not a tar file")

        mock_cbk = MagicMock()

        with self.assertRaisesRegex(APIDataError, "Failed to decompress Gzip archive"):
            self.client.read_all(corrupt_data, mock_cbk)

        mock_cbk.assert_not_called()

    @patch('tarfile.open')
    def test_read_all_handles_tar_error(self, mock_tarfile_open):
        """
        Tests that read_all correctly catches a tarfile.TarError and re-raises
        it as an APIDataError.
        """
        with patch('modules.api.api_client.gzip_ng_threaded.open') as mock_gzip:
            mock_gzip.return_value.__enter__.return_value = BytesIO(b'dummy data')
            mock_tarfile_open.side_effect = tarfile.TarError("Mocked tarfile error")

            with self.assertRaisesRegex(APIDataError, "Failed to read tar archive: Mocked tarfile error"):
                self.client.read_all(BytesIO(b'dummy gzip data'), MagicMock())

            mock_tarfile_open.assert_called_once()

    def test_set_access_token(self):
        """
        Tests that set_access_token correctly updates the client's access token
        on the instance and in the httpx headers.
        """
        self.client.http_client.headers = {}

        new_token = "a-brand-new-token"
        self.client.set_access_token(new_token)

        self.assertEqual(self.client.access_token, new_token)

        self.assertEqual(
            self.client.http_client.headers['Authorization'],
            f'Bearer {new_token}'
        )

    def test_get_batches_prefix(self):
        """
        Tests the internal _get_batches_prefix helper method to ensure it
        formats the date and hour correctly.
        """
        test_time = datetime(2001, 1, 15, 12, 00, 0)
        expected_prefix = "batches/2001-01-15/12"
        self.assertEqual(self.client._get_batches_prefix(test_time), expected_prefix)

    @patch.object(Client, '_get_entity', autospec=True)
    def test_all_get_entity_wrappers_call_correct_paths(self, mock_get_entity):
        """
        Tests all simple wrappers around _get_entity to ensure they call it
        with the correct path format.
        """
        req = Request()
        test_id_str = "test-id"
        test_id_int = 123
        test_time = datetime(2001, 1, 15, 12)

        test_cases = {
            'get_codes': ([], "codes"),
            'get_code': ([test_id_str], f"codes/{test_id_str}"),
            'get_languages': ([], "languages"),
            'get_language': ([test_id_str], f"languages/{test_id_str}"),
            'get_projects': ([], "projects"),
            'get_project': ([test_id_str], f"projects/{test_id_str}"),
            'get_namespaces': ([], "namespaces"),
            'get_namespace': ([test_id_int], f"namespaces/{test_id_int}"),
            'get_batches': ([test_time], "batches/2001-01-15/12"),
            'get_batch': ([test_time, test_id_str], f"batches/2001-01-15/12/{test_id_str}"),
            'get_snapshots': ([], "snapshots"),
            'get_snapshot': ([test_id_str], f"snapshots/{test_id_str}"),
            'get_chunks': ([test_id_str], f"snapshots/{test_id_str}/chunks"),
            'get_chunk': ([test_id_str, test_id_str], f"snapshots/{test_id_str}/chunks/{test_id_str}"),
            'get_articles': ([test_id_str], f"articles/{test_id_str}"),
            'get_structured_contents': ([test_id_str], f"structured-contents/{test_id_str}"),
            'get_structured_snapshots': ([], "snapshots/structured-contents/"),
            'get_structured_snapshot': ([test_id_str], f"snapshots/structured-contents/{test_id_str}")
        }

        with patch.object(Code, 'from_json'), \
             patch.object(Language, 'from_json'), \
             patch.object(Project, 'from_json'), \
             patch.object(Namespace, 'from_json'), \
             patch.object(Batch, 'from_json'), \
             patch.object(Snapshot, 'from_json'), \
             patch.object(Article, 'from_json'), \
             patch.object(StructuredContent, 'from_json'):

            for method_name, (args, expected_path) in test_cases.items():
                with self.subTest(method=method_name):
                    method_to_call = getattr(self.client, method_name)
                    full_args = args + [req]
                    method_to_call(*full_args)

                    call_args = mock_get_entity.call_args[0]
                    self.assertEqual(call_args[2], expected_path)
                    mock_get_entity.reset_mock()

    @patch.object(Client, '_head_entity', autospec=True)
    @patch.object(Client, '_read_entity', autospec=True)
    @patch.object(Client, '_download_entity', autospec=True)
    @patch.object(Client, '_subscribe_to_entity', autospec=True)
    def test_all_action_wrappers_call_correct_paths(self, mock_subscribe, mock_download, mock_read, mock_head):
        """
        Tests wrappers for head, read, download, and subscribe methods to ensure
        they call the correct internal method with the correct path.
        """
        test_id = "test-id"
        test_time = datetime(2001, 1, 15, 12)
        mock_cbk = MagicMock()
        mock_writer = BytesIO()
        req = Request()

        test_cases = {
            'head_batch': (mock_head, [test_time, test_id], "batches/2001-01-15/12/test-id/download"),
            'read_batch': (mock_read, [test_time, test_id, mock_cbk], "bbatches/2001-01-15/12/test-id/download"),
            'download_batch': (mock_download, [test_time, test_id, mock_writer], "batches/2001-01-15/12/test-id/download"),
            'head_snapshot': (mock_head, [test_id], "snapshots/test-id/download"),
            'read_snapshot': (mock_read, [test_id, mock_cbk], "snapshots/test-id/download"),
            'download_snapshot': (mock_download, [test_id, mock_writer], "snapshots/test-id/download"),
            'head_chunk': (mock_head, [test_id, test_id], "snapshots/test-id/chunks/test-id/download"),
            'read_chunk': (mock_read, [test_id, test_id, mock_cbk], "snapshots/test-id/chunks/test-id/download"),
            'download_chunk': (mock_download, [test_id, test_id, mock_writer], "snapshots/test-id/chunks/test-id/download"),
            'head_structured_snapshot': (mock_head, [test_id], "snapshots/structured-contents/test-id/download"),
            'read_structured_snapshot': (mock_read, [test_id, mock_cbk], "snapshots/structured-contents/test-id/download"),
            'download_structured_snapshot': (mock_download, [test_id, mock_writer], "snapshots/structured-contents/test-id/download"),
            'stream_articles': (mock_subscribe, [req, mock_cbk], "articles"),
        }

        with patch.object(Batch, 'from_json'), \
             patch.object(Snapshot, 'from_json'), \
             patch.object(Article, 'from_json'), \
             patch.object(StructuredContent, 'from_json'):

            for method_name, (mock_to_check, args, expected_path) in test_cases.items():
                with self.subTest(method=method_name):
                    method_to_call = getattr(self.client, method_name)
                    method_to_call(*args)

                    mock_to_check.assert_called_once()
                    call_args = mock_to_check.call_args[0]
                    self.assertEqual(call_args[1], expected_path)
                    mock_to_check.reset_mock()

    @patch.object(Client, '_get_entity', autospec=True)
    def test_get_entity_methods_parse_data_correctly(self, mock_get_entity):
        """
        Tests that public get_* methods correctly parse the JSON response
        from _get_entity into the expected model objects.
        """

        def create_side_effect(json_to_use):
            """Creates a side-effect function that populates 'val'."""

            def mock_side_effect(*args):
                val = args[3]
                if isinstance(val, list):
                    val.extend(json_to_use)
                elif isinstance(val, dict):
                    val.update(json_to_use)
            return mock_side_effect

        test_cases = {
            'get_codes': ([], Code, [{"identifier": "c1"}], list, "c1", "identifier"),
            'get_languages': ([], Language, [{"identifier": "l1"}], list, "l1", "identifier"),
            'get_projects': ([], Project, [{"identifier": "p1"}], list, "p1", "identifier"),
            'get_namespaces': ([], Namespace, [{"identifier": 1}], list, 1, "identifier"),
            'get_batches': ([datetime(2024,1,1)], Batch, [{"identifier": "b1"}], list, "b1", "identifier"),
            'get_snapshots': ([], Snapshot, [{"identifier": "s1"}], list, "s1", "identifier"),
            'get_chunks': (["s1"], Snapshot, [{"identifier": "c1"}], list, "c1", "identifier"),
            'get_articles': (["Test"], Article, [{"name": "a1"}], list, "a1", "name"),
            'get_structured_contents': (["Test"], StructuredContent, [{"name": "sc1"}], list, "sc1", "name"),
            'get_structured_snapshots': ([], StructuredContent, [{"identifier": "scs1"}], list, "scs1", "identifier"),
            'get_code': (["c1"], Code, {"identifier": "c1"}, Code, "c1", "identifier"),
            'get_language': (["l1"], Language, {"identifier": "l1"}, Language, "l1", "identifier"),
            'get_project': (["p1"], Project, {"identifier": "p1"}, Project, "p1", "identifier"),
            'get_namespace': ([1], Namespace, {"identifier": 1}, Namespace, 1, "identifier"),
            'get_batch': ([datetime(2024,1,1), "b1"], Batch, {"identifier": "b1"}, Batch, "b1", "identifier"),
            'get_snapshot': (["s1"], Snapshot, {"identifier": "s1"}, Snapshot, "s1", "identifier"),
            'get_chunk': (["s1", "c1"], Snapshot, {"identifier": "c1"}, Snapshot, "c1", "identifier"),
            'get_structured_snapshot': (["scs1"], StructuredContent, {"identifier": "scs1"}, StructuredContent, "scs1", "identifier"),
        }

        for method_name, (args, model, mock_json, expected_type, expected_id, id_attr) in test_cases.items():

            with self.subTest(method=method_name):
                mock_get_entity.side_effect = create_side_effect(mock_json)

                method_to_call = getattr(self.client, method_name)
                full_args = args + [Request()]

                with patch.object(model, 'from_json', wraps=model.from_json) as mock_from_json:
                    result = method_to_call(*full_args)

                    self.assertIsInstance(result, expected_type)
                    self.assertGreater(mock_from_json.call_count, 0)

                    if expected_type is list:
                        self.assertEqual(getattr(result[0], id_attr), expected_id)
                    else:
                        self.assertEqual(getattr(result, id_attr), expected_id)

                mock_get_entity.reset_mock()

    @patch.object(Client, '_read_entity', autospec=True)
    @patch.object(Client, '_subscribe_to_entity', autospec=True)
    def test_read_action_methods_parse_data_correctly(self, mock_subscribe, mock_read):
        """
        Tests that public read_* and stream_* methods correctly parse JSON
        and pass the model object to the user's callback.
        """

        def create_side_effect(json_to_use):
            """Creates a side-effect function that calls the internal callback."""

            def mock_internal_method(*args):
                internal_cbk_arg = args[-1]
                internal_cbk_arg(json_to_use)
            return mock_internal_method

        test_cases = {
            'read_batch': (mock_read, [datetime(2024,1,1), "b1"], Batch, {"identifier": "b1"}, "identifier", "b1"),
            'read_snapshot': (mock_read, ["s1"], Snapshot, {"identifier": "s1"}, "identifier", "s1"),
            'read_chunk': (mock_read, ["s1", "c1"], Snapshot, {"identifier": "c1"}, "identifier", "c1"),
            'read_structured_snapshot': (mock_read, ["scs1"], StructuredContent, {"identifier": "scs1"}, "identifier", "scs1"),
            'stream_articles': (mock_subscribe, [Request()], Article, {"name": "a1"}, "name", "a1"),
        }

        for method_name, (mock_to_patch, args, model, mock_json, id_attr, expected_id) in test_cases.items():

            with self.subTest(method=method_name):

                mock_to_patch.side_effect = create_side_effect(mock_json)

                user_callback = MagicMock(return_value=True)
                method_to_call = getattr(self.client, method_name)
                full_args = args + [user_callback]

                with patch.object(model, 'from_json', wraps=model.from_json) as mock_from_json:
                    method_to_call(*full_args)

                    mock_from_json.assert_called_once_with(mock_json)
                    user_callback.assert_called_once()

                    result_obj = user_callback.call_args[0][0]
                    self.assertIsInstance(result_obj, model)
                    self.assertEqual(getattr(result_obj, id_attr), expected_id)

                mock_to_patch.reset_mock()

    def test_get_entity_methods_raise_apidataerror_on_model_error(self):
        """
        Tests that if a model's from_json raises DataModelError, the
        client's get_* method correctly raises APIDataError.
        """
        test_cases = {
            'get_codes': ([], Code),
            'get_code': (["c1"], Code),
            'get_articles': (["Test"], Article),
        }

        with patch.object(Client, '_get_entity', autospec=True) as mock_get_entity:
            for method_name, (args, model) in test_cases.items():
                with self.subTest(method=method_name):

                    def mock_get_entity_side_effect(_self, _req, _path, val):
                        if isinstance(val, list):
                            val.extend([{"id": 1}])
                        elif isinstance(val, dict):
                            val.update({"id": 1})

                    mock_get_entity.side_effect = mock_get_entity_side_effect
                    mock_get_entity.reset_mock()

                    with patch.object(model, 'from_json', side_effect=DataModelError("Test Model Error")):
                        method_to_call = getattr(self.client, method_name)
                        full_args = args + [Request()]

                        with self.assertRaisesRegex(APIDataError, "Test Model Error"):
                            method_to_call(*full_args)

                        mock_get_entity.assert_called_once()

class TestTarfileStreamWrapper(unittest.TestCase):
    """Test suite for the _TarfileStreamWrapper class."""

    def setUp(self):
        self.mock_stream = MagicMock(spec=BytesIO)
        self.wrapper = _TarfileStreamWrapper(self.mock_stream)

    def test_passthrough_methods(self):
        """Tests that methods are passed through to the underlying stream."""
        self.wrapper.read(10)
        self.mock_stream.read.assert_called_once_with(10)

        self.wrapper.close()
        self.mock_stream.close.assert_called_once()

        self.wrapper.flush()
        self.mock_stream.flush.assert_called_once()

        self.mock_stream.closed = True
        self.assertTrue(self.wrapper.closed)

    def test_wrapper_methods(self):
        """Tests the methods implemented by the wrapper itself."""
        self.assertTrue(self.wrapper.readable())
        self.assertFalse(self.wrapper.writable())
        self.assertFalse(self.wrapper.seekable())


class TestRequest(unittest.TestCase):
    """Test suite for the Request class."""
    def test_init(self):
        """
        Tests Request initialization with default values and with all parameters specified,
        verifying to_json output for both.
        """
        req = Request()
        self.assertIsNone(req.since)
        self.assertEqual(req.fields, [])
        self.assertNotIn('filters', req.to_json())
        self.assertIsNone(req.limit)
        self.assertEqual(req.parts, [])
        self.assertEqual(req.offsets, {})
        self.assertEqual(req.since_per_partition, {})
        self.assertEqual(req.to_json(), {})

        since = datetime(2024, 1, 1)
        fields = ["field1", "field2"]
        filters = [Filter("field", "value")]
        limit = 10
        parts = [1, 2, 3]
        offsets = {1: 10, 2: 20}
        since_per_partition = {1: datetime(2024, 1, 1), 2: datetime(2024, 1, 2)}
        req = Request(since=since,
                      fields=fields,
                      filters=filters,
                      limit=limit,
                      parts=parts,
                      offsets=offsets,
                      since_per_partition=since_per_partition)

        self.assertEqual(req.since, since)
        self.assertEqual(req.fields, fields)
        self.assertEqual(req.limit, limit)
        self.assertEqual(req.parts, parts)
        self.assertEqual(req.offsets, offsets)
        self.assertEqual(req.since_per_partition, since_per_partition)

        expected_json = {
            'since': '2024-01-01T00:00:00',
            'fields': ['field1', 'field2'],
            'filters': [{'field': 'field', 'value': 'value'}],
            'limit': 10,
            'parts': [1, 2, 3],
            'offsets': {1: 10, 2: 20},
            'since_per_partition': {1: '2024-01-01T00:00:00', 2: '2024-01-02T00:00:00'}
        }
        self.assertDictEqual(req.to_json(), expected_json)

    def test_init_with_dict_filters(self):
        """
        Tests that Request correctly converts a dict of filters into
        the expected list format in its to_json output.
        """
        filters_dict = {'project': 'enwiki', 'namespace': '0'}
        req = Request(filters=filters_dict)

        expected_json_filters = [
            {'field': 'project', 'value': 'enwiki'},
            {'field': 'namespace', 'value': '0'}
        ]

        self.assertCountEqual(req.to_json()['filters'], expected_json_filters)

    def test_to_json_omits_empty_and_none_values(self):
        """Tests that to_json correctly omits keys with None or empty values."""
        req = Request(
            since=None,
            fields=[],
            filters=None,
            limit=10,
            parts=[],
            offsets={},
        )
        expected_json = {'limit': 10}
        self.assertDictEqual(req.to_json(), expected_json)


class TestFilter(unittest.TestCase):
    """Test suite for the Filter class."""
    def test_init_and_to_dict(self):
        """Tests basic instantiation and to_dict conversion of the Filter class."""
        field = "test_field"
        value = "test_value"
        filter_obj = Filter(field, value)
        self.assertEqual(filter_obj.field, field)
        self.assertEqual(filter_obj.value, value)

        expected_dict = {'field': 'test_field', 'value': 'test_value'}
        self.assertDictEqual(filter_obj.to_dict(), expected_dict)


if __name__ == '__main__':
    unittest.main()
