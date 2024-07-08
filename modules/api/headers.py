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
