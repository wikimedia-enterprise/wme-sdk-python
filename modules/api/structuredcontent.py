from typing import List, Optional
from datetime import datetime
from version import Version
from entity import Entity
from project import Project
from language import Language
from image import Image


class Link:
    def __init__(self,
                 url: Optional[str] = None,
                 text: Optional[str] = None,
                 images: Optional[List[Image]] = None):
        self.url = url
        self.text = text
        self.images = images or []

    @staticmethod
    def from_json(data: dict) -> 'Link':
        return Link(
            url=data['url'],
            text=data['text'],
            images=[Image.from_json(image) for image in data['images']]
        )


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

    @staticmethod
    def from_json(data: dict) -> 'Part':
        return Part(
            name=data['name'],
            part_type=data['type'],
            value=data['value'],
            values=data['values'],
            images=[Image.from_json(image) for image in data['images']],
            links=[Link.from_json(link) for link in data['links']],
            has_parts=[Part.from_json(part) for part in data['hasParts']]
        )

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

    @staticmethod
    def from_json(data: dict) -> 'StructuredContent':
        return StructuredContent(
            name=data['name'],
            identifier=data['identifier'],
            abstract=data['abstract'],
            description=data['description'],
            version=Version.from_json(data['version']),
            url=data['url'],
            date_created=datetime.fromisoformat(data['dateCreated']),
            date_modified=datetime.fromisoformat(data['dateModified']),
            main_entity=Entity.from_json(data['mainEntity']),
            additional_entities=[Entity.from_json(entity) for entity in data['additionalEntities']],
            is_part_of=Project.from_json(data['isPartOf']),
            in_language=Language.from_json(data['inLanguage']),
            infobox=[Part.from_json(part) for part in data['infobox']],
            article_sections=[Part.from_json(section) for section in data['articleSections']],
            image=Image.from_json(data['image'])
        )

    @staticmethod
    def to_json(structured_content: 'StructuredContent') -> dict:
        return {
            'name': structured_content.name,
            'identifier': structured_content.identifier,
            'abstract': structured_content.abstract,
            'description': structured_content.description,
            'version': Version.to_json(structured_content.version),
            'url': structured_content.url,
            'dateCreated': structured_content.date_created.isoformat(),
            'dateModified': structured_content.date_modified.isoformat(),
            'mainEntity': Entity.to_json(structured_content.main_entity),
            'additionalEntities': [Entity.to_json(entity) for entity in structured_content.additional_entities],
            'isPartOf': Project.to_json(structured_content.is_part_of),
            'inLanguage': Language.to_json(structured_content.in_language),
            'infobox': [Part.to_json(part) for part in structured_content.infobox],
            'articleSections': [Part.to_json(section) for section in structured_content.article_sections],
            'image': Image.to_json(structured_content.image)
        }
