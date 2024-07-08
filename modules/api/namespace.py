from typing import Optional


class Namespace:
    def __init__(self,
                 name: Optional[str] = None,
                 identifier: Optional[int] = None,
                 description: Optional[str] = None):
        self.name = name
        self.identifier = identifier
        self.description = description
