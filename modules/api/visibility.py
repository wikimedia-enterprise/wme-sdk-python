from typing import Optional


class Visibility:
    def __init__(self,
                 text: Optional[bool] = None,
                 editor: Optional[bool] = None,
                 comment: Optional[bool] = None):
        self.text = text
        self.editor = editor
        self.comment = comment
