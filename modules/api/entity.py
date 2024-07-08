from typing import List, Optional


class Entity:
    def __init__(self,
                 identifier: Optional[str] = None,
                 url: Optional[str] = None,
                 aspects: Optional[List[str]] = None):
        self.identifier = identifier
        self.url = url
        self.aspects = aspects or []
