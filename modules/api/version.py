from typing import List, Optional
from scores import Scores
from editor import Editor
from size import Size


class PreviousVersion:
    def __init__(self,
                 identifier: Optional[int] = None,
                 number_of_characters: Optional[int] = None):
        self.identifier = identifier
        self.number_of_characters = number_of_characters
    @staticmethod
    def from_json(data: dict) -> 'PreviousVersion':
        """Creates a PreviousVersion instance from a dictionary (JSON object)"""
        if not isinstance(data, dict):
            return PreviousVersion()
        return PreviousVersion(
            identifier=data.get('identifier'),
            number_of_characters=data.get('number_of_characters')
        )
    @staticmethod
    def to_json(previous_version: 'PreviousVersion') -> dict:
        """Converts a PreviousVersion instance to a dictionary for JSON serialization"""
        return {
            'identifier': previous_version.identifier,
            'number_of_characters': previous_version.number_of_characters
        }
        


class Version:
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
        return Version(
            # Initialize Version fields from data
            data['identifier'],
            data['comment'],
            data['tags'],
            data['is_minor_edit'],
            data['is_flagged_stable'],
            data['is_breaking_news'],
            data['has_tag_needs_citation'],
            Scores.from_json(data['scores']),
            Editor.from_json(data['editor']),
            data['number_of_characters'],
            Size.from_json(data['size'])
        )

    @staticmethod
    def to_json(version: 'Version') -> dict:
        return {
            'identifier': version.identifier,
            'comment': version.comment,
            'tags': version.tags,
            'is_minor_edit': version.is_minor_edit,
            'is_flagged_stable': version.is_flagged_stable,
            'is_breaking_news': version.is_breaking_news,
            'has_tag_needs_citation': version.has_tag_needs_citation,
            'scores': Scores.to_json(version.scores),
            'editor': Editor.to_json(version.editor),
            'number_of_characters': version.number_of_characters,
            'size': Size.to_json(version.size)
        }
