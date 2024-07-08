from typing import Optional
from datetime import datetime
from language import Language
from size import Size


class Project:
    def __init__(self,
                 name: Optional[str] = None,
                 identifier: Optional[str] = None,
                 url: Optional[str] = None,
                 code: Optional[str] = None,
                 version: Optional[str] = None,
                 date_modified: Optional[datetime] = None,
                 in_language: Optional[Language] = None,
                 size: Optional[Size] = None):
        self.name = name
        self.identifier = identifier
        self.url = url
        self.code = code
        self.version = version
        self.date_modified = date_modified
        self.in_language = in_language
        self.size = size
