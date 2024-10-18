from typing import Optional
from datetime import datetime
from language import Language
from size import Size


class Project:
    def __init__(self,
                 name: Optional[str] = None,
                 identifier: Optional[str] = None,
                 url: Optional[str] = None,
                 code: Optional[str] = None,
                 version: Optional[str] = None,
                 date_modified: Optional[datetime] = None,
                 in_language: Optional[Language] = None,
                 size: Optional[Size] = None):
        self.name = name
        self.identifier = identifier
        self.url = url
        self.code = code
        self.version = version
        self.date_modified = date_modified
        self.in_language = in_language
        self.size = size

    @staticmethod
    def from_json(data: dict) -> 'Project':
        return Project(
            name=data['name'],
            identifier=data['identifier'],
            url=data['url'],
            code=data['code'],
            version=data['version'],
            date_modified=datetime.fromisoformat(data['dateModified']),
            in_language=Language.from_json(data['inLanguage']),
            size=Size.from_json(data['size'])
        )

    @staticmethod
    def to_json(project: 'Project') -> dict:
        return {
            'name': project.name,
            'identifier': project.identifier,
            'url': project.url,
            'code': project.code,
            'version': project.version,
            'dateModified': project.date_modified.isoformat(),
            'inLanguage': Language.to_json(project.in_language),
            'size': Size.to_json(project.size)
        }
