class Entity:
    """
    Entity representation.
    """

    def __init__(self, id=None, name=None, type=None):
        """
        Initialize Entity instance.

        :param id: The entity identifier.
        :param name: The name of the entity.
        :param type: The type of the entity.
        """
        self.id = id
        self.name = name
        self.type = type

    def to_dict(self):
        """
        Convert the Entity instance to a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create an Entity instance from a dictionary.
        """
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            type=data.get("type")
        )
