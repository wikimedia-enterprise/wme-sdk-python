from typing import Optional


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
        return Visibility(
            text=data['text'],
            editor=data['editor'],
            comment=data['comment']
        )

    @staticmethod
    def to_json(visibility: 'Visibility') -> dict:
        return {
            'text': visibility.text,
            'editor': visibility.editor,
            'comment': visibility.comment
        }
