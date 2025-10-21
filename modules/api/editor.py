# pylint: disable=too-many-instance-attributes, too-many-arguments, too-many-positional-arguments

"""Represents an editor and their data"""

from typing import List, Optional
from datetime import datetime
from .exceptions import DataModelError


class Editor:
    """Represents a user or editor who contributes to content."""
    def __init__(self,
                 identifier: Optional[int] = None,
                 name: Optional[str] = None,
                 edit_count: Optional[int] = None,
                 groups: Optional[List[str]] = None,
                 is_bot: Optional[bool] = None,
                 is_anonymous: Optional[bool] = None,
                 is_admin: Optional[bool] = None,
                 is_patroller: Optional[bool] = None,
                 has_advanced_rights: Optional[bool] = None,
                 date_started: Optional[datetime] = None):
        self.identifier = identifier
        self.name = name
        self.edit_count = edit_count
        self.groups = groups or []
        self.is_bot = is_bot
        self.is_anonymous = is_anonymous
        self.is_admin = is_admin
        self.is_patroller = is_patroller
        self.has_advanced_rights = has_advanced_rights
        self.date_started = date_started

    @staticmethod
    def from_json(data: dict) -> 'Editor':
        """
        Deserializes a dictionary into an Editor instance.

        This method maps dictionary keys to Editor attributes, parsing the
        ISO 8601 'date_started' string into a datetime object.

        Args:
            data: A dictionary containing the editor's data.

        Returns:
            An Editor instance.

        Raises:
            DataModelError: If the input is not a dict or if parsing fails
                            (e.g., invalid date format).
        """
        if not isinstance(data, dict):
            raise DataModelError(f"Expected a dict for Editor data, but got {type(data).__name__}")

        try:
            date_str = data.get('date_started')

            return Editor(
                identifier=data.get('identifier'),
                name=data.get('name'),
                edit_count=data.get('edit_count'),
                groups=data.get('groups'),
                is_bot=data.get('is_bot'),
                is_anonymous=data.get('is_anonymous'),
                is_admin=data.get('is_admin'),
                is_patroller=data.get('is_patroller'),
                has_advanced_rights=data.get('has_advanced_rights'),
                date_started=datetime.fromisoformat(date_str) if date_str else None
            )
        except (ValueError, TypeError) as e:
            editor_name = data.get('name', 'N/A')
            raise DataModelError(f"Failed to parse Editor with name '{editor_name}': {e}") from e

    @staticmethod
    def to_json(editor: 'Editor') -> dict:
        """
        Serializes the Editor instance into a JSON-compatible dictionary.

        Formats the 'date_started' datetime object as an ISO 8601 string.

        Args:
            editor: The Editor instance to serialize.

        Returns:
            A dictionary representation of the editor.
        """
        return {
            'identifier': editor.identifier,
            'name': editor.name,
            'editCount': editor.edit_count,
            'groups': editor.groups,
            'is_bot': editor.is_bot,
            'is_anonymous': editor.is_anonymous,
            'is_admin': editor.is_admin,
            'is_patroller': editor.is_patroller,
            'has_advanced_rights': editor.has_advanced_rights,
            'date_started': editor.date_started.isoformat() if editor.date_started else None
        }
