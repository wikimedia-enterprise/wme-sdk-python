"""
Provides a client for interacting with the Wikimedia Enterprise API.

This module contains the primary `Client` class for making API requests,
as well as helper classes `Request` and `Filter` for building queries.
"""

import datetime
import io
import json
import logging
import tarfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Dict, List, Optional, Union
import httpx
from .exceptions import APIDataError, APIRequestError, APIStatusError

logger = logging.getLogger(__name__)

DATE_FORMAT = "%Y-%m-%d"
HOUR_FORMAT = "%H"

class Filter:
    """Represents a simple key-value filter for an API query."""
    def __init__(self, field: str, value: str):
        """Initializes a Filter object.

        Args:
            field (str): The name of the field to filter on.
            value (str): The value to filter for.
        """
        self.field = field
        self.value = value

    def to_dict(self):
        """Converts the Filter object to a dictionary.

        Returns:
            A dictionary representation of the filter, suitable for JSON serialization.
        """
        return {
            'field': self.field,
            'value': self.value
        }


class Request:
    """Builds and holds the parameters for an API request payload."""
    since: Optional[datetime.datetime]
    fields: List[str]
    limit: Optional[int]
    parts: List[int]
    offsets: Dict[int, int]
    since_per_partition: Dict[int, datetime.datetime]
    _filters_list: List[Dict[str, str]]

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    # Disabling these warnings to maintain backward compatibility for users
    def __init__(self,
                 since: Optional[datetime.datetime] = None,
                 fields: Optional[List[str]] = None,
                 limit: Optional[int] = None,
                 parts: Optional[List[int]] = None,
                 offsets: Optional[Dict[int, int]] = None,
                 since_per_partition: Optional[Dict[int, datetime.datetime]] = None,
                 filters: Optional[Union[Dict[str, str], List[Any]]] = None):
        """Initializes a request object with query parameters.

        Args:
            since: Retrieve items created since this timestamp.
            fields: A list of specific fields to return in the response.
            limit: The maximum number of items to return.
            parts: A list of partitions to query from.
            offsets: A dictionary mapping partition numbers to offsets.
            since_per_partition: A dictionary mapping partition numbers to "since" timestamps.
            filters: Filters to apply to the query. Can be a simple dictionary or a list of Filter objects.
        """
        self.since = since
        self.fields = fields if fields is not None else []
        self.limit = limit
        self.parts = parts if parts is not None else []
        self.offsets = offsets if offsets is not None else {}
        self.since_per_partition = since_per_partition if since_per_partition is not None else {}

        if isinstance(filters, dict):
            self._filters_list = self._convert_dict_to_filters(filters)
        elif isinstance(filters, list):
            self._filters_list = [f.to_dict() for f in filters]
        else:
            self._filters_list = []

    def _convert_dict_to_filters(self, filters_dict: Dict[str, str]) -> List[Dict[str, str]]:
        """Converts a {'field': 'value'} dict to [{'field':..., 'value':...}]"""
        return [{"field": key, "value": value} for key, value in filters_dict.items()]

    def to_json(self):
        """
        Serializes the Request object into a JSON-compatible dictionary.

        Any parameters that are None, empty lists, or empty dicts are omitted
        from the final output to create a clean request payload.

        Returns:
            A dictionary representing the API request payload.
        """
        result = {
            'since': self.since.isoformat() if self.since else None,
            'fields': self.fields if self.fields else None,
            'filters': self._filters_list if self._filters_list else None,
            'limit': self.limit,
            'parts': self.parts if self.parts else None,
            'offsets': self.offsets if self.offsets else None,
            'since_per_partition': {k: v.isoformat() for k, v in self.since_per_partition.items()} if self.since_per_partition else None
        }

        # Remove keys with None or empty values
        return {k: v for k, v in result.items() if v not in [None, [], {}, '']}


