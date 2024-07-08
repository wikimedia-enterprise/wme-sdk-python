class Headers:
    """
    Headers representation.
    """

    def __init__(self, key=None, value=None):
        """
        Initialize Headers instance.

        :param key: The header key.
        :param value: The header value.
        """
        self.key = key
        self.value = value

    def to_dict(self):
        """
        Convert the Headers instance to a dictionary.
        """
        return {
            "key": self.key,
            "value": self.value
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Headers instance from a dictionary.
        """
        return cls(
            key=data.get("key"),
            value=data.get("value")
        )
