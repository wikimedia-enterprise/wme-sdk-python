class License:
    """
    License representation.
    """

    def __init__(self, name=None, url=None):
        """
        Initialize License instance.

        :param name: The name of the license.
        :param url: The URL of the license.
        """
        self.name = name
        self.url = url

    def to_dict(self):
        """
        Convert the License instance to a dictionary.
        """
        return {
            "name": self.name,
            "url": self.url
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a License instance from a dictionary.
        """
        return cls(
            name=data.get("name"),
            url=data.get("url")
        )
