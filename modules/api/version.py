class Version:
    """
    Version representation.
    """

    def __init__(self, number=None, name=None):
        """
        Initialize Version instance.

        :param number: The version number.
        :param name: The version name.
        """
        self.number = number
        self.name = name

    def to_dict(self):
        """
        Convert the Version instance to a dictionary.
        """
        return {
            "number": self.number,
            "name": self.name
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Version instance from a dictionary.
        """
        return cls(
            number=data.get("number"),
            name=data.get("name")
        )
