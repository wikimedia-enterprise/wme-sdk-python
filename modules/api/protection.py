"""Represents a protection level's data"""

from typing import Optional
from .exceptions import DataModelError


class Protection:
    """Represents a protection level applied to a resource, like an article."""
    def __init__(self,
                 protection_type: Optional[str] = None,
                 level: Optional[str] = None,
                 expiry: Optional[str] = None):
        self.protection_type = protection_type
        self.level = level
        self.expiry = expiry

    @staticmethod
    def from_json(data: dict) -> 'Protection':
        """
        Deserializes a dictionary into a Protection instance.

        Args:
            data: A dictionary containing the protection data (type, level, expiry).

        Returns:
            A Protection instance.

        Raises:
            DataModelError: If the input is not a dict or if parsing fails.
        """
        if not isinstance(data, dict):
            raise DataModelError(f"Expected a dict for Protection data, but got {type(data).__name__}")

        try:
            return Protection(
                protection_type=data.get('type'),
                level=data.get('level'),
                expiry=data.get('expiry')
            )
        except (KeyError, TypeError) as e:
            prot_type = data.get('type', 'N/A')
            raise DataModelError(f"Failed to parse Protection data for type '{prot_type}': {e}") from e

    @staticmethod
    def to_json(protection: 'Protection') -> dict:
        """
        Serializes the Protection instance into a JSON-compatible dictionary.

        Args:
            protection: The Protection instance to serialize.

        Returns:
            A dictionary representation of the protection level.
        """
        return {
            'type': protection.protection_type,
            'level': protection.level,
            'expiry': protection.expiry
        }
