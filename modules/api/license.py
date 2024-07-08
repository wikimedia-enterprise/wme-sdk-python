from typing import Optional


class License:
    def __init__(self,
                 name: Optional[str] = None,
                 identifier: Optional[str] = None,
                 url: Optional[str] = None):
        self.name = name
        self.identifier = identifier
        self.url = url
