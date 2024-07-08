from typing import Optional


class Size:
    def __init__(self,
                 value: Optional[float] = None,
                 unit_text: Optional[str] = None):
        self.value = value
        self.unit_text = unit_text
