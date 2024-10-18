from typing import Optional


class Code:
    def __init__(self,
                 identifier: Optional[str] = None,
                 name: Optional[str] = None,
                 description: Optional[str] = None):
        self.identifier = identifier
        self.name = name
        self.description = description

    @staticmethod
    def from_json(data: dict) -> 'Code':
        return Code(
            identifier=data['identifier'],
            name=data['name'],
            description=data['description']
        )

    @staticmethod
    def to_json(code: 'Code') -> dict:
        return {
            'identifier': code.identifier,
            'name': code.name,
            'description': code.description
        }
