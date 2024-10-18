from typing import Optional


class Namespace:
    def __init__(self,
                 name: Optional[str] = None,
                 identifier: Optional[int] = None,
                 description: Optional[str] = None):
        self.name = name
        self.identifier = identifier
        self.description = description

    @staticmethod
    def from_json(data: dict) -> 'Namespace':
        return Namespace(
            name=data['name'],
            identifier=data['identifier'],
            description=data['description']
        )

    @staticmethod
    def to_json(namespace: 'Namespace') -> dict:
        return {
            'name': namespace.name,
            'identifier': namespace.identifier,
            'description': namespace.description
        }
