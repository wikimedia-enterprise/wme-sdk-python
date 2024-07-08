from typing import Optional


class Language:
    def __init__(self,
                 identifier: Optional[str] = None,
                 name: Optional[str] = None,
                 alternate_name: Optional[str] = None,
                 direction: Optional[str] = None):
        self.identifier = identifier
        self.name = name
        self.alternate_name = alternate_name
        self.direction = direction
