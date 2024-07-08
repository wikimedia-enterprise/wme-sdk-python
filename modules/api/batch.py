class Batch:
    """
    Batch representation.
    """

    def __init__(self, id=None, size=None, completed=None):
        """
        Initialize Batch instance.

        :param id: The batch identifier.
        :param size: The size of the batch.
        :param completed: Indicates if the batch is completed.
        """
        self.id = id
        self.size = size
        self.completed = completed

    def to_dict(self):
        """
        Convert the Batch instance to a dictionary.
        """
        return {
            "id": self.id,
            "size": self.size,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Batch instance from a dictionary.
        """
        return cls(
            id=data.get("id"),
            size=data.get("size"),
            completed=data.get("completed")
        )
