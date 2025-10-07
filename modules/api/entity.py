from typing import List, Optional


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
            return Entity()
        return Entity(
            identifier=data.get('identifier'),
            url=data.get('url'),
            aspects=data.get('aspects')
        )
    @staticmethod
    def to_json(entity: 'Entity') -> dict:
        """Converts an Entity instance to a dictionary for JSON serialization"""
        return {
            'identifier': entity.identifier,
            'url': entity.url,
            'aspects': entity.aspects
        }
