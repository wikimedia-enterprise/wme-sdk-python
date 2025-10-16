"""Retrieves a namespace's data"""

from typing import Optional
from .exceptions import DataModelError


class Namespace:
    """Represents a content namespace"""
    def __init__(self,
                 name: Optional[str] = None,
                 identifier: Optional[int] = None,
                 description: Optional[str] = None):
        self.name = name
        self.identifier = identifier
        self.description = description

    @staticmethod
    def from_json(data: dict) -> 'Namespace':
        """Constructs a Namespace object from a dictionary representation."""
        if not isinstance(data, dict):
            raise DataModelError(f"Expected a dict for Namespace data, but got {type(data).__name__}")

        try:
            return Namespace(
                name=data.get('name'),
                identifier=data.get('identifier'),
                description=data.get('description')
            )
        except (KeyError, TypeError) as e:
            ns_name = data.get('name', 'N/A')
            raise DataModelError(f"Failed to parse Namespace data for '{ns_name}': {e}") from e

    @staticmethod
    def to_json(namespace: 'Namespace') -> dict:
        """Converts a Namespace instance into a dictionary for JSON serialization."""
        return {
            'name': namespace.name,
            'identifier': namespace.identifier,
            'description': namespace.description
        }
