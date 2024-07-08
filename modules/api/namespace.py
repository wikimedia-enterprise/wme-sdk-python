class Namespace:
    """
    Namespace representation.
    """

    def __init__(self, prefix=None, uri=None):
        """
        Initialize Namespace instance.

        :param prefix: The namespace prefix.
        :param uri: The namespace URI.
        """
        self.prefix = prefix
        self.uri = uri

    def to_dict(self):
        """
        Convert the Namespace instance to a dictionary.
        """
        return {
            "prefix": self.prefix,
            "uri": self.uri
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Namespace instance from a dictionary.
        """
        return cls(
            prefix=data.get("prefix"),
            uri=data.get("uri")
        )
