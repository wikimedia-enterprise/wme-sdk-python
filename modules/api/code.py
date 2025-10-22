"""Represents a project's code with it's data"""

from typing import Optional


class Code:
    """Represents a projects code"""
    def __init__(self,
                 identifier: Optional[str] = None,
                 name: Optional[str] = None,
                 description: Optional[str] = None):
        self.identifier = identifier
        self.name = name
        self.description = description

    @staticmethod
    def from_json(data: dict) -> 'Code':
        """Creates a Code instance from a dictionary"""
        return Code(
            identifier=data['identifier'],
            name=data['name'],
            description=data['description']
        )

    @staticmethod
    def to_json(code: 'Code') -> dict:
        """Converts a Code instance into a dictionary for JSON serialization."""
        return {
            'identifier': code.identifier,
            'name': code.name,
            'description': code.description
        }
