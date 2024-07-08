class StructuredContent:
    """
    StructuredContent representation.
    """

    def __init__(self, title=None, body=None, format=None):
        """
        Initialize StructuredContent instance.

        :param title: The title of the content.
        :param body: The body of the content.
        :param format: The format of the content.
        """
        self.title = title
        self.body = body
        self.format = format

    def to_dict(self):
        """
        Convert the StructuredContent instance to a dictionary.
        """
        return {
            "title": self.title,
            "body": self.body,
            "format": self.format
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a StructuredContent instance from a dictionary.
        """
        return cls(
            title=data.get("title"),
            body=data.get("body"),
            format=data.get("format")
        )
