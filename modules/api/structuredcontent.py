from typing import List, Optional, Dict
from datetime import datetime
from modules.api.article import Image
from version import Version
from entity import Entity
from project import Project
from language import Language


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

    @staticmethod
    def to_json(link: 'Link') -> dict:
        return {
            'url': link.url,
            'text': link.text,
            'images': [Image.to_json(image) for image in link.images]
        }

class Citation:
    def __init__(self,
                 identifier: Optional[str] = None,
                 group: Optional[str] = None,
                 text: Optional[str] = None):
        self.identifier = identifier
        self.group = group
        self.text = text

    @staticmethod
    def from_json(data: dict) -> 'Citation':
        return Citation(
            identifier=data.get('identifier', ""),
            group=data.get('group', ""),
            text=data.get('text', "")
        )

    @staticmethod
    def to_json(citation: 'Citation') -> dict:
        return {
            'identifier': citation.identifier,
            'group': citation.group,
            'text': citation.text
        }

class Part:
    def __init__(self,
                 name: Optional[str] = None,
                 part_type: Optional[str] = None,
                 value: Optional[str] = None,
                 values: Optional[List[str]] = None,
                 images: Optional[List[Image]] = None,
                 links: Optional[List[Link]] = None,
                 has_parts: Optional[List['Part']] = None,
                 citations: Optional[List[Citation]] = None):
        self.name = name
        self.part_type = part_type
        self.value = value
        self.values = values or []
        self.images = images or []
        self.links = links or []
        self.has_parts = has_parts or []
        self.citations = citations or []

    @staticmethod
    def from_json(data: dict) -> 'Part':
        return Part(
            name=data['name'],
            part_type=data['type'],
            value=data['value'],
            values=data['values'],
            images=[Image.from_json(image) for image in data['images']],
            links=[Link.from_json(link) for link in data['links']],
            has_parts=[Part.from_json(part) for part in data['hasParts']],
            citations=[Citation.from_json(citation) for citation in data['citations']]
        )

    @staticmethod
    def to_json(part: 'Part') -> dict:
        return {
            'name': part.name,
            'type': part.part_type,
            'value': part.value,
            'values': part.values,
            'images': [Image.to_json(image) for image in part.images],
            'links': [Link.to_json(link) for link in part.links],
            'hasParts': [Part.to_json(sub_part) for sub_part in part.has_parts],
            'citations': [Citation.to_json(citation) for citation in part.citations]
        }

class ReferenceText:
    def __init__(self,
                 value: Optional[str] = None,
                 links: Optional[List[Link]] = None):
        self.value = value
        self.links = links or []

    @staticmethod
    def from_json(data: dict) -> 'ReferenceText':
        return ReferenceText(
            value=data.get('value', ""),
            links=[Link.from_json(link) for link in data.get('links', [])]
        )

    @staticmethod
    def to_json(text: 'ReferenceText') -> dict:
        return {
            'value': text.value,
            'links': [Link.to_json(link) for link in text.links]
        }

class Reference:
    def __init__(self,
                 identifier: Optional[str] = "",
                 group: Optional[str] = "",
                 ref_type: Optional[str] = "",
                 metadata: Optional[Dict[str, str]] = None,
                 text: Optional[ReferenceText] = None,
                 source: Optional[ReferenceText] = None):
        self.identifier = identifier
        self.group = group
        self.ref_type = ref_type
        self.metadata = metadata or {}
        self.text = text
        self.source = source

    @staticmethod
    def from_json(data: dict) -> 'ReferenceText':
        return ReferenceText(
            identifier=data.get('identifier', ""),
            group=data.get('group', ""),
            ref_type=data.get('type', ""),
            metadata=data.get('metadata', {}),
            text=ReferenceText.from_json(data.get('text')),
            source=ReferenceText.from_json(data.get('source'))
        )

    @staticmethod
    def to_json(reference: 'ReferenceText') -> dict:
        return {
            'identifier': reference.identifier,
            'group': reference.group,
            'type': reference.ref_type,
            'metadata': reference.metadata,
            'text': ReferenceText.to_json(reference.text),
            'source': ReferenceText.to_json(reference.source)
        }


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
                 infoboxes: Optional[List[Part]] = None,
                 article_sections: Optional[List[Part]] = None,
                 image: Optional[Image] = None,
                 references: Optional[List[Reference]] = None):
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
        self.infoboxes = infoboxes or []
        self.article_sections = article_sections or []
        self.image = image
        self.references = references or []

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
            infoboxes=[Part.from_json(part) for part in data['infoboxes']],
            article_sections=[Part.from_json(section) for section in data['articleSections']],
            image=Image.from_json(data['image']),
            references=[Reference.from_json(reference) for reference in data.get('references', [])]
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
            'infoboxes': [Part.to_json(part) for part in structured_content.infoboxes],
            'articleSections': [Part.to_json(section) for section in structured_content.article_sections],
            'image': Image.to_json(structured_content.image),
            'references': [Reference.to_json(reference) for reference in structured_content.references]
        }
