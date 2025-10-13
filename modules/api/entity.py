from typing import List, Optional
from exceptions import DataModelError


class Entity:
    def __init__(self,
                 identifier: Optional[str] = None,
                 url: Optional[str] = None,
                 aspects: Optional[List[str]] = None):
        self.identifier = identifier
        self.url = url
        self.aspects = aspects or []

    @staticmethod
    def from_json(data: dict) -> 'Entity':
        """Creates an Entity instance from a dictionary (JSON object)"""
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
        """Converts an Entity instance to a dictionary for JSON serialization"""
        return {
            'identifier': entity.identifier,
            'url': entity.url,
            'aspects': entity.aspects
        }
