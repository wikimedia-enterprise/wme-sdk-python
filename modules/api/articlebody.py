from typing import Optional


class ArticleBody:
    def __init__(self,
                 html: Optional[str] = None,
                 wikitext: Optional[str] = None):
        self.html = html
        self.wikitext = wikitext

    @staticmethod
    def from_json(data: dict) -> 'ArticleBody':
        return ArticleBody(
            html=data['html'],
            wikitext=data['wikitext']
        )

    @staticmethod
    def to_json(article_body: 'ArticleBody') -> dict:
        return {
            'html': article_body.html,
            'wikitext': article_body.wikitext
        }
