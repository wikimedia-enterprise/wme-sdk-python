class Project:
    """
    Project representation.
    """

    def __init__(self, name=None, description=None, active=None):
        """
        Initialize Project instance.

        :param name: The name of the project.
        :param description: The description of the project.
        :param active: Indicates if the project is active.
        """
        self.name = name
        self.description = description
        self.active = active

    def to_dict(self):
        """
        Convert the Project instance to a dictionary.
        """
        return {
            "name": self.name,
            "description": self.description,
            "active": self.active
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Project instance from a dictionary.
        """
        return cls(
            name=data.get("name"),
            description=data.get("description"),
            active=data.get("active")
        )
