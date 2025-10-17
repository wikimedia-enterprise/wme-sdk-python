"""Defines a data model for a snapshot"""

from typing import Optional, List
from datetime import datetime
from .project import Project
from .language import Language
from .namespace import Namespace
from .size import Size
from .exceptions import DataModelError

# pylint: disable=too-many-instance-attributes
class Snapshot:
    """Represents metadata for a specific snapshot of a bulk data dump."""
    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def __init__(self,
                 identifier: Optional[str] = None,
                 version: Optional[str] = None,
                 date_modified: Optional[datetime] = None,
                 is_part_of: Optional[Project] = None,
                 in_language: Optional[Language] = None,
                 namespace: Optional[Namespace] = None,
                 size: Optional[Size] = None,
                 chunks: Optional[List[str]] = None):
        self.identifier = identifier
        self.version = version
        self.date_modified = date_modified
        self.is_part_of = is_part_of
        self.in_language = in_language
        self.namespace = namespace
        self.size = size
        self.chunks = chunks or []

    @staticmethod
    def from_json(data: dict) -> 'Snapshot':
        """Constructs a Snapshot object from a dictionary representation."""
        if not isinstance(data, dict):
            raise DataModelError(f"Expected a dict for Snapshot data, but got {type(data).__name__}")

        try:
            date_str = data.get('date_modified')

            return Snapshot(
                identifier=data.get('identifier'),
                version=data.get('version'),
                date_modified=datetime.fromisoformat(date_str) if date_str else None,
                is_part_of=Project.from_json(p_data) if (p_data := data.get('is_part_of')) else None,
                in_language=Language.from_json(l_data) if (l_data := data.get('in_language')) else None,
                namespace=Namespace.from_json(n_data) if (n_data := data.get('namespace')) else None,
                size=Size.from_json(s_data) if (s_data := data.get('size')) else None,
                chunks=data.get('chunks')
            )
        except (ValueError, TypeError, DataModelError) as e:
            snapshot_id = data.get('identifier', 'N/A')
            raise DataModelError(f"Failed to parse Snapshot data for '{snapshot_id}': {e}") from e

    @staticmethod
    def to_json(snapshot: 'Snapshot') -> dict:
        """Converts a Snapshot instance into a dictionary for JSON serialization."""
        return {
            'identifier': snapshot.identifier,
            'version': snapshot.version,
            'chunks': snapshot.chunks,
            'date_modified': snapshot.date_modified.isoformat() if snapshot.date_modified else None,
            'is_part_of': Project.to_json(snapshot.is_part_of) if snapshot.is_part_of else None,
            'in_language': Language.to_json(snapshot.in_language) if snapshot.in_language else None,
            'namespace': Namespace.to_json(snapshot.namespace) if snapshot.namespace else None,
            'size': Size.to_json(snapshot.size) if snapshot.size else None
        }
