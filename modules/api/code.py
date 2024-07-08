from typing import Optional


class Code:
    def __init__(self,
                 identifier: Optional[str] = None,
                 name: Optional[str] = None,
                 description: Optional[str] = None):
        self.identifier = identifier
        self.name = name
        self.description = description
