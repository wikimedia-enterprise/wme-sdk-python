"""Represents a language and it's parsing methods"""

from typing import Optional, Set
from .exceptions import DataModelError

VALID_DIRECTIONS: Set[str] = {'ltr', 'rtl'}

class Language:
    """Represents a language and its writing direction."""
    def __init__(self,
                 identifier: Optional[str] = None,
                 name: Optional[str] = None,
                 alternate_name: Optional[str] = None,
                 direction: Optional[str] = None):
        self.identifier = identifier
        self.name = name
        self.alternate_name = alternate_name
        self.direction = direction

    @staticmethod
    def from_json(data: dict) -> 'Language':
        """Constructs a Language object from a dictionary representation."""
        if not isinstance(data, dict):
            raise DataModelError(f"Expected a dict for Language data, but got {type(data).__name__}")
        try:
            direction_str = data.get('direction')
            if direction_str and direction_str not in VALID_DIRECTIONS:
                raise ValueError(f"'{direction_str}' is not a valid direction.")

            return Language(
                identifier=data.get('identifier'),
                name=data.get('name'),
                alternate_name=data.get('alternate_name'),
                direction=direction_str
            )
        except (ValueError, TypeError) as e:
            lang_name = data.get('name', 'N/A')
            raise DataModelError(f"Failed to parse Language data for '{lang_name}': {e}") from e


    @staticmethod
    def to_json(language: 'Language') -> dict:
        """Converts a Language instance into a dictionary for JSON serialization."""
        return {
            'identifier': language.identifier,
            'name': language.name,
            'alternate_name': language.alternate_name,
            'direction': language.direction
        }
