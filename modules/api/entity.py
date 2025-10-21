"""Represents a wikidata entity"""

from typing import List, Optional
from .exceptions import DataModelError


class Entity:
    """Represents a wikidata entity's metadata"""
    def __init__(self,
                 identifier: Optional[str] = None,
                 url: Optional[str] = None,
                 aspects: Optional[List[str]] = None):
        self.identifier = identifier
        self.url = url
        self.aspects = aspects or []

    @staticmethod
    def from_json(data: dict) -> 'Entity':
        """
        Deserializes a dictionary into an Entity instance.

        Args:
            data: A dictionary containing the entity's data.

        Returns:
            An Entity instance.

        Raises:
            DataModelError: If the input is not a dict or if parsing fails.
        """
        if not isinstance(data, dict):
            raise DataModelError(f"Expected a dict for Entity data, but got {type(data).__name__}")
        try:
            return Entity(
                identifier=data.get('identifier'),
                url=data.get('url'),
                aspects=data.get('aspects')
            )
        except (ValueError, TypeError) as e:
            entity_id = data.get('identifier', 'N/A')
            raise DataModelError(f"Failed to parse Entity with identifier '{entity_id}': {e}") from e

    @staticmethod
    def to_json(entity: 'Entity') -> dict:
        """
        Serializes the Entity instance into a JSON-compatible dictionary.

        Args:
            entity: The Entity instance to serialize.

        Returns:
            A dictionary representation of the entity.
        """
        return {
            'identifier': entity.identifier,
            'url': entity.url,
            'aspects': entity.aspects
        }
