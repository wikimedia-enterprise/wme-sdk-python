# pylint: disable=too-few-public-methods, too-many-instance-attributes, too-many-public-methods, too-many-arguments, too-many-positional-arguments

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
import typing
import gzip
from abc import ABC, abstractmethod
from zlib_ng import gzip_ng_threaded
import httpx
from .exceptions import APIDataError, APIRequestError, APIStatusError, DataModelError
from .code import Code
from .language import Language
from .project import Project
from .namespace import Namespace
from .batch import Batch
from .snapshot import Snapshot
from .article import Article
from .structuredcontent import StructuredContent

InternalReadCallback = Callable[[dict], bool]

CodeReadCallback = Callable[[Code], bool]
LanguageReadCallback = Callable[[Language], bool]
ProjectReadCallback = Callable[[Project], bool]
NamespaceReadCallback = Callable[[Namespace], bool]
BatchReadCallback = Callable[[Batch], bool]
SnapshotReadCallback = Callable[[Snapshot], bool]
ArticleReadCallback = Callable[[Article], bool]
StructuredContentReadCallback = Callable[[StructuredContent], bool]

logger = logging.getLogger(__name__)

DATE_FORMAT = "%Y-%m-%d"
HOUR_FORMAT = "%H"

class Filter:
    """Represents a simple key-value filter for an API query."""
    def __init__(self, field: str, value: Any):
        """Initializes a Filter object.

        Args:
            field (str): The name of the field to filter on.
            value (Any): The value to filter for.
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

class _TarfileStreamWrapper:
    """
    Wraps the non-seekable file object from tarfile.extractfile()
    to make it compatible with io.TextIOWrapper, which expects
    a .seekable() method to exist.
    """
    def __init__(self, tarfile_stream: typing.IO[bytes]):
        self._stream = tarfile_stream

    @property
    def closed(self) -> bool:
        """Returns True if the underlying stream is closed, False otherwise."""
        return self._stream.closed

    def read(self, *args, **kwargs):
        """Reads and returns data from the underlying stream, passing along any arguments."""
        return self._stream.read(*args, **kwargs)

    def readable(self):
        """Returns True to indicate the stream is readable."""
        return True

    def seekable(self):
        """
        Returns False to indicate the stream is not seekable.
        This is the primary purpose of this wrapper.
        """
        return False

    def writable(self):
        """Returns False to indicate the stream is not writable."""
        return False

    def close(self):
        """Closes the underlying tarfile stream."""
        self._stream.close()

    def flush(self):
        """
        Flushes the write buffers of the underlying stream, if applicable.
        This method was missing.
        """
        self._stream.flush()

class API(ABC):
    """
    Abstract Base Class defining the contract for the Wikimedia Enterprise API client.
    This ensures all client implementations have a consistent interface.
    """
    @abstractmethod
    def set_access_token(self, token: str):
        """Updates the access token for the client instance."""

    @abstractmethod
    def get_codes(self, req: Request) -> List[Code]:
        """Retrieves codes"""

    @abstractmethod
    def get_code(self, idr: str, req: Request) -> Code:
        """Retrieves a code"""

    @abstractmethod
    def get_languages(self, req: Request) -> List[Language]:
        """Retrieves languages"""

    @abstractmethod
    def get_language(self, idr: str, req: Request) -> Language:
        """Retrieves a language"""

    @abstractmethod
    def get_projects(self, req: Request) -> List[Project]:
        """Retrieves projects"""

    @abstractmethod
    def get_project(self, idr: str, req: Request) -> Project:
        """Retrieves a project."""

    @abstractmethod
    def get_namespaces(self, req: Request) -> List[Namespace]:
        """Retrieves namespaces"""

    @abstractmethod
    def get_namespace(self, idr: int, req: Request) -> Namespace:
        """Retrieves a namespace"""

    @abstractmethod
    def get_batches(self, timestamp: datetime.datetime, req: Request) -> List[Batch]:
        """Retrieves data batches."""

    @abstractmethod
    def get_batch(self, timestamp: datetime.datetime, idr: str, req: Request) -> Batch:
        """Retrieves a single batch."""

    @abstractmethod
    def head_batch(self, timestamp: datetime.datetime, idr: str) -> dict:
        """Retrieves metadata for a specific data batch."""

    @abstractmethod
    def read_batch(self, timestamp: datetime.datetime, idr: str, cbk: BatchReadCallback):
        """Reads and processes the content of a specific data batch via a callback."""

    @abstractmethod
    def download_batch(self, timestamp: datetime.datetime, idr: str, writer: io.BytesIO):
        """Downloads a batch."""

    @abstractmethod
    def get_snapshots(self, req: Request) -> List[Snapshot]:
        """Retrieves snapshots"""

    @abstractmethod
    def get_snapshot(self, idr: str, req: Request) -> Snapshot:
        """Retrieves a single snapshot"""

    @abstractmethod
    def head_snapshot(self, idr: str) -> dict:
        """Retrieves a single head snapshot"""

    @abstractmethod
    def read_snapshot(self, idr: str, cbk: SnapshotReadCallback):
        """Reads a single snapshot"""

    @abstractmethod
    def download_snapshot(self, idr: str, writer: io.BytesIO):
        """Downloads a single snapshot"""

    @abstractmethod
    def get_chunks(self, sid: str, req: Request) -> List[Snapshot]:
        """Retrieves chunks"""

    @abstractmethod
    def get_chunk(self, sid: str, idr: str, req: Request) -> Snapshot:
        """Retrieves a chunk"""

    @abstractmethod
    def head_chunk(self, sid: str, idr: str) -> dict:
        """Retrieves a head chunk"""

    @abstractmethod
    def read_chunk(self, sid: str, idr: str, cbk: SnapshotReadCallback):
        """Reads a chunk"""

    @abstractmethod
    def download_chunk(self, sid: str, idr: str, writer: io.BytesIO):
        """Downloads a chunk"""

    @abstractmethod
    def get_articles(self, name: str, req: Request) -> List[Article]:
        """Retrieves articles"""

    @abstractmethod
    def get_structured_contents(self, name: str, req: Request) -> List[StructuredContent]:
        """Retrieves structured contents"""

    @abstractmethod
    def stream_articles(self, req: Request, cbk: ArticleReadCallback):
        """Streams articles"""

    @abstractmethod
    def read_all(self, rdr: io.BytesIO, cbk: InternalReadCallback):
        """Contains different types"""

    @abstractmethod
    def get_structured_snapshots(self, req: Request) -> List[StructuredContent]:
        """Retrieves structured content snapshots."""

    @abstractmethod
    def get_structured_snapshot(self, idr: str, req: Request) -> StructuredContent:
        """Retrieves a single structured content snapshot."""

    @abstractmethod
    def head_structured_snapshot(self, idr: str) -> dict:
        """Retrieves metadata for a structured content snapshot."""

    @abstractmethod
    def read_structured_snapshot(self, idr: str, cbk: StructuredContentReadCallback):
        """Reads a structured content snapshot."""

    @abstractmethod
    def download_structured_snapshot(self, idr: str, writer: io.BytesIO):
        """Downloads a structured content snapshot."""


class Client(API):
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
            http2=True,
            follow_redirects=True
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

        Handles rate limiting, catches httpx errors, and re-raises them as
        API-specific exceptions.

        Args:
            method (str): The HTTP method (e.g., 'GET', 'POST').
            url (str): The full URL for the request.
            **kwargs: Additional keyword arguments passed to the httpx request.

        Returns:
            The httpx.Response object.

        Raises:
            APIStatusError: If the response status code is 4xx or 5xx.
            APIRequestError: If an error occurs during the request (e.g., connection error).
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
        """
        Internal helper to fetch a JSON entity via POST and populate a container.

        Makes a POST request to the given `path` with the `req` payload.
        The JSON response is then used to update (for dicts) or extend (for lists)
        the `val` argument in-place.

        Args:
            req (Optional[Request]): The request payload object.
            path (str): The API endpoint path (e.g., "projects").
            val (Any): The list or dict object to populate with the response.

        Raises:
            APIDataError: If the JSON response is malformed or its type
                          (list/dict) does not match `val`'s type.
        """
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

    def _read_loop(self, rdr: typing.BinaryIO, cbk: InternalReadCallback):
        """
        Processes a byte stream of newline-delimited JSON (NDJSON).

        Reads from the stream line by line, decodes each line as JSON,
        and calls the callback function with the resulting object.
        Skips empty lines and logs a warning for malformed JSON.

        Args:
            rdr (io.BytesIO): A byte stream containing NDJSON data.
            cbk (Callable[[dict], Any]): A callback function to process each JSON object.
        """
        scanner = io.TextIOWrapper(rdr, encoding="utf-8")
        for line in scanner:
            if not line.strip():
                continue
            try:
                article = json.loads(line)
                if not cbk(article):
                    return False
            except json.JSONDecodeError:
                logger.warning("Skipping line due to JSON decode error", exc_info=True)

        return True

    def _read_entity(self, path: str, cbk: Callable[[dict], Any]):
        """
        Internal helper to fetch a resource and process it as NDJSON.

        Makes a GET request to the given `path` and passes the response
        content to `_read_loop` for processing.

        Args:
            path (str): The API endpoint path (e.g., "snapshots/123/download").
            cbk (Callable[[dict], Any]): A callback function to process each JSON object.
        """
        response = self._request('GET', f"{self.base_url}v2/{path}")
        self._read_loop(io.BytesIO(response.content), cbk)

    def _head_entity(self, path: str) -> dict:
        """
        Internal helper to perform a HEAD request and parse key headers.

        Makes a HEAD request to the given `path` and returns a dictionary
        of parsed headers, including a 'Content-Length' (as int) and
        a cleaned 'ETag' (quotes removed).

        Args:
            path (str): The API endpoint path.

        Returns:
            dict: A dictionary of parsed response headers.

        Raises:
            APIDataError: If 'Content-Length' header is present but not a valid integer.
        """
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
        """
        Downloads a large entity, in parallel chunks, into `writer`.

        Performs a HEAD request to get content length, then calculates chunks
        and downloads them in parallel using a ThreadPoolExecutor. If chunking
        is disabled (download_chunk_size <= 0), it downloads the file in a
        single request.

        Args:
            path (str): The API endpoint path (e.g., "snapshots/123/download").
            writer (io.BytesIO): A writable, seekable byte stream to write
                                 the downloaded content into.

        Raises:
            APIRequestError: If a download chunk fails due to a network or
                             HTTP status error.
            APIDataError: If a download chunk fails for an unexpected reason.
        """
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

    def _subscribe_to_entity(self, path: str, req: Request, cbk: InternalReadCallback):
        """
        Internal helper to connect to a real-time stream endpoint.

        Makes a streaming GET request to the given `path` on the `realtime_url`.
        It processes the incoming NDJSON stream, calling the callback for
        each valid JSON object received.

        Args:
            path (str): The API endpoint path (e.g., "articles").
            req (Request): The request payload object, typically containing filters.
            cbk (Callable[[dict], Any]): A callback function to process each JSON object.

        Raises:
            APIStatusError: If the stream connection returns a 4xx or 5xx status.
            APIRequestError: If an error occurs during the stream connection.
        """
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
                            if not cbk(article):
                                break
                        except json.JSONDecodeError:
                            logger.warning("Skipping malformed JSON line in stream: %s", line)
        except httpx.HTTPStatusError as e:
            raise APIStatusError(f"HTTP Error: {e.response.status_code} on stream", request=e.request, response=e.response) from e
        except httpx.RequestError as e:
            raise APIRequestError(f"Stream Request Error: {e}", request=e.request) from e

    def read_all(self, rdr: io.BytesIO, cbk: InternalReadCallback):
        """
        Reads a .tar.gz archive containing NDJSON files.

        Extracts each file from the given byte stream (assumed to be a .tar.gz archive),
        reads it as NDJSON, and processes each JSON object using the
        provided callback.

        Args:
            rdr (io.BytesIO): A byte stream containing the .tar.gz archive data.
            cbk (Callable[[dict], Any]): A callback function to process each JSON object
                                         from each file in the archive.

        Raises:
            APIDataError: If the archive is corrupt or cannot be read as a tarfile.
        """
        try:
            with gzip_ng_threaded.open(rdr, mode="rb", threads=-1) as decompressed_stream:

                typed_stream = typing.cast(typing.BinaryIO, decompressed_stream)

                with tarfile.open(fileobj=typed_stream, mode='r|') as tar:
                    while True:
                        member = tar.next()
                        if member is None:
                            break

                        if not member.isfile():
                            continue

                        f = tar.extractfile(member)

                        if f:
                            with f:
                                wrapped_stream = _TarfileStreamWrapper(f)
                                typed_stream = typing.cast(typing.BinaryIO, wrapped_stream)
                                if not self._read_loop(typed_stream, cbk):
                                    break
        except tarfile.TarError as e:
            raise APIDataError(f"Failed to read tar archive: {e}") from e
        except gzip.BadGzipFile as e:
            raise APIDataError(f"Failed to decompress Gzip archive: {e}") from e


    def set_access_token(self, token: str):
        """
        Updates the access token for the client instance.

        This updates both the `access_token` attribute and the
        'Authorization' header on the internal `httpx.Client`.

        Args:
            token (str): The new access token.
        """
        self.access_token = token
        self.http_client.headers['Authorization'] = f'Bearer {token}'

    def get_codes(self, req: Request) -> List[Code]:
        """Retrieves codes"""
        codes_list = []
        self._get_entity(req, "codes", codes_list)
        try:
            return[Code.from_json(c) for c in codes_list]
        except DataModelError as e:
            raise APIDataError(f"Failed to parse project list data: {e}") from e

    def get_code(self, idr: str, req: Request) -> Code:
        """Retrieves a single code"""
        code_dict = {}
        self._get_entity(req, f"codes/{idr}", code_dict)
        try:
            return Code.from_json(code_dict)
        except DataModelError as e:
            raise APIDataError(f"Failed to parse code data: {e}") from e

    def get_languages(self, req: Request) -> List[Language]:
        """Retrieves languages"""
        languages_list = []
        self._get_entity(req, "languages", languages_list)
        try:
            return[Language.from_json(l) for l in languages_list]
        except DataModelError as e:
            raise APIDataError(f"Failed to parse Language list data: {e}") from e

    def get_language(self, idr: str, req: Request) -> Language:
        """Retrieves a language"""
        language_dict = {}
        self._get_entity(req, f"languages/{idr}", language_dict)
        try:
            return Language.from_json(language_dict)
        except DataModelError as e:
            raise APIDataError(f"Failed to parse language data: {e}") from e

    def get_projects(self, req: Request) -> List[Project]:
        """Retrieves projects"""
        project_list = []
        self._get_entity(req, "projects", project_list)
        try:
            return[Project.from_json(p) for p in project_list]
        except DataModelError as e:
            raise APIDataError(f"Failed to parse Project list data: {e}") from e

    def get_project(self, idr: str, req: Request) -> Project:
        """Retrieves a project"""
        project_dict = {}
        self._get_entity(req, f"projects/{idr}", project_dict)
        try:
            return Project.from_json(project_dict)
        except DataModelError as e:
            raise APIDataError(f"Failed to parse project data: {e}") from e

    def get_namespaces(self, req: Request) -> List[Namespace]:
        """Retrieves namespaces"""
        namespaces_list = []
        self._get_entity(req, "namespaces", namespaces_list)
        try:
            return[Namespace.from_json(ns) for ns in namespaces_list]
        except DataModelError as e:
            raise APIDataError(f"Failed to parse Namespaces list data: {e}") from e

    def get_namespace(self, idr: int, req: Request) -> Namespace:
        """Retrieves a namespace"""
        namespace_dict = {}
        self._get_entity(req, f"namespaces/{idr}", namespace_dict)
        try:
            return Namespace.from_json(namespace_dict)
        except DataModelError as e:
            raise APIDataError(f"Failed to parse namespace data: {e}") from e

    def _get_batches_prefix(self, timestamp: datetime.datetime):
        return f"batches/{timestamp.strftime(DATE_FORMAT)}/{timestamp.strftime(HOUR_FORMAT)}"

    def get_batches(self, timestamp: datetime.datetime, req: Request) -> List[Batch]:
        """Retrieves data batches"""
        batches_list = []
        self._get_entity(req, self._get_batches_prefix(timestamp), batches_list)
        try:
            return[Batch.from_json(b) for b in batches_list]
        except DataModelError as e:
            raise APIDataError(f"Failed to parse Batches list data: {e}") from e

    def get_batch(self, timestamp: datetime.datetime, idr: str, req: Request) -> Batch:
        """Retrieves a single batch"""
        batch_dict = {}
        self._get_entity(req, f"{self._get_batches_prefix(timestamp)}/{idr}", batch_dict)
        try:
            return Batch.from_json(batch_dict)
        except DataModelError as e:
            raise APIDataError(f"Failed to parse batch data: {e}") from e

    def head_batch(self, timestamp: datetime.datetime, idr: str) -> dict:
        """Retrieves metadata for a specific data batch."""
        return self._head_entity(f"{self._get_batches_prefix(timestamp)}/{idr}/download")

    def read_batch(self, timestamp: datetime.datetime, idr: str, cbk: BatchReadCallback):
        """Reads and processes the content of a specific data batch via a callback."""
        def parsing_callback(data: dict) -> bool:
            try:
                batch_obj = Batch.from_json(data)
                return cbk(batch_obj)
            except DataModelError as e:
                logger.warning("Skipping batch data due to model error: %s", e)
                return True

        self._read_entity(f"b{self._get_batches_prefix(timestamp)}/{idr}/download", parsing_callback)

    def download_batch(self, timestamp: datetime.datetime, idr: str, writer: io.BytesIO):
        """Downloads a batch"""
        self._download_entity(f"{self._get_batches_prefix(timestamp)}/{idr}/download", writer)

    def get_snapshots(self, req: Request) -> List[Snapshot]:
        """Retrieves snapshots"""
        snapshot_list = []
        self._get_entity(req, "snapshots", snapshot_list)
        try:
            return[Snapshot.from_json(ss) for ss in snapshot_list]
        except DataModelError as e:
            raise APIDataError(f"Failed to parse Snapshots list data: {e}") from e

    def get_snapshot(self, idr: str, req: Request) -> Snapshot:
        """Retrieves a snapshot"""
        snapshot_dict = {}
        self._get_entity(req, f"snapshots/{idr}", snapshot_dict)
        try:
            return Snapshot.from_json(snapshot_dict)
        except DataModelError as e:
            raise APIDataError(f"Failed to parse snapshot data: {e}") from e

    def head_snapshot(self, idr: str) -> dict:
        """Retrieves metadata for a snapshot"""
        return self._head_entity(f"snapshots/{idr}/download")

    def read_snapshot(self, idr: str, cbk: SnapshotReadCallback):
        """Reads a snapshot"""
        def parsing_callback(data: dict) -> bool:
            try:
                snapshot_obj = Snapshot.from_json(data)
                return cbk(snapshot_obj)
            except DataModelError as e:
                logger.warning("Skipping snapshot data due to model error: %s", e)
                return True

        self._read_entity(f"snapshots/{idr}/download", parsing_callback)

    def download_snapshot(self, idr: str, writer: io.BytesIO):
        """Downloads a snapshot"""
        self._download_entity(f"snapshots/{idr}/download", writer)

    def get_chunks(self, sid: str, req: Request) -> List[Snapshot]:
        """Retrieves chunks"""
        chunks_list = []
        self._get_entity(req, f"snapshots/{sid}/chunks", chunks_list)
        try:
            return[Snapshot.from_json(cs) for cs in chunks_list]
        except DataModelError as e:
            raise APIDataError(f"Failed to parse Chunks list data: {e}") from e

    def get_chunk(self, sid: str, idr: str, req: Request) -> Snapshot:
        """Retrieves a single chunk"""
        chunk_dict = {}
        self._get_entity(req, f"snapshots/{sid}/chunks/{idr}", chunk_dict)
        try:
            return Snapshot.from_json(chunk_dict)
        except DataModelError as e:
            raise APIDataError(f"Failed to parse chunk data: {e}") from e

    def head_chunk(self, sid: str, idr: str) -> dict:
        """Retrieves a chunk's metadata"""
        return self._head_entity(f"snapshots/{sid}/chunks/{idr}/download")

    def read_chunk(self, sid: str, idr: str, cbk: SnapshotReadCallback):
        """Reads a chunk"""
        def parsing_callback(data: dict) -> bool:
            try:
                chunk_obj = Snapshot.from_json(data)
                return cbk(chunk_obj)
            except DataModelError as e:
                logger.warning("Skipping chunk data due to model error: %s", e)
                return True
        self._read_entity(f"snapshots/{sid}/chunks/{idr}/download", parsing_callback)

    def download_chunk(self, sid: str, idr: str, writer: io.BytesIO):
        """Downloads a chunk"""
        self._download_entity(f"snapshots/{sid}/chunks/{idr}/download", writer)

    def get_articles(self, name: str, req: Request) -> List[Article]:
        """Retrieves articles"""
        articles_list = []
        self._get_entity(req, f"articles/{name}", articles_list)
        try:
            return[Article.from_json(a) for a in articles_list]
        except DataModelError as e:
            raise APIDataError(f"Failed to parse Articles list data: {e}") from e

    def get_structured_contents(self, name: str, req: Request) -> List[StructuredContent]:
        """Retrieves structured contents"""
        contents_list = []
        self._get_entity(req, f"structured-contents/{name}", contents_list)
        try:
            return[StructuredContent.from_json(sc) for sc in contents_list]
        except DataModelError as e:
            raise APIDataError(f"Failed to parse Structured Contents list data: {e}") from e

    def get_structured_snapshots(self, req: Request) -> List[StructuredContent]:
        """Retrieves structured snapshots"""
        snapshots_list = []
        self._get_entity(req, "snapshots/structured-contents/", snapshots_list)
        try:
            return [StructuredContent.from_json(s) for s in snapshots_list]
        except DataModelError as e:
            raise APIDataError(f"Failed to parse structured snapshot list data: {e}") from e

    def get_structured_snapshot(self, idr: str, req: Request) -> StructuredContent:
        """Retrieves a structured snapshot"""
        snapshot_dict = {}
        self._get_entity(req, f"snapshots/structured-contents/{idr}", snapshot_dict)
        try:
            return StructuredContent.from_json(snapshot_dict)
        except DataModelError as e:
            raise APIDataError(f"Failed to parse structured snapshot data: {e}") from e

    def head_structured_snapshot(self, idr: str) -> dict:
        """Retrieves a structured snapshot's metadata"""
        return self._head_entity(f"snapshots/structured-contents/{idr}/download")

    def read_structured_snapshot(self, idr: str, cbk: StructuredContentReadCallback):
        """Reads a structured snapshot"""

        def parsing_callback(data: dict) -> bool:
            try:
                snapshot_obj = StructuredContent.from_json(data)
                return cbk(snapshot_obj)
            except DataModelError as e:
                logger.warning("Skipping structured snapshot data due to model error: %s", e)
                return True

        self._read_entity(f"snapshots/structured-contents/{idr}/download", parsing_callback)

    def download_structured_snapshot(self, idr: str, writer: io.BytesIO):
        """Downloads a structured snapshot"""
        self._download_entity(f"snapshots/structured-contents/{idr}/download", writer)

    def stream_articles(self, req: Request, cbk: ArticleReadCallback):
        """Streams rt articles"""
        def parsing_callback(data: dict) -> bool:
            try:
                article_obj = Article.from_json(data)
                return cbk(article_obj)
            except DataModelError as e:
                logger.warning("Skipping article stream data due to model error: %s", e)
                return True

        self._subscribe_to_entity("articles", req, parsing_callback)