class Client:
    """
    The main client for interacting with the Wikimedia Enterprise API.

    This client handles authentication, HTTP requests, retries, rate limiting,
    and processing of API responses.
    """
    def __init__(self,
                 user_agent: Optional[str] = None,
                 timeout: float = 30.0,
                 max_retries: int = 3,
                 rate_limit_per_second: Optional[float] = None,
                 **kwargs):
        """
        Initializes the API Client using HTTPX.

        Args:
            user_agent (str, optional): A custom User-Agent string for requests. If not provided, defaults to "WME Python SDK".
            timeout (float, optional): The timeout for requests in seconds. Defaults to 30.0.
            max_retries (int, optional): The maximum number of retries for failed requests. Defaults to 3.
            rate_limit_per_second (float, optional): The maximum number of requests to make per second. Defaults to None (no limit).
            **kwargs: Other optional settings like 'base_url', 'realtime_url', 'access_token', etc.
        """
        self.access_token = kwargs.get('access_token', "")

        self.user_agent = user_agent or "WME Python SDK"

        self.rate_limit_period = 1.0 / rate_limit_per_second if rate_limit_per_second else 0
        self.last_request_time = 0

        headers = {
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }

        retry_transport = httpx.HTTPTransport(
            retries=max_retries,
        )

        self.http_client = httpx.Client(
            headers=headers,
            timeout=timeout,
            transport=retry_transport,
            http2=True
        )

        self.base_url = kwargs.get('base_url', "https://api.enterprise.wikimedia.com/")
        self.realtime_url = kwargs.get('realtime_url', "https://realtime.enterprise.wikimedia.com/")
        self.download_chunk_size = kwargs.get('download_chunk_size', -1)
        self.download_concurrency = kwargs.get('download_concurrency', 10)
        self.scanner_buffer_size = kwargs.get('scanner_buffer_size', 20971520)

    def _rate_limit_wait(self):
        if self.rate_limit_period == 0:
            return

        elapsed = time.monotonic() - self.last_request_time
        wait_time = self.rate_limit_period - elapsed
        if wait_time > 0:
            time.sleep(wait_time)
        self.last_request_time = time.monotonic()

    def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """
        Internal method to perform an HTTP request.

        Handles rate limiting and raises an exception for non-2xx responses.

        Args:
            method (str): The HTTP method (e.g., 'GET', 'POST').
            url (str): The full URL for the request.
            **kwargs: Additional keyword arguments passed to the httpx request.

        Returns:
            The httpx.Response object.

        Raises:
            httpx.HTTPStatusError: If the response status code is 4xx or 5xx.
        """
        self._rate_limit_wait()

        try:
            response = self.http_client.request(method, url, **kwargs)
            logger.debug("Request successful: %s %s -> %s", method, url, response.status_code)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                logger.warning("Received 429 Too Many Requests. Client may retry.")
            else:
                logger.error("HTTP Status Error: %s for url %s", e.response.status_code, e.request.url)
            raise APIStatusError(f"HTTP Error: {e.response.status_code} {e.response.reason_phrase}", request=e.request, response=e.response) from e
        except httpx.RequestError as e:
            logger.error("Request Error: %s for url %s", e, e.request.url)
            raise APIRequestError(f"Request Error: {e} for url {e.request.url}", request=e.request) from e

    def _get_entity(self, req: Optional[Request], path: str, val: Any):
        """Fetches a JSON entity and populates a list or dict."""
        json_payload = req.to_json() if req else None
        response = self._request('POST', f"{self.base_url}v2/{path}", json=json_payload)
        try:
            json_response = response.json()
        except json.JSONDecodeError as e:
            raise APIDataError(f"Failed to decode JSON from response: {e.msg}") from e

        if isinstance(val, list) and isinstance(json_response, list):
            val.extend(json_response)
        elif isinstance(val, dict) and isinstance(json_response, dict):
            val.update(json_response)
        else:
            raise APIDataError("Mismatched types between expected container and JSON response.")

    def _read_loop(self, rdr: io.BytesIO, cbk: Callable[[dict], Any]):
        scanner = io.TextIOWrapper(rdr)
        for line in scanner:
            if not line.strip():
                continue
            try:
                article = json.loads(line)
                cbk(article)
            except json.JSONDecodeError:
                logger.warning("Skipping line due to JSON decode error", exc_info=True)

    def _read_entity(self, path: str, cbk: Callable[[dict], Any]):
        response = self._request('GET', f"{self.base_url}v2/{path}")
        self._read_loop(io.BytesIO(response.content), cbk)

    def _head_entity(self, path: str) -> dict:
        response = self._request('HEAD', f"{self.base_url}v2/{path}")
        try:
            content_length = int(response.headers.get('Content-Length', 0))
        except (ValueError, TypeError) as e:
            raise APIDataError(f"Invalid 'Content-Length' header received: {response.headers.get('Content-Length')}") from e

        headers = {
            'ETag': response.headers.get('ETag', '').strip('"'),
            'Content-Type': response.headers.get('Content-Type', ''),
            'Accept-Ranges': response.headers.get('Accept-Ranges', ''),
            'Last-Modified': response.headers.get('Last-Modified', ''),
            'Content-Length': content_length
        }
        return headers

    def _download_entity(self, path: str, writer: io.BytesIO):
        """Downloads a large entity, potentially in parallel chunks."""
        full_path = f"{self.base_url}v2/{path}"
        headers = self._head_entity(path)
        content_length = headers['Content-Length']

        if content_length == 0:
            return

        if self.download_chunk_size > 0:
            chunk_size = min(self.download_chunk_size, content_length)
            chunks = [(i, min(i + chunk_size, content_length) - 1) for i in range(0, content_length, chunk_size)]
        else:
            chunks = [(0, content_length - 1)]

        def download_chunk(start, end):
            range_header = {'Range': f"bytes={start}-{end}"}
            res = self._request('GET', full_path, headers=range_header)
            writer.seek(start)
            writer.write(res.content)

        with ThreadPoolExecutor(max_workers=self.download_concurrency) as executor:
            futures = {executor.submit(download_chunk, start, end): (start, end) for start, end in chunks}
            for future in as_completed(futures):
                try:
                    future.result()
                except (APIRequestError, APIStatusError) as e:
                    logger.critical("A download chunk failed, cancelling remaining downloads.")
                    for f in futures:
                        f.cancel()
                    raise APIRequestError(
                        f"A download chunk failed: {e}",
                        request=e.request
                ) from e
                except Exception as e:
                    logger.critical("A download chunk failed with an unexpected error, cancelling remaining downloads.")
                    for f in futures:
                        f.cancel()
                    raise APIDataError(
                        f"A download chunk failed with an unexpected error: {e}"
                    ) from e

    def _subscribe_to_entity(self, path: str, req: Request, cbk: Callable[[dict], Any]):
        json_payload = req.to_json() if req else None
        headers = {
            'Cache-Control': 'no-cache',
            'Accept': 'application/x-ndjson',
            'Connection': 'keep-alive'
        }

        try:
            with self.http_client.stream(
                'GET',
                f"{self.realtime_url}v2/{path}",
                json=json_payload,
                headers=headers
            ) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        try:
                            article=json.loads(line)
                            cbk(article)
                        except json.JSONDecodeError:
                            logger.warning("Skipping malformed JSON line in stream: %s", line)
        except httpx.HTTPStatusError as e:
            raise APIStatusError(f"HTTP Error: {e.response.status_code} on stream", request=e.request, response=e.response) from e
        except httpx.RequestError as e:
            raise APIRequestError(f"Stream Request Error: {e}", request=e.request) from e

    def read_all(self, rdr: io.BytesIO, cbk: Callable[[dict], Any]):
        """Reads a tar archive"""
        try:
            with tarfile.open(fileobj=rdr, mode='r:gz') as tar:
                for member in tar.getmembers():
                    f = tar.extractfile(member)
                    if f:
                        with f:
                            self._read_loop(io.BytesIO(f.read()), cbk)
        except tarfile.TarError as e:
            raise APIDataError(f"Failed to read tar archive: {e}") from e

    def set_access_token(self, token: str):
        """Sets the access token"""
        self.access_token = token
        self.http_client.headers['Authorization'] = f'Bearer {token}'

    def get_codes(self, req: Request) -> List[dict]:
        """Retrieves codes"""
        codes = []
        self._get_entity(req, "codes", codes)
        return codes

    def get_code(self, idr: str, req: Request) -> dict:
        """Retrieves a single code"""
        code = {}
        self._get_entity(req, f"codes/{idr}", code)
        return code

    def get_languages(self, req: Request) -> List[dict]:
        """Retrieves languages"""
        languages = []
        self._get_entity(req, "languages", languages)
        return languages

    def get_language(self, idr: str, req: Request) -> dict:
        """Retrieves a language"""
        language = {}
        self._get_entity(req, f"languages/{idr}", language)
        return language

    def get_projects(self, req: Request) -> List[dict]:
        """Retrieves projects"""
        projects = []
        self._get_entity(req, "projects", projects)
        return projects

    def get_project(self, idr: str, req: Request) -> dict:
        """Retrieves a project"""
        project = {}
        self._get_entity(req, f"projects/{idr}", project)
        return project

    def get_namespaces(self, req: Request) -> List[dict]:
        """Retrieves namespaces"""
        namespaces = []
        self._get_entity(req, "namespaces", namespaces)
        return namespaces

    def get_namespace(self, idr: int, req: Request) -> dict:
        """Retrieves a namespace"""
        namespace = {}
        self._get_entity(req, f"namespaces/{idr}", namespace)
        return namespace

    def _get_batches_prefix(self, timestamp: datetime.datetime):
        return f"batches/{timestamp.strftime(DATE_FORMAT)}/{timestamp.strftime(HOUR_FORMAT)}"

    def get_batches(self, timestamp: datetime.datetime, req: Request) -> List[dict]:
        """Retrieves data batches"""
        batches = []
        self._get_entity(req, self._get_batches_prefix(timestamp), batches)
        return batches

    def get_batch(self, timestamp: datetime.datetime, idr: str, req: Request) -> dict:
        """Retrieves a single batch"""
        batch = {}
        self._get_entity(req, f"{self._get_batches_prefix(timestamp)}/{idr}", batch)
        return batch

    def head_batch(self, timestamp: datetime.datetime, idr: str) -> dict:
        """Retrieves metadata for a specific data batch."""
        return self._head_entity(f"{self._get_batches_prefix(timestamp)}/{idr}/download")

    def read_batch(self, timestamp: datetime.datetime, idr: str, cbk: Callable[[dict], Any]):
        """Reads and processes the content of a specific data batch via a callback."""
        self._read_entity(f"b{self._get_batches_prefix(timestamp)}/{idr}/download", cbk)

    def download_batch(self, timestamp: datetime.datetime, idr: str, writer: io.BytesIO):
        """Downloads a batch"""
        self._download_entity(f"{self._get_batches_prefix(timestamp)}/{idr}/download", writer)

    def get_snapshots(self, req: Request) -> List[dict]:
        """Retrieves snapshots"""
        snapshots = []
        self._get_entity(req, "snapshots", snapshots)
        return snapshots

    def get_snapshot(self, idr: str, req: Request) -> dict:
        """Retrieves a snapshot"""
        snapshot = {}
        self._get_entity(req, f"snapshots/{idr}", snapshot)
        return snapshot

    def head_snapshot(self, idr: str) -> dict:
        """Retrieves metadata for a snapshot"""
        return self._head_entity(f"snapshots/{idr}/download")

    def read_snapshot(self, idr: str, cbk: Callable[[dict], Any]):
        """Reads a snapshot"""
        self._read_entity(f"snapshots/{idr}/download", cbk)

    def download_snapshot(self, idr: str, writer: io.BytesIO):
        """Downloads a snapshot"""
        self._download_entity(f"snapshots/{idr}/download", writer)

    def get_chunks(self, sid: str, req: Request) -> List[dict]:
        """Retrieves chunks"""
        chunks = []
        self._get_entity(req, f"snapshots/{sid}/chunks", chunks)
        return chunks

    def get_chunk(self, sid: str, idr: str, req: Request) -> dict:
        """Retrieves a single chunk"""
        chunk = {}
        self._get_entity(req, f"snapshots/{sid}/chunks/{idr}", chunk)
        return chunk

    def head_chunk(self, sid: str, idr: str) -> dict:
        """Retrieves a chunk's metadata"""
        return self._head_entity(f"snapshots/{sid}/chunks/{idr}/download")

    def read_chunk(self, sid: str, idr: str, cbk: Callable[[dict], Any]):
        """Reads a chunk"""
        self._read_entity(f"snapshots/{sid}/chunks/{idr}/download", cbk)

    def download_chunk(self, sid: str, idr: str, writer: io.BytesIO):
        """Downloads a chunk"""
        self._download_entity(f"snapshots/{sid}/chunks/{idr}/download", writer)

    def get_articles(self, name: str, req: Request) -> List[dict]:
        """Retrieves articles"""
        articles = []
        self._get_entity(req, f"articles/{name}", articles)
        return articles

    def get_structured_contents(self, name: str, req: Request) -> List[dict]:
        """Retrieves structured contents"""
        contents = []
        self._get_entity(req, f"structured-contents/{name}", contents)
        return contents

    def get_structured_snapshots(self, req: Request) -> List[dict]:
        """Retrieves structured snapshots"""
        structured_snapshots = []
        self._get_entity(req, "snapshots/structured-contents/", structured_snapshots)
        return structured_snapshots

    def get_structured_snapshot(self, idr: str, req: Request) -> dict:
        """Retrieves a structured snapshot"""
        structured_snapshot = {}
        self._get_entity(req, f"snapshots/structured-contents/{idr}", structured_snapshot)
        return structured_snapshot

    def head_structured_snapshot(self, idr: str) -> dict:
        """Retrieves a structured snapshot's metadata"""
        return self._head_entity(f"snapshots/structured-contents/{idr}/download")

    def read_structured_snapshot(self, idr: str, cbk: Callable[[dict], Any]):
        """Reads a structured snapshot"""
        self._read_entity(f"snapshots/structured-contents/{idr}/download", cbk)

    def download_structured_snapshot(self, idr: str, writer: io.BytesIO):
        """Downloads a structured snapshot"""
        self._download_entity(f"snapshots/structured-contents/{idr}/download", writer)

    def stream_articles(self, req: Request, cbk: Callable[[dict], Any]):
        """Streams rt articles"""
        self._subscribe_to_entity("articles", req, cbk)
