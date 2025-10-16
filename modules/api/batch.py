"""Defines a batch"""

from typing import Optional
from datetime import datetime
from .project import Project
from .language import Language
from .namespace import Namespace
from .size import Size
from .exceptions import DataModelError


class Batch:
    """Represents metadata for a batch."""
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
        """Safely creates a Batch instance from a dictionary, handling potential errors."""
        if not isinstance(data, dict):
            raise DataModelError(f"Expected a dict for Batch data but got {type(data).__name__}")
        try:
            date_str = data.get('date_modified')
            date_obj = datetime.fromisoformat(date_str) if date_str else None

            return Batch(
                identifier=data.get('identifier'),
                version=data.get('version'),
                date_modified=date_obj,
                is_part_of=Project.from_json(is_part_of) if (is_part_of := data.get('is_part_of')) else None,
                in_language=Language.from_json(in_language) if (in_language := data.get('in_language')) else None,
                namespace=Namespace.from_json(namespace) if (namespace := data.get('namespace')) else None,
                size=Size.from_json(size) if (size := data.get('size')) else None
            )
        except (ValueError, TypeError) as e:
            batch_id = data.get('identifier', 'N/A')
            raise DataModelError(f"Failed to parse Batch with identifier '{batch_id}': {e}") from e

    @staticmethod
    def to_json(batch: 'Batch') -> dict:
        """Safely converts a Batch instance to a dictionary, handling optional None values."""
        return {
            'identifier': batch.identifier,
            'version': batch.version,
            'date_modified': batch.date_modified.isoformat() if batch.date_modified else None,
            'is_part_of': Project.to_json(batch.is_part_of) if batch.is_part_of else None,
            'in_language': Language.to_json(batch.in_language) if batch.in_language else None,
            'namespace': Namespace.to_json(batch.namespace) if batch.namespace else None,
            'size': Size.to_json(batch.size) if batch.size else None
        }
