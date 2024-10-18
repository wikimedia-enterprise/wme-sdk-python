from typing import Optional


class Protection:
    def __init__(self,
                 protection_type: Optional[str] = None,
                 level: Optional[str] = None,
                 expiry: Optional[str] = None):
        self.protection_type = protection_type
        self.level = level
        self.expiry = expiry

    @staticmethod
    def from_json(data: dict) -> 'Protection':
        return Protection(
            protection_type=data['type'],
            level=data['level'],
            expiry=data['expiry']
        )

    @staticmethod
    def to_json(protection: 'Protection') -> dict:
        return {
            'type': protection.protection_type,
            'level': protection.level,
            'expiry': protection.expiry
        }
