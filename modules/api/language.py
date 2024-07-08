class Language:
    """
    Language representation.
    """

    def __init__(self, code=None, name=None):
        """
        Initialize Language instance.

        :param code: The language code.
        :param name: The name of the language.
        """
        self.code = code
        self.name = name

    def to_dict(self):
        """
        Convert the Language instance to a dictionary.
        """
        return {
            "code": self.code,
            "name": self.name
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Language instance from a dictionary.
        """
        return cls(
            code=data.get("code"),
            name=data.get("name")
        )
