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
