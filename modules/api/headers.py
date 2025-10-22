# pylint: disable=too-many-arguments, too-many-positional-arguments

"""Represents a collection of HTTP headers for a resource and it's parsing methods"""

from typing import Optional
from datetime import datetime
from .exceptions import DataModelError

HTTP_DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"


class Headers:
    """Holds key HTTP metadata for a resource, like ETag and Content-Length."""
    def __init__(self,
                 content_length: Optional[int] = None,
                 etag: Optional[str] = None,
                 last_modified: Optional[datetime] = None,
                 content_type: Optional[str] = None,
                 accept_ranges: Optional[str] = None):
        self.content_length = content_length
        self.etag = etag
        self.last_modified = last_modified
        self.content_type = content_type
        self.accept_ranges = accept_ranges

    @staticmethod
    def from_json(data: dict) -> 'Headers':
        """
        Deserializes a dictionary into a Headers instance.

        This method maps dictionary keys to Headers attributes, parsing the
        'last_modified' string using the standard HTTP date format
        (e.g., "Mon, 15 Jan 2001 07:28:00 GMT").

        Args:
            data: A dictionary containing the header data.

        Returns:
            A Headers instance.

        Raises:
            DataModelError: If the input is not a dict or if date parsing fails.
        """
        if not isinstance(data, dict):
            raise DataModelError(f"Expected a dict for Headers data, but got {type(data).__name__}")

        try:
            last_modified_str = data.get('last_modified')

            return Headers(
                content_length=data.get('content_length'),
                etag=data.get('etag'),

                last_modified=datetime.strptime(last_modified_str, HTTP_DATE_FORMAT) if last_modified_str else None,

                content_type=data.get('content_type'),
                accept_ranges=data.get('accept_ranges')
            )
        except (ValueError, TypeError) as e:
            raise DataModelError(f"Failed to parse Headers data: {e}") from e

    @staticmethod
    def to_json(headers: 'Headers') -> dict:
        """
        Serializes the Headers instance into a JSON-compatible dictionary.

        Formats the 'last_modified' datetime object as a standard
        HTTP date string (e.g., "Mon, 15 Jan 2001 07:28:00 GMT").

        Args:
            headers: The Headers instance to serialize.

        Returns:
            A dictionary representation of the headers.
        """
        return {
            'content_length': headers.content_length,
            'etag': headers.etag,

            'last_modified': headers.last_modified.strftime(HTTP_DATE_FORMAT) if headers.last_modified else None,

            'content_type': headers.content_type,
            'accept_ranges': headers.accept_ranges
        }
