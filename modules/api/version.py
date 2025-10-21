# pylint: disable=too-many-arguments, too-many-positional-arguments, too-many-instance-attributes

"""Defines data models for content revisions and their metadata."""

from typing import List, Optional
from .scores import Scores
from .editor import Editor
from .size import Size
from .exceptions import DataModelError


class PreviousVersion:
    """A lightweight reference to the version preceding the current one."""
    def __init__(self,
                 identifier: Optional[int] = None,
                 number_of_characters: Optional[int] = None):
        self.identifier = identifier
        self.number_of_characters = number_of_characters

    @staticmethod
    def from_json(data: dict) -> 'PreviousVersion':
        """Creates a PreviousVersion instance from a dictionary (JSON object)"""
        if not isinstance(data, dict):
            raise DataModelError(f"Expected dict for PreviousVersion, got {type(data).__name__}")
        try:
            return PreviousVersion(
                identifier=data.get('identifier'),
                number_of_characters=data.get('number_of_characters')
            )
        except (KeyError, TypeError) as e:
            prev_id = data.get('identifier', 'N/A')
            raise DataModelError(f"Failed to parse PreviousVersion '{prev_id}': {e}") from e
    @staticmethod
    def to_json(previous_version: 'PreviousVersion') -> dict:
        """Converts a PreviousVersion instance to a dictionary for JSON serialization"""
        return {
            'identifier': previous_version.identifier,
            'number_of_characters': previous_version.number_of_characters
        }



class Version:
    """Represents a specific revision of a piece of content."""
    def __init__(self,
                 identifier: Optional[int] = None,
                 comment: Optional[str] = None,
                 tags: Optional[List[str]] = None,
                 is_minor_edit: Optional[bool] = None,
                 is_flagged_stable: Optional[bool] = None,
                 is_breaking_news: Optional[bool] = None,
                 has_tag_needs_citation: Optional[bool] = None,
                 scores: Optional[Scores] = None,
                 editor: Optional[Editor] = None,
                 number_of_characters: Optional[int] = None,
                 size: Optional[Size] = None):
        self.identifier = identifier
        self.comment = comment
        self.tags = tags or []
        self.is_minor_edit = is_minor_edit
        self.is_flagged_stable = is_flagged_stable
        self.is_breaking_news = is_breaking_news
        self.has_tag_needs_citation = has_tag_needs_citation
        self.scores = scores
        self.editor = editor
        self.number_of_characters = number_of_characters
        self.size = size

    @staticmethod
    def from_json(data: dict) -> 'Version':
        """Constructs a Version object from a dictionary representation."""
        if not isinstance(data, dict):
            raise DataModelError(f"Expected dict for Version, got {type(data).__name__}")

        try:
            return Version(
                identifier=data.get('identifier'),
                comment=data.get('comment'),
                tags=data.get('tags'),
                is_minor_edit=data.get('is_minor_edit'),
                is_flagged_stable=data.get('is_flagged_stable'),
                is_breaking_news=data.get('is_breaking_news'),
                has_tag_needs_citation=data.get('has_tag_needs_citation'),
                number_of_characters=data.get('number_of_characters'),
                scores=Scores.from_json(s_data) if (s_data := data.get('scores')) else None,
                editor=Editor.from_json(e_data) if (e_data := data.get('editor')) else None,
                size=Size.from_json(sz_data) if (sz_data := data.get('size')) else None
            )
        except (KeyError, TypeError, DataModelError) as e:
            version_id = data.get('identifier', 'N/A')
            raise DataModelError(f"Failed to parse Version '{version_id}': {e}") from e

    @staticmethod
    def to_json(version: 'Version') -> dict:
        """Converts a Version instance into a dictionary for JSON serialization."""
        return {
            'identifier': version.identifier,
            'comment': version.comment,
            'tags': version.tags,
            'is_minor_edit': version.is_minor_edit,
            'is_flagged_stable': version.is_flagged_stable,
            'is_breaking_news': version.is_breaking_news,
            'has_tag_needs_citation': version.has_tag_needs_citation,
            'number_of_characters': version.number_of_characters,
            'scores': Scores.to_json(version.scores) if version.scores else None,
            'editor': Editor.to_json(version.editor) if version.editor else None,
            'size': Size.to_json(version.size) if version.size else None
        }
