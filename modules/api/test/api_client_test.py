# pylint: disable=W0212, too-many-locals, too-many-public-methods

"""
Unit tests for the `api_client` module.

This file contains test suites for the Client, Request, and Filter classes,
ensuring their methods and initializers behave as expected. Mocks are used
to isolate the tests from actual network calls.
"""

import unittest
import json
import tarfile
from unittest.mock import MagicMock, patch
from datetime import datetime
from io import BytesIO
from typing import cast
import httpx
from modules.api.api_client import Client, Request, Filter
from modules.api.exceptions import APIStatusError, APIDataError, APIRequestError

CLIENT_LOGGER_NAME = 'modules.api.api_client'


class TestClient(unittest.TestCase):
    """Test suite for the Client class in the api_client module."""

    def setUp(self):
        """Set up a test client and mock the HTTP client before each test."""
        self.client = Client(access_token="test_access_token")
        self.client.http_client = MagicMock(spec=httpx.Client)

    def test_init(self):
        """Tests that the Client initializes correctly with default values and with custom overrides."""
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
        """Tests that `_request` catches `httpx.HTTPStatusError` and re-raises it as `APIStatusError`."""
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
        Tests that `_get_entity` correctly calls `_request` with the proper URL and
        JSON payload, and updates the passed-in `val` dictionary with the response.
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
        Tests `_read_entity` calls `_request` with the correct URL
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
        Tests that the rate-limiting logic within `_request` correctly calculates
        and applies `time.sleep` when calls are made within the `rate_limit_period`.
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
            # Configure the mock to raise JSONDecodeError
            mock_response.json.side_effect = json.JSONDecodeError(
                "Expecting value", "doc text", 0
            )
            mock_request.return_value = mock_response

            val = {}
            with self.assertRaisesRegex(APIDataError, "Failed to decode JSON from response: Expecting value"):
                self.client._get_entity(Request(), "path", val)

    def test_read_loop_skips_empty_lines(self):
        """Tests that `_read_loop` correctly skips empty lines or lines with only whitespace."""
        data = b'{"a": 1}\n\n{"b": 2}\n   \n\t\n{"c": 3}'
        mock_rdr = BytesIO(data)
        mock_cbk = MagicMock()

        self.client._read_loop(mock_rdr, mock_cbk)

        self.assertEqual(mock_cbk.call_count, 3)
        mock_cbk.assert_any_call({"a": 1})
        mock_cbk.assert_any_call({"b": 2})
        mock_cbk.assert_any_call({"c": 3})

    def test_head_entity_returns_parsed_headers(self):
        """
        Tests `_head_entity` correctly parses headers, converting 'Content-Length'
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
        Tests `_download_entity` performs a HEAD request but makes no subsequent
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
        Tests `_download_entity` catches `APIStatusError` during a chunk download,
        logs a critical error, and re-raises it as `APIRequestError`.
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
        Tests `_download_entity` catches a generic `Exception` during a chunk download,
        logs a critical error, and re-raises it as `APIDataError`.
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

        mock_cbk = MagicMock()
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

        mock_cbk = MagicMock()
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

        mock_cbk = MagicMock()
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

        with self.assertRaisesRegex(APIDataError, "Failed to read tar archive"):
            self.client.read_all(corrupt_data, mock_cbk)

        mock_cbk.assert_not_called()

    @patch('tarfile.open')
    def test_read_all_handles_tar_error(self, mock_tarfile_open):
        """
        Tests that read_all correctly catches a tarfile.TarError and re-raises
        it as an APIDataError.
        """
        mock_tarfile_open.side_effect = tarfile.TarError("Mocked tarfile error")

        with self.assertRaisesRegex(APIDataError, "Failed to read tar archive: Mocked tarfile error"):
            self.client.read_all(BytesIO(b'dummy data'), MagicMock())

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
    def test_all_get_entity_wrappers(self, mock_get_entity):
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
    def test_all_action_wrappers(self, mock_subscribe, mock_download, mock_read, mock_head):
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

        for method_name, (mock_to_check, args, expected_path) in test_cases.items():
            with self.subTest(method=method_name):
                method_to_call = getattr(self.client, method_name)
                method_to_call(*args)

                mock_to_check.assert_called_once()
                call_args = mock_to_check.call_args[0]
                self.assertEqual(call_args[1], expected_path)
                mock_to_check.reset_mock()

class TestRequest(unittest.TestCase):
    """Test suite for the Request class."""
    def test_init(self):
        """
        Tests Request initialization with default values and with all parameters specified,
        verifying `to_json` output for both.
        """
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
        """
        Tests that `Request` correctly converts a `dict` of filters into
        the expected list format in its `to_json` output.
        """
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
