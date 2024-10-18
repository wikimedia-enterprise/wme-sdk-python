from typing import Optional


class Size:
    def __init__(self,
                 value: Optional[float] = None,
                 unit_text: Optional[str] = None):
        self.value = value
        self.unit_text = unit_text

    @staticmethod
    def from_json(data: dict) -> 'Size':
        return Size(
            value=data['value'],
            unit_text=data['unit_text']
        )

    @staticmethod
    def to_json(size: 'Size') -> dict:
        return {
            'value': size.value,
            'unit_text': size.unit_text
        }
