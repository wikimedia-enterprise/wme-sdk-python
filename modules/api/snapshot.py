class Snapshot:
    """
    Snapshot representation.
    """

    def __init__(self, timestamp=None, description=None):
        """
        Initialize Snapshot instance.

        :param timestamp: The timestamp of the snapshot.
        :param description: The description of the snapshot.
        """
        self.timestamp = timestamp
        self.description = description

    def to_dict(self):
        """
        Convert the Snapshot instance to a dictionary.
        """
        return {
            "timestamp": self.timestamp,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Snapshot instance from a dictionary.
        """
        return cls(
            timestamp=data.get("timestamp"),
            description=data.get("description")
        )
