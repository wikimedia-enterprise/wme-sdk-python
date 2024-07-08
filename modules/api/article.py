from articlebody import ArticleBody


class Article:
    """
    Article representation.
    """

    def __init__(self, title=None, body=None, tags=None):
        """
        Initialize Article instance.

        :param title: The title of the article.
        :param body: The body of the article (an ArticleBody instance).
        :param tags: The tags associated with the article.
        """
        self.title = title
        self.body = body if body else ArticleBody()
        self.tags = tags if tags else []

    def to_dict(self):
        """
        Convert the Article instance to a dictionary.
        """
        return {
            "title": self.title,
            "body": self.body.to_dict(),
            "tags": self.tags
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create an Article instance from a dictionary.
        """
        body = ArticleBody.from_dict(data.get("body", {}))
        return cls(
            title=data.get("title"),
            body=body,
            tags=data.get("tags", [])
        )
