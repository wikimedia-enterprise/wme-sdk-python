"""Retrieves license data"""

from typing import Optional
from .exceptions import DataModelError


class License:
    """Retrieves license data"""
    def __init__(self,
                 name: Optional[str] = None,
                 identifier: Optional[str] = None,
                 url: Optional[str] = None):
        self.name = name
        self.identifier = identifier
        self.url = url

    @staticmethod
    def from_json(data: dict) -> 'License':
        """
        Deserializes a dictionary into a License instance.

        Args:
            data: A dictionary containing the license's data.

        Returns:
            A License instance.

        Raises:
            DataModelError: If the input is not a dict or if parsing fails.
        """
        if not isinstance(data, dict):
            raise DataModelError(f"Expected a dict for License data, but got {type(data).__name__}")

        try:
            return License(
                name=data.get('name'),
                identifier=data.get('identifier'),
                url=data.get('url')
            )
        except (KeyError, TypeError) as e:
            license_name = data.get('name', 'N/A')
            raise DataModelError(f"Failed to parse License data for '{license_name}': {e}") from e

    @staticmethod
    def to_json(licenses: 'License') -> dict:
        """
        Serializes the License instance into a JSON-compatible dictionary.

        Args:
            licenses: The License instance to serialize.

        Returns:
            A dictionary representation of the license.
        """
        return {
            'name': licenses.name,
            'identifier': licenses.identifier,
            'url': licenses.url
        }
