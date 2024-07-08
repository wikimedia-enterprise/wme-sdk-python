from typing import Optional


class ArticleBody:
    def __init__(self,
                 html: Optional[str] = None,
                 wikitext: Optional[str] = None):
        self.html = html
        self.wikitext = wikitext
