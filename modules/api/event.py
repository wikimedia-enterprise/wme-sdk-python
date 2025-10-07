from typing import Optional, Set
from datetime import datetime
from exceptions import DataModelError

# Type of events supported by the system.
EVENT_TYPE_UPDATE = "update"
EVENT_TYPE_DELETE = "delete"
EVENT_TYPE_VISIBILITY_CHANGE = "visibility-change"
VALID_EVENT_TYPES: Set[str] = {EVENT_TYPE_UPDATE, EVENT_TYPE_DELETE, EVENT_TYPE_VISIBILITY_CHANGE}

class Event:
    def __init__(self,
                 identifier: Optional[str] = None,
                 event_type: Optional[str] = None,
                 date_created: Optional[datetime] = None,
                 date_published: Optional[datetime] = None,
                 partition: Optional[int] = None,
                 offset: Optional[int] = None):
        self.identifier = identifier
        self.event_type = event_type
        self.date_created = date_created
        self.date_published = date_published
        self.partition = partition
        self.offset = offset

    @staticmethod
    def from_json(data: dict) -> 'Event':
        if not isinstance(data, dict):
            raise DataModelError(f"Expected a dict for Event data, but got {type(data).__name__}")
        
        try:
            event_type_str = data.get('eventType')
            if event_type_str and event_type_str not in VALID_EVENT_TYPES:
                raise ValueError(f"'{event_type_str}' is not a valid event type.")
            
            created_str = data.get('dateCreated')
            published_str = data.get('datePublished')
            
            return Event(
                identifier=data.get('identifier'),
                event_type=event_type_str,
                date_created=datetime.fromisoformat(created_str) if created_str else None,
                date_published=datetime.fromisoformat(published_str) if published_str else None,
                partition=data.get('partition'),
                offset=data.get('offset')
            )
        except (ValueError, TypeError) as e:
            event_id = data.get('identifier', 'N/A')
            raise DataModelError(f"Failed to parse Event with identifier '{event_id}': {e}") from e

    @staticmethod
    def to_json(event: 'Event') -> dict:
        return {
            'identifier': event.identifier,
            'eventType': event.event_type,
            'dateCreated': event.date_created.isoformat() if event.date_created else None,
            'datePublished': event.date_published.isoformat() if event.date_published else None,
            'partition': event.partition,
            'offset': event.offset
        }