# pylint: disable=too-many-arguments, too-many-positional-arguments, too-many-instance-attributes, too-many-locals

"""Defines data models for representing a Wikimedia article and its components."""

from typing import List, Optional
from datetime import datetime
from .protection import Protection
from .version import Version, PreviousVersion
from .namespace import Namespace
from .language import Language
from .entity import Entity
from .articlebody import ArticleBody
from .license import License
from .visibility import Visibility
from .event import Event
from .project import Project
from .exceptions import DataModelError


class Image:
    """Represents an image with its associated metadata"""

    def __init__(self,
                 content_url: Optional[str] = None,
                 width: Optional[int] = None,
                 height: Optional[int] = None,
                 alternative_text: Optional[str] = None,
                 caption: Optional[str] = None):
        self.content_url = content_url
        self.width = width
        self.height = height
        self.alternative_text = alternative_text
        self.caption = caption

    @staticmethod
    def from_json(data: dict) -> 'Image':
        """Creates an Image instance from a dictionary"""
        return Image(
            content_url=data.get('content_url'),
            width=data.get('width'),
            height=data.get('height'),
            alternative_text=data.get('alternative_text'),
            caption=data.get('caption')
           )

    @staticmethod
    def to_json(image: 'Image') -> dict:
        """Converts an Image instance into a dictionary for JSON serialization."""
        return {
            'content_url': image.content_url,
            'width': image.width,
            'height': image.height,
            'alternative_text': image.alternative_text,
            'caption': image.caption
            }


class Category:
    """Represents a content's category"""
    def __init__(self,
                 name: Optional[str] = None,
                 url: Optional[str] = None):
        self.name = name
        self.url = url

    @staticmethod
    def from_json(data: dict) -> 'Category':
        """Creates a Category instance from a dictionary"""
        return Category(
            name=data.get('name'),
            url=data.get('url')
          )

    @staticmethod
    def to_json(category: 'Category') -> dict:
        """Converts a Category instance into a dictionary for JSON serialization."""
        return {
            'name': category.name,
            'url': category.url
        }


class Redirect:
    """Represents redirects within an article"""
    def __init__(self,
                 name: Optional[str] = None,
                 url: Optional[str] = None):
        self.name = name
        self.url = url

    @staticmethod
    def from_json(data: dict) -> 'Redirect':
        """Creates a Redirect instance from a dictionary"""
        return Redirect(
            name=data.get('name'),
            url=data.get('url')
         )

    @staticmethod
    def to_json(redirect: 'Redirect') -> dict:
        """Converts a Redirect instance into a dictionary for JSON serialization."""
        return {
            'name': redirect.name,
            'url': redirect.url
        }


class Template:
    """Represents a template"""
    def __init__(self,
                 name: Optional[str] = None,
                 url: Optional[str] = None):
        self.name = name
        self.url = url

    @staticmethod
    def from_json(data: dict) -> 'Template':
        """Creates a Template instance from a dictionary"""
        return Template(
            name=data.get('name'),
            url=data.get('url')
        )

    @staticmethod
    def to_json(template: 'Template') -> dict:
        """Converts a Template instance into a dictionary for JSON serialization."""
        return {
            'name': template.name,
            'url': template.url
        }

class Article:
    """Represents a comprehensive data model for an article."""
    def __init__(self,
                 name: Optional[str] = None,
                 abstract: Optional[str] = None,
                 identifier: Optional[int] = None,
                 date_created: Optional[datetime] = None,
                 date_modified: Optional[datetime] = None,
                 date_previously_modified: Optional[datetime] = None,
                 protection: Optional[List[Protection]] = None,
                 version: Optional[Version] = None,
                 previous_version: Optional[PreviousVersion] = None,
                 url: Optional[str] = None,
                 watchers_count: Optional[int] = None,
                 namespace: Optional[Namespace] = None,
                 in_language: Optional[Language] = None,
                 main_entity: Optional[Entity] = None,
                 additional_entities: Optional[List[Entity]] = None,
                 categories: Optional[List[Category]] = None,
                 templates: Optional[List[Template]] = None,
                 redirects: Optional[List[Redirect]] = None,
                 is_part_of: Optional[Project] = None,
                 article_body: Optional[ArticleBody] = None,
                 licenses: Optional[List[License]] = None,
                 visibility: Optional[Visibility] = None,
                 event: Optional[Event] = None,
                 image: Optional[Image] = None):
        self.name = name
        self.abstract = abstract
        self.identifier = identifier
        self.date_created = date_created
        self.date_modified = date_modified
        self.date_previously_modified = date_previously_modified
        self.protection = protection or []
        self.version = version
        self.previous_version = previous_version
        self.url = url
        self.watchers_count = watchers_count
        self.namespace = namespace
        self.in_language = in_language
        self.main_entity = main_entity
        self.additional_entities = additional_entities or []
        self.categories = categories or []
        self.templates = templates or []
        self.redirects = redirects or []
        self.is_part_of = is_part_of
        self.article_body = article_body
        self.licenses = licenses or []
        self.visibility = visibility
        self.event = event
        self.image = image

    @staticmethod
    def from_json(data: dict) -> 'Article':
        """Creates an Article instance from a dictionary"""
        try:
            return Article(
                name=data.get('name'),
                abstract=data.get('abstract'),
                identifier=data.get('identifier'),
                date_created=Article.parse_date(data.get('date_created')),
                date_modified=Article.parse_date(data.get('date_modified')),
                date_previously_modified=Article.parse_date(data.get('date_previously_modified')),
                protection=[Protection.from_json(p) for p in data.get('protection', [])],
                version=Version.from_json(version_data) if (version_data := data.get('version')) else None,
                previous_version=PreviousVersion.from_json(previous_version) if (previous_version := data.get('previous_version')) else None,
                url=data.get('url'),
                watchers_count=data.get('watchers_count'),
                namespace=Namespace.from_json(namespace) if (namespace := data.get('namespace')) else None,
                in_language=Language.from_json(in_language) if (in_language := data.get('in_language')) else None,
                main_entity=Entity.from_json(main_entity) if (main_entity := data.get('main_entity')) else None,
                additional_entities=[Entity.from_json(e) for e in data.get('additional_entities', [])],
                categories=[Category.from_json(c) for c in data.get('categories', [])],
                templates=[Template.from_json(t) for t in data.get('templates', [])],
                redirects=[Redirect.from_json(r) for r in data.get('redirects', [])],
                is_part_of=Project.from_json(is_part_of) if (is_part_of := data.get('is_part_of')) else None,
                article_body=ArticleBody.from_json(article_body) if (article_body := data.get('article_body')) else None,
                licenses=[License.from_json(l) for l in data.get('license', [])],
                visibility=Visibility.from_json(visibility) if (visibility := data.get('visibility')) else None,
                event=Event.from_json(event) if (event := data.get('event')) else None,
                image=Image.from_json(image) if (image := data.get('image')) else None,
        )
        except (ValueError, TypeError, KeyError) as e:
            article_id = data.get('identifier', 'N/A')
            raise DataModelError(f"Failed to parse Article with identifier '{article_id}': {e}") from e


    @staticmethod
    def to_json(article: 'Article') -> dict:
        """Converts a Article instance into a dictionary for JSON serialization."""
        return {
            'name': article.name,
            'abstract': article.abstract,
            'identifier': article.identifier,
            'date_created': article.date_created.strftime('%Y-%m-%dT%H:%M:%SZ') if article.date_created else None,
            'date_modified': article.date_modified.strftime('%Y-%m-%dT%H:%M:%SZ') if article.date_modified else None,
            'date_previously_modified': article.date_previously_modified.strftime('%Y-%m-%dT%H:%M:%SZ') if article.date_previously_modified else None,
            'protection': [Protection.to_json(p) for p in article.protection],
            'version': Version.to_json(article.version) if article.version else None,
            'previous_version': PreviousVersion.to_json(article.previous_version) if article.previous_version else None,
            'url': article.url,
            'watchers_count': article.watchers_count,
            'namespace': Namespace.to_json(article.namespace) if article.namespace else None,
            'in_language': Language.to_json(article.in_language) if article.in_language else None,
            'main_entity': Entity.to_json(article.main_entity) if article.main_entity else None,
            'additional_entities': [Entity.to_json(e) for e in article.additional_entities],
            'categories': [Category.to_json(c) for c in article.categories],
            'templates': [Template.to_json(t) for t in article.templates],
            'redirects': [Redirect.to_json(r) for r in article.redirects],
            'is_part_of': Project.to_json(article.is_part_of) if article.is_part_of else None,
            'article_body': ArticleBody.to_json(article.article_body) if article.article_body else None,
            'license': [License.to_json(l) for l in article.licenses],
            'visibility': Visibility.to_json(article.visibility) if article.visibility else None,
            'event': Event.to_json(article.event) if article.event else None,
            'image': Image.to_json(article.image) if article.image else None,
        }

    @staticmethod
    def parse_date(date_str: Optional[str]) -> Optional[datetime]:
        """Parses an article's date"""
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError as e:
            raise DataModelError(f"Invalid date format for '{date_str}': {e}") from e
