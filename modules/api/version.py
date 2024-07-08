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
