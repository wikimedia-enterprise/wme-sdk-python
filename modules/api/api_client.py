import tarfile
import json
import requests
import io
import datetime
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Any, List, Optional, Dict, Union
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


DATE_FORMAT = "%Y-%m-%d"
HOUR_FORMAT = "%H"


class Filter:
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value

    def to_dict(self):
        return {
            'field': self.field,
            'value': self.value
        }


class Request:
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
        # Build the dictionary without any empty or None values
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
    def __init__(self,
                 user_agent: Optional[str] = None,
                 #Adding parameters for timeouts, retries, and rate limits
                 timeout: float = 30.0,
                 max_retries: int = 3,
                 backoff_factor: float = 0.5,
                 rate_limit_per_second: Optional[float] = None,
                 **kwargs):
        """
        Initializes the API Client.

        Args:
            user_agent (Optional[str], optional): A custom User-Agent string for requests. 
                                                  If None, a default is used. Defaults to None.
            **kwargs: Other optional settings like 'base_url', 'realtime_url', etc.
            
        Should a user want to use a custom user agent, they could do something like this:
        custom_ua = "MyDataApp/2.5 (contact@myapp.com)"
        client2 = WikimediaClient(access_token="TOKEN_ABC", user_agent=custom_ua)
        """
        
        self.access_token = kwargs.get('access_token', "")
        
        # Use the provided user_agent or fall back to a default.
        self.user_agent = user_agent or "WME Python SDK"
        
        #Store resilencie configuration
        self.timeout = timeout
        self.rate_limit_period = 1.0 / rate_limit_per_second if rate_limit_per_second else 0
        self.last_request_time = 0
        
        #configure HTTP session with retry logic
        self.http_client = requests.Session()
        
        #retry strategy
        retry_strategy = Retry(
            total = max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[500, 502, 503, 504], #only re-try on server-side errors
            allowed_methods=["HEAD", "GET", "POST"]
        )
        
        #Adapter with this strategy and mount it to the session
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.http_client.mount("https://", adapter)
        self.http_client.mount("http://", adapter)
        
        # The rest of the settings can still be pulled from kwargs for flexibility.
        self.base_url = kwargs.get('base_url', "https://api.enterprise.wikimedia.com/")
        self.realtime_url = kwargs.get('realtime_url', "https://realtime.enterprise.wikimedia.com/")
        self.download_chunk_size = kwargs.get('download_chunk_size', -1)
        self.download_concurrency = kwargs.get('download_concurrency', 10)
        self.scanner_buffer_size = kwargs.get('scanner_buffer_size', 20971520)
        
    #Helper method for rate limiting
    def _rate_limit_wait(self):
        if self.rate_limit_period == 0:
            return
            
        elapsed = time.monotonic() - self.last_request_time
        wait_time = self.rate_limit_period - elapsed
        if wait_time > 0:
            time.sleep(wait_time)
                
        self.last_request_time = time.monotonic()

        
    def _new_request(self, url: str, method: str, path: str, req: Optional[Request]) -> requests.Request:
        data = json.dumps(req.to_json()) if req else ''
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        })
        return requests.Request(method, f"{url}v2/{path}", data=data, headers=headers)

    def _do(self, req: requests.Request) -> requests.Response:
        self._rate_limit_wait()
        
        prepared = self.http_client.prepare_request(req)
        
        #The http_client is now configured with retries, so we add the timeout
        response = self.http_client.send(
            prepared,
            timeout=self.timeout
        )
        
        response.raise_for_status()
        return response

    def _get_entity(self, req: Optional[Request], path: str, val: Any):
        request = self._new_request(self.base_url, 'POST', path, req)
        response = self._do(request)
        json_response = response.json()

        if isinstance(val, list) and isinstance(json_response, list):
            val.extend(json_response)  # If both are lists
        elif isinstance(val, dict) and isinstance(json_response, dict):
            val.update(json_response)  # If both are dicts
        else:
            raise TypeError("Incompatible types for val and json_response")

    def _read_loop(self, rdr: io.BytesIO, cbk: Callable[[dict], Any]):
        scanner = io.TextIOWrapper(rdr)
        for line in scanner:
            article = json.loads(line)
            cbk(article)

    def _read_entity(self, path: str, cbk: Callable[[dict], Any]):
        request = self._new_request(self.base_url, 'GET', path, None)
        response = self._do(request)
        self._read_loop(io.BytesIO(response.content), cbk)

    def _head_entity(self, path: str) -> dict:
        request = self._new_request(self.base_url, 'HEAD', path, None)
        response = self._do(request)
        headers = {
            'ETag': response.headers.get('ETag', '').strip('"'),
            'Content-Type': response.headers.get('Content-Type', ''),
            'Accept-Ranges': response.headers.get('Accept-Ranges', ''),
            'Last-Modified': response.headers.get('Last-Modified', ''),
            'Content-Length': int(response.headers.get('Content-Length', 0))
        }
        return headers

    def _download_entity(self, path: str, writer: io.BytesIO):
        headers = self._head_entity(path)
        content_length = headers['Content-Length']
        if self.download_chunk_size > 0:
            chunk_size = min(self.download_chunk_size, content_length)
            chunks = [(i, min(i + chunk_size, content_length)) for i in range(0, content_length, chunk_size)]
        else:
            chunks = [(0, content_length)]

        def download_chunk(start, end):
            req = self._new_request(self.base_url, 'GET', path, None)
            req.headers['Range'] = f"bytes={start}-{end}"
            res = self._do(req)
            writer.seek(start)
            writer.write(res.content)

        with ThreadPoolExecutor(max_workers=self.download_concurrency) as executor:
            futures = [executor.submit(download_chunk, start, end) for start, end in chunks]
            for future in futures:
                future.result()

    def _subscribe_to_entity(self, path: str, req: Request, cbk: Callable[[dict], Any]):
        data = json.dumps(req.to_json()) if req else ''
        headers = {
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
            'Cache-Control': 'no-cache',
            'Accept': 'application/x-ndjson',
            'Connection': 'keep-alive'
        }

        response = self.http_client.get(f"{self.realtime_url}v2/{path}", data=data, headers=headers, stream=True)

        for line in response.iter_lines():
            article = json.loads(line)
            cbk(article)

    def read_all(self, rdr: io.BytesIO, cbk: Callable[[dict], Any]):
        with tarfile.open(fileobj=rdr, mode='r:gz') as tar:
            for member in tar.getmembers():
                f = tar.extractfile(member)
                if f:
                    self._read_loop(io.BytesIO(f.read()), cbk)

    def set_access_token(self, token: str):
        self.access_token = token

    def get_codes(self, req: Request) -> List[dict]:
        codes = []
        self._get_entity(req, "codes", codes)
        return codes

    def get_code(self, idr: str, req: Request) -> dict:
        code = {}
        self._get_entity(req, f"codes/{idr}", code)
        return code

    def get_languages(self, req: Request) -> List[dict]:
        languages = []
        self._get_entity(req, "languages", languages)
        return languages

    def get_language(self, idr: str, req: Request) -> dict:
        language = {}
        self._get_entity(req, f"languages/{idr}", language)
        return language

    def get_projects(self, req: Request) -> List[dict]:
        projects = []
        self._get_entity(req, "projects", projects)
        return projects

    def get_project(self, idr: str, req: Request) -> dict:
        project = {}
        self._get_entity(req, f"projects/{idr}", project)
        return project

    def get_namespaces(self, req: Request) -> List[dict]:
        namespaces = []
        self._get_entity(req, "namespaces", namespaces)
        return namespaces

    def get_namespace(self, idr: int, req: Request) -> dict:
        namespace = {}
        self._get_entity(req, f"namespaces/{idr}", namespace)
        return namespace

    def _get_batches_prefix(self, time: datetime.datetime):
        return f"batches/{time.strftime(DATE_FORMAT)}/{time.strftime(HOUR_FORMAT)}"

    def get_batches(self, time: datetime.datetime, req: Request) -> List[dict]:
        batches = []
        self._get_entity(req, self._get_batches_prefix(time), batches)
        return batches

    def get_batch(self, time: datetime.datetime, idr: str, req: Request) -> dict:
        batch = {}
        self._get_entity(req, f"{self._get_batches_prefix(time)}/{idr}", batch)
        return batch

    def head_batch(self, time: datetime.datetime, idr: str) -> dict:
        return self._head_entity(f"{self._get_batches_prefix(time)}/{idr}/download")

    def read_batch(self, time: datetime.datetime, idr: str, cbk: Callable[[dict], Any]):
        self._read_entity(f"b{self._get_batches_prefix(time)}/{idr}/download", cbk)

    def download_batch(self, time: datetime.datetime, idr: str, writer: io.BytesIO):
        self._download_entity(f"{self._get_batches_prefix(time)}/{idr}/download", writer)

    def get_snapshots(self, req: Request) -> List[dict]:
        snapshots = []
        self._get_entity(req, "snapshots", snapshots)
        return snapshots

    def get_snapshot(self, idr: str, req: Request) -> dict:
        snapshot = {}
        self._get_entity(req, f"snapshots/{idr}", snapshot)
        return snapshot

    def head_snapshot(self, idr: str) -> dict:
        return self._head_entity(f"snapshots/{idr}/download")

    def read_snapshot(self, idr: str, cbk: Callable[[dict], Any]):
        self._read_entity(f"snapshots/{idr}/download", cbk)

    def download_snapshot(self, idr: str, writer: io.BytesIO):
        self._download_entity(f"snapshots/{idr}/download", writer)

    def get_chunks(self, sid: str, req: Request) -> List[dict]:
        chunks = []
        self._get_entity(req, f"snapshots/{sid}/chunks", chunks)
        return chunks

    def get_chunk(self, sid: str, idr: str, req: Request) -> dict:
        chunk = {}
        self._get_entity(req, f"snapshots/{sid}/chunks/{idr}", chunk)
        return chunk

    def head_chunk(self, sid: str, idr: str) -> dict:
        return self._head_entity(f"snapshots/{sid}/chunks/{idr}/download")

    def read_chunk(self, sid: str, idr: str, cbk: Callable[[dict], Any]):
        self._read_entity(f"snapshots/{sid}/chunks/{idr}/download", cbk)

    def download_chunk(self, sid: str, idr: str, writer: io.BytesIO):
        self._download_entity(f"snapshots/{sid}/chunks/{idr}/download", writer)

    def get_articles(self, name: str, req: Request) -> List[dict]:
        articles = []
        self._get_entity(req, f"articles/{name}", articles)
        return articles

    def get_structured_contents(self, name: str, req: Request) -> List[dict]:
        contents = []
        self._get_entity(req, f"structured-contents/{name}", contents)
        return contents

    def get_structured_snapshots(self, req: Request) -> List[dict]:
        """Get a list of structured content snapshots."""
        structured_snapshots = []
        self._get_entity(req, "snapshots/structured-contents/", structured_snapshots)
        return structured_snapshots

    def get_structured_snapshot(self, idr: str, req: Request) -> dict:
        structured_snapshot = {}
        self._get_entity(req, f"snapshots/structured-contents/{idr}", structured_snapshot)
        return structured_snapshot

    def head_structured_snapshot(self, idr: str) -> dict:
        return self._head_entity(f"snapshots/structured-contents/{idr}/download")

    def read_structured_snapshot(self, idr: str, cbk: Callable[[dict], Any]):
        self._read_entity(f"snapshots/structured-contents/{idr}/download", cbk)

    def download_structured_snapshot(self, idr: str, writer: io.BytesIO):
        self._download_entity(f"snapshots/structured-contents/{idr}/download", writer)

    def stream_articles(self, req: Request, cbk: Callable[[dict], Any]):
        self._subscribe_to_entity("articles", req, cbk)