from typing import Optional
from datetime import datetime

# Type of events supported by the system.
EVENT_TYPE_UPDATE = "update"
EVENT_TYPE_DELETE = "delete"
EVENT_TYPE_VISIBILITY_CHANGE = "visibility-change"


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
        return Event(
            identifier=data['identifier'],
            event_type=data['eventType'],
            date_created=datetime.fromisoformat(data['dateCreated']),
            date_published=datetime.fromisoformat(data['datePublished']),
            partition=data['partition'],
            offset=data['offset']
        )

    @staticmethod
    def to_json(event: 'Event') -> dict:
        return {
            'identifier': event.identifier,
            'eventType': event.event_type,
            'dateCreated': event.date_created.isoformat(),
            'datePublished': event.date_published.isoformat(),
            'partition': event.partition,
            'offset': event.offset
        }
