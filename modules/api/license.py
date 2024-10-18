from typing import Optional


class License:
    def __init__(self,
                 name: Optional[str] = None,
                 identifier: Optional[str] = None,
                 url: Optional[str] = None):
        self.name = name
        self.identifier = identifier
        self.url = url

    @staticmethod
    def from_json(data: dict) -> 'License':
        return License(
            name=data['name'],
            identifier=data['identifier'],
            url=data['url']
        )

    @staticmethod
    def to_json(license: 'License') -> dict:
        return {
            'name': license.name,
            'identifier': license.identifier,
            'url': license.url
        }
