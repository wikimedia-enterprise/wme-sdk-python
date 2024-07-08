from typing import List, Optional
from datetime import datetime
from protection import Protection
from version import Version, PreviousVersion
from namespace import Namespace
from language import Language
from entity import Entity
from articlebody import ArticleBody
from license import License
from visibility import Visibility
from event import Event
from project import Project


class Image:
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


class Category:
    def __init__(self,
                 name: Optional[str] = None,
                 url: Optional[str] = None):
        self.name = name
        self.url = url


class Redirect:
    def __init__(self,
                 name: Optional[str] = None,
                 url: Optional[str] = None):
        self.name = name
        self.url = url


class Template:
    def __init__(self,
                 name: Optional[str] = None,
                 url: Optional[str] = None):
        self.name = name
        self.url = url


class Article:
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
                 license: Optional[List[License]] = None,
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
        self.license = license or []
        self.visibility = visibility
        self.event = event
        self.image = image
