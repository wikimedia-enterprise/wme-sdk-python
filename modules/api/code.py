class Code:
    """
    Code representation.
    """

    def __init__(self, value=None, description=None):
        """
        Initialize Code instance.

        :param value: The code value.
        :param description: The description of the code.
        """
        self.value = value
        self.description = description

    def to_dict(self):
        """
        Convert the Code instance to a dictionary.
        """
        return {
            "value": self.value,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Code instance from a dictionary.
        """
        return cls(
            value=data.get("value"),
            description=data.get("description")
        )
