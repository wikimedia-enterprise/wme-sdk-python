"""Represents a size with a numerical value"""

from typing import Optional
from .exceptions import DataModelError

class Size:
    """Represents a size with a numerical value"""
    def __init__(self,
                 value: Optional[float] = None,
                 unit_text: Optional[str] = None):
        self.value = value
        self.unit_text = unit_text

    @staticmethod
    def from_json(data: dict) -> 'Size':
        """Constructs a Size object from a dictionary representation."""
        if not isinstance(data, dict):
            raise DataModelError(f"Expected a dict for Size data, but got {type(data).__name__}")

        try:
            return Size(
                value=data.get('value'),
                unit_text=data.get('unit_text')
            )
        except (KeyError, TypeError) as e:
            raise DataModelError(f"Failed to parse Size data: {e}") from e

    @staticmethod
    def to_json(size: 'Size') -> dict:
        """Converts a Size instance into a dictionary for JSON serialization."""
        return {
            'value': size.value,
            'unit_text': size.unit_text
        }
