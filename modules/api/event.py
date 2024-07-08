class Event:
    """
    Event representation.
    """

    def __init__(self, id=None, type=None, description=None, timestamp=None):
        """
        Initialize Event instance.

        :param id: The event identifier.
        :param type: The type of the event.
        :param description: The description of the event.
        :param timestamp: The timestamp of the event.
        """
        self.id = id
        self.type = type
        self.description = description
        self.timestamp = timestamp

    def to_dict(self):
        """
        Convert the Event instance to a dictionary.
        """
        return {
            "id": self.id,
            "type": self.type,
            "description": self.description,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create an Event instance from a dictionary.
        """
        return cls(
            id=data.get("id"),
            type=data.get("type"),
            description=data.get("description"),
            timestamp=data.get("timestamp")
        )
