from typing import Optional
from datetime import datetime
from language import Language
from size import Size
from exceptions import DataModelError


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
        if not isinstance(data, dict):
            raise DataModelError(f"Expected a dict for Project data, but got {type(data).__name__}")
        
        try:
            date_str = data.get('date_modified')
            return Project(
                name=data.get('name'),
                identifier=data.get('identifier'),
                url=data.get('url'),
                code=data.get('code'),
                version=data.get('version'),
                date_modified=datetime.fromisoformat(date_str) if date_str else None,
                in_language=Language.from_json(lang_data) if (lang_data := data.get('in_language')) else None,
                size=Size.from_json(s_data) if (s_data := data.get('size')) else None
            )
        except (ValueError, TypeError, DataModelError) as e:
            project_name = data.get('name', 'N/A')
            raise DataModelError(f"Failed to parse Project data for '{project_name}': {e}") from e

    @staticmethod
    def to_json(project: 'Project') -> dict:
        return {
            'name': project.name,
            'identifier': project.identifier,
            'url': project.url,
            'code': project.code,
            'version': project.version,
            'date_modified': project.date_modified.isoformat() if project.date_modified else None,
            'in_language': Language.to_json(project.in_language) if project.in_language else None,
            'size': Size.to_json(project.size) if project.size else None
        }
