class ArticleBody:
    """
    ArticleBody representation.
    """

    def __init__(self, content=None, language=None):
        """
        Initialize ArticleBody instance.

        :param content: The content of the article body.
        :param language: The language of the article body.
        """
        self.content = content
        self.language = language

    def to_dict(self):
        """
        Convert the ArticleBody instance to a dictionary.
        """
        return {
            "content": self.content,
            "language": self.language
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create an ArticleBody instance from a dictionary.
        """
        return cls(
            content=data.get("content"),
            language=data.get("language")
        )
