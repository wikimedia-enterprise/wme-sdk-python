from typing import Optional


class Language:
    def __init__(self,
                 identifier: Optional[str] = None,
                 name: Optional[str] = None,
                 alternate_name: Optional[str] = None,
                 direction: Optional[str] = None):
        self.identifier = identifier
        self.name = name
        self.alternate_name = alternate_name
        self.direction = direction

    @staticmethod
    def from_json(data: dict) -> 'Language':
        return Language(
            identifier=data['identifier'],
            name=data['name'],
            alternate_name=data['alternate_name'],
            direction=data['direction']
        )

    @staticmethod
    def to_json(language: 'Language') -> dict:
        return {
            'identifier': language.identifier,
            'name': language.name,
            'alternate_name': language.alternate_name,
            'direction': language.direction
        }
