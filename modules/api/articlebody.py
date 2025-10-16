"""Defines an article's body"""

from typing import Optional


class ArticleBody:
    """Represents an article's body"""
    def __init__(self,
                 html: Optional[str] = None,
                 wikitext: Optional[str] = None):
        self.html = html
        self.wikitext = wikitext

    @staticmethod
    def from_json(data: dict) -> 'ArticleBody':
        """Creates an ArticleBody instance from a dictionary"""
        return ArticleBody(
            html=data['html'],
            wikitext=data['wikitext']
        )

    @staticmethod
    def to_json(article_body: 'ArticleBody') -> dict:
        """Converts a ArticleBody instance into a dictionary for JSON serialization."""
        return {
            'html': article_body.html,
            'wikitext': article_body.wikitext
        }
