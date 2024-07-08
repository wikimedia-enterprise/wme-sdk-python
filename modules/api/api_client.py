import tarfile
import json
import requests
import io
import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Any, List, Optional, Dict


DATE_FORMAT = "%Y-%m-%d"


class Filter:
    def __init__(self, field: str, value: Any):
        self.field = field
        self.value = value


class Request:
    def __init__(self,
                 since: Optional[datetime.datetime] = None,
                 fields: Optional[List[str]] = None,
                 filters: Optional[List[Filter]] = None,
                 limit: Optional[int] = None,
                 parts: Optional[List[int]] = None,
                 offsets: Optional[Dict[int, int]] = None,
                 since_per_partition: Optional[Dict[int, datetime.datetime]] = None):
        self.since = since
        self.fields = fields or []
        self.filters = filters or []
        self.limit = limit
        self.parts = parts or []
        self.offsets = offsets or {}
        self.since_per_partition = since_per_partition or {}


class Client:
    def __init__(self, **kwargs):
        self.http_client = requests.Session()
        self.user_agent = kwargs.get('user_agent', "")
        self.base_url = kwargs.get('base_url', "https://api.enterprise.wikimedia.com/")
        self.realtime_url = kwargs.get('realtime_url', "https://realtime.enterprise.wikimedia.com/")
        self.access_token = kwargs.get('access_token', "")
        self.download_min_chunk_size = kwargs.get('download_min_chunk_size', 5242880)
        self.download_chunk_size = kwargs.get('download_chunk_size', 5242880 * 5)
        self.download_concurrency = kwargs.get('download_concurrency', 10)
        self.scanner_buffer_size = kwargs.get('scanner_buffer_size', 20971520)

    def _new_request(self, url: str, method: str, path: str, req: Optional[Request]) -> requests.Request:
        data = json.dumps(req.__dict__) if req else ''
        headers = {
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        return requests.Request(method, f"{url}v2/{path}", data=data, headers=headers)

    def _do(self, req: requests.Request) -> requests.Response:
        prepared = self.http_client.prepare_request(req)
        response = self.http_client.send(prepared)
        response.raise_for_status()
        return response

    def _get_entity(self, req: Optional[Request], path: str, val: Any):
        request = self._new_request(self.base_url, 'POST', path, req)
        response = self._do(request)
        val.update(response.json())

    def _read_loop(self, rdr: io.BytesIO, cbk: Callable[[dict], Any]):
        scanner = io.TextIOWrapper(rdr, buffer_size=self.scanner_buffer_size)
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
        chunk_size = min(self.download_chunk_size, content_length)
        chunks = [(i, min(i + chunk_size, content_length)) for i in range(0, content_length, chunk_size)]

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
        request = self._new_request(self.realtime_url, 'GET', path, req)
        request.headers.update({
            'Cache-Control': 'no-cache',
            'Accept': 'application/x-ndjson',
            'Connection': 'keep-alive'
        })
        response = self._do(request)
        self._read_loop(io.BytesIO(response.content), cbk)

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

    def get_batches(self, date: datetime.datetime, req: Request) -> List[dict]:
        batches = []
        self._get_entity(req, f"batches/{date.strftime(DATE_FORMAT)}", batches)
        return batches

    def get_batch(self, date: datetime.datetime, idr: str, req: Request) -> dict:
        batch = {}
        self._get_entity(req, f"batches/{date.strftime(DATE_FORMAT)}/{idr}", batch)
        return batch

    def head_batch(self, date: datetime.datetime, idr: str) -> dict:
        return self._head_entity(f"batches/{date.strftime(DATE_FORMAT)}/{idr}/download")

    def read_batch(self, date: datetime.datetime, idr: str, cbk: Callable[[dict], Any]):
        self._read_entity(f"batches/{date.strftime(DATE_FORMAT)}/{idr}/download", cbk)

    def download_batch(self, date: datetime.datetime, idr: str, writer: io.BytesIO):
        self._download_entity(f"batches/{date.strftime(DATE_FORMAT)}/{idr}/download", writer)

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

    def get_articles(self, name: str, req: Request) -> List[dict]:
        articles = []
        self._get_entity(req, f"articles/{name}", articles)
        return articles

    def get_structured_contents(self, name: str, req: Request) -> List[dict]:
        contents = []
        self._get_entity(req, f"structured-contents/{name}", contents)
        return contents

    def stream_articles(self, req: Request, cbk: Callable[[dict], Any]):
        self._subscribe_to_entity("articles", req, cbk)
