from typing import Optional


class Protection:
    def __init__(self,
                 protection_type: Optional[str] = None,
                 level: Optional[str] = None,
                 expiry: Optional[str] = None):
        self.protection_type = protection_type
        self.level = level
        self.expiry = expiry
