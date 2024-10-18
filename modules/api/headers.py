from typing import Optional
from datetime import datetime


class Headers:
    def __init__(self,
                 content_length: Optional[int] = None,
                 etag: Optional[str] = None,
                 last_modified: Optional[datetime] = None,
                 content_type: Optional[str] = None,
                 accept_ranges: Optional[str] = None):
        self.content_length = content_length
        self.etag = etag
        self.last_modified = last_modified
        self.content_type = content_type
        self.accept_ranges = accept_ranges

    @staticmethod
    def from_json(data: dict) -> 'Headers':
        return Headers(
            content_length=data['content-length'],
            etag=data['etag'],
            last_modified=datetime.fromisoformat(data['last-modified']),
            content_type=data['content-type'],
            accept_ranges=data['accept-ranges']
        )

    @staticmethod
    def to_json(headers: 'Headers') -> dict:
        return {
            'content-length': headers.content_length,
            'etag': headers.etag,
            'last-modified': headers.last_modified.isoformat(),
            'content-type': headers.content_type,
            'accept-ranges': headers.accept_ranges
        }
