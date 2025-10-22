"""Retrieves a namespace's data"""

from typing import Optional
from .exceptions import DataModelError


class Namespace:
    """Holds metadata for a Wikimedia content namespace (e.g., 'Article', 'Talk')."""
    def __init__(self,
                 name: Optional[str] = None,
                 identifier: Optional[int] = None,
                 description: Optional[str] = None):
        self.name = name
        self.identifier = identifier
        self.description = description

    @staticmethod
    def from_json(data: dict) -> 'Namespace':
        """
        Deserializes a dictionary into a Namespace instance.

        Args:
            data: A dictionary containing the namespace's data.

        Returns:
            A Namespace instance.

        Raises:
            DataModelError: If the input is not a dict or if parsing fails.
        """
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
        """
        Serializes the Namespace instance into a JSON-compatible dictionary.

        Args:
            namespace: The Namespace instance to serialize.

        Returns:
            A dictionary representation of the namespace.
        """
        return {
            'name': namespace.name,
            'identifier': namespace.identifier,
            'description': namespace.description
        }
