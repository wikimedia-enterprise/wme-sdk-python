# pylint: disable=too-many-arguments, too-many-positional-arguments, R0801

"""Data model for Wikimedia Enterprise batch metadata."""

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
        """
        Deserializes a dictionary into a Batch instance.

        This method maps dictionary keys to Batch attributes, parsing nested
        objects (Project, Language, etc.) and ISO 8601 date strings.

        Args:
            data: A dictionary containing the batch metadata.

        Returns:
            A Batch instance.

        Raises:
            DataModelError: If the input is not a dict or if parsing fails
                            (e.g., invalid date format).
        """
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
        """
        Serializes the Batch instance into a JSON-compatible dictionary.

        Converts nested objects (Project, Language, etc.) to their dictionary
        representations and formats datetime objects as ISO 8601 strings.

        Args:
            batch: The Batch instance to serialize.

        Returns:
            A dictionary representation of the batch.
        """
        return {
            'identifier': batch.identifier,
            'version': batch.version,
            'date_modified': batch.date_modified.isoformat() if batch.date_modified else None,
            'is_part_of': Project.to_json(batch.is_part_of) if batch.is_part_of else None,
            'in_language': Language.to_json(batch.in_language) if batch.in_language else None,
            'namespace': Namespace.to_json(batch.namespace) if batch.namespace else None,
            'size': Size.to_json(batch.size) if batch.size else None
        }
