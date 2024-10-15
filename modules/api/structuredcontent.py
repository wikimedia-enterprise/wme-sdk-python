from typing import List, Optional
from datetime import datetime
from modules.api.article import Image
from version import Version
from entity import Entity
from project import Project
from language import Language
from namespace import Namespace
from size import Size


class Link:
    def __init__(self,
                 url: Optional[str] = None,
                 text: Optional[str] = None,
                 images: Optional[List[Image]] = None):
        self.url = url
        self.text = text
        self.images = images or []


class Part:
    def __init__(self,
                 name: Optional[str] = None,
                 part_type: Optional[str] = None,
                 value: Optional[str] = None,
                 values: Optional[List[str]] = None,
                 images: Optional[List[Image]] = None,
                 links: Optional[List[Link]] = None,
                 has_parts: Optional[List['Part']] = None):
        self.name = name
        self.part_type = part_type
        self.value = value
        self.values = values or []
        self.images = images or []
        self.links = links or []
        self.has_parts = has_parts or []


class StructuredContent:
    def __init__(self,
                 name: Optional[str] = None,
                 identifier: Optional[int] = None,
                 abstract: Optional[str] = None,
                 description: Optional[str] = None,
                 version: Optional[Version] = None,
                 url: Optional[str] = None,
                 date_created: Optional[datetime] = None,
                 date_modified: Optional[datetime] = None,
                 main_entity: Optional[Entity] = None,
                 additional_entities: Optional[List[Entity]] = None,
                 is_part_of: Optional[Project] = None,
                 in_language: Optional[Language] = None,
                 infobox: Optional[List[Part]] = None,
                 article_sections: Optional[List[Part]] = None,
                 image: Optional[Image] = None):
        self.name = name
        self.identifier = identifier
        self.abstract = abstract
        self.description = description
        self.version = version
        self.url = url
        self.date_created = date_created
        self.date_modified = date_modified
        self.main_entity = main_entity
        self.additional_entities = additional_entities or []
        self.is_part_of = is_part_of
        self.in_language = in_language
        self.infobox = infobox or []
        self.article_sections = article_sections or []
        self.image = image       



class StructuredContentSnapshot:
    def __init__(self,
                 identifier: Optional[str] = None,
                 version: Optional[str] = None,
                 date_modified: Optional[datetime] = None,
                 is_part_of: Optional[Project] = None,
                 in_language: Optional[Language] = None,
                 namespace: Optional[Namespace] = None,
                 size: Optional[Size] = None):
        self.identifier = identifier
        self.version = version
        self.date_modified = date_modified
        self.is_part_of = is_part_of
        self.in_language = in_language
        self.namespace = namespace
        self.size = size