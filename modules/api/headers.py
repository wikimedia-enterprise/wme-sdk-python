from typing import Optional
from datetime import datetime
from exceptions import DataModelError

HTTP_DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"


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
        if not isinstance(data, dict):
            raise DataModelError(f"Expected a dict for Headers data, but got {type(data).__name__}")
        
        try:
            last_modified_str = data.get('last_modified')
            
            return Headers(
                content_length=data.get('content_length'),
                etag=data.get('etag'),
                
                last_modified=datetime.strptime(last_modified_str, HTTP_DATE_FORMAT) if last_modified_str else None,
                
                content_type=data.get('content_type'),
                accept_ranges=data.get('accept_ranges')
            )
        except (ValueError, TypeError) as e:
            raise DataModelError(f"Failed to parse Headers data: {e}") from e

    @staticmethod
    def to_json(headers: 'Headers') -> dict:
        return {
            'content_length': headers.content_length,
            'etag': headers.etag,

            'last_modified': headers.last_modified.strftime(HTTP_DATE_FORMAT) if headers.last_modified else None,
            
            'content_type': headers.content_type,
            'accept_ranges': headers.accept_ranges
        }
