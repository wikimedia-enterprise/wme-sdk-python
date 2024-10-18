from typing import Optional
from datetime import datetime
from project import Project
from language import Language
from namespace import Namespace
from size import Size


class Batch:
    def __init__(self,
                 identifier: Optional[str] = None,
                 version: Optional[str] = None,
                 date_modified: Optional[datetime] = None,
                 is_part_of: Optional[Project] = None,
                 in_language: Optional[Language] = None,
                 namespace: Optional[Namespace] = None,
                 size: Optional[Size] = None):
        self.identifier = identifier
        self.version = version
        self.date_modified = date_modified
        self.is_part_of = is_part_of
        self.in_language = in_language
        self.namespace = namespace
        self.size = size

    @staticmethod
    def from_json(data: dict) -> 'Batch':
        return Batch(
            identifier=data['identifier'],
            version=data['version'],
            date_modified=datetime.fromisoformat(data['dateModified']),
            is_part_of=Project.from_json(data['isPartOf']),
            in_language=Language.from_json(data['inLanguage']),
            namespace=Namespace.from_json(data['namespace']),
            size=Size.from_json(data['size'])
        )

    @staticmethod
    def to_json(batch: 'Batch') -> dict:
        return {
            'identifier': batch.identifier,
            'version': batch.version,
            'dateModified': batch.date_modified.isoformat(),
            'isPartOf': Project.to_json(batch.is_part_of),
            'inLanguage': Language.to_json(batch.in_language),
            'namespace': Namespace.to_json(batch.namespace),
            'size': Size.to_json(batch.size)
        }
