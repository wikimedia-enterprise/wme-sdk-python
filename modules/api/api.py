class API:
    """
    API representation.
    """

    def __init__(self, version=None, endpoint=None):
        """
        Initialize API instance.

        :param version: The API version.
        :param endpoint: The API endpoint.
        """
        self.version = version
        self.endpoint = endpoint

    def to_dict(self):
        """
        Convert the API instance to a dictionary.
        """
        return {
            "version": self.version,
            "endpoint": self.endpoint
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create an API instance from a dictionary.
        """
        return cls(
            version=data.get("version"),
            endpoint=data.get("endpoint")
        )
