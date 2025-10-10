from typing import Optional
from exceptions import DataModelError


class Visibility:
    def __init__(self,
                 text: Optional[bool] = None,
                 editor: Optional[bool] = None,
                 comment: Optional[bool] = None):
        self.text = text
        self.editor = editor
        self.comment = comment

    @staticmethod
    def from_json(data: dict) -> 'Visibility':
        if not isinstance(data, dict):
            raise DataModelError(f"Expected a dict for Visibility data, but got {type(data).__name__}")
        
        try:
            return Visibility(
                text=data.get('text'),
                editor=data.get('editor'),
                comment=data.get('comment')
            )
        except (KeyError, TypeError) as e:
            raise DataModelError(f"Failed to parse Visibility data: {e}") from e

    @staticmethod
    def to_json(visibility: 'Visibility') -> dict:
        return {
            'text': visibility.text,
            'editor': visibility.editor,
            'comment': visibility.comment
        }
