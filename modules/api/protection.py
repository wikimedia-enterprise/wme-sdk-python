from typing import Optional
from exceptions import DataModelError


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
        if not isinstance(data, dict):
            raise DataModelError(f"Expected a dict for Protection data, but got {type(data).__name__}")
        
        try:
            return Protection(
                protection_type=data['type'],
                level=data['level'],
                expiry=data['expiry']
            )
        except (KeyError, TypeError) as e:
            prot_type = data.get('type', 'N/A')
            raise DataModelError(f"Failed to parse Protection data for type '{prot_type}': {e}") from e

    @staticmethod
    def to_json(protection: 'Protection') -> dict:
        return {
            'type': protection.protection_type,
            'level': protection.level,
            'expiry': protection.expiry
        }
