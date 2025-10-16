from typing import List, Optional, Dict
from datetime import datetime
from modules.api.article import Image
from version import Version
from entity import Entity
from project import Project
from language import Language
from exceptions import DataModelError


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
        if not isinstance(data, dict):
            raise DataModelError(f"Expected dict for Link, got {type(data).__name__}")
        try:
            return Link(
                url=data['url'],
                text=data['text'],
                images=[Image.from_json(image) for image in data['images']]
            )
        except (TypeError, DataModelError) as e:
            raise DataModelError(f"Failed to parse Link data: {e}") from e

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
        if not isinstance(data, dict):
            raise DataModelError(f"Expected dict for Citation, got {type(data).__name__}")
        try:
            return Citation(
                identifier=data.get('identifier'),
                group=data.get('group'),
                text=data.get('text')
            )
        except (TypeError) as e:
            raise DataModelError(f"Failed to parse Citation data: {e}") from e

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
        if not isinstance(data, dict):
            raise DataModelError(f"Expected dict for Part, got {type(data).__name__}")
        try:
            return Part(
                name=data.get('name'),
                part_type=data.get('type'),
                value=data.get('value'),
                values=data.get('values'),
                images=[Image.from_json(image) for image in data.get('images', [])],
                links=[Link.from_json(link) for link in data.get('links', [])],
                has_parts=[Part.from_json(part) for part in data.get('has_parts', [])],
                citations=[Citation.from_json(citation) for citation in data.get('citations', [])]
            )
        except (TypeError, DataModelError) as e:
            part_name = data.get('name', 'N/A')
            raise DataModelError(f"Failed to parse Part '{part_name}': {e}") from e

    @staticmethod
    def to_json(part: 'Part') -> dict:
        return {
            'name': part.name,
            'type': part.part_type,
            'value': part.value,
            'values': part.values,
            'images': [Image.to_json(image) for image in part.images],
            'links': [Link.to_json(link) for link in part.links],
            'has_parts': [Part.to_json(sub_part) for sub_part in part.has_parts],
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
        if not isinstance(data, dict):
            raise DataModelError(f"Expected dict for ReferenceText, got {type(data).__name__}")
        try:
            return ReferenceText(
                value=data.get('value'),
                links=[Link.from_json(link) for link in data.get('links', [])]
            )
        except (TypeError, DataModelError) as e:
            raise DataModelError(f"Failed to parse ReferenceText: {e}") from e

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
    def from_json(data: dict) -> 'Reference':
        if not isinstance(data, dict):
            raise DataModelError(f"Expected dict for Reference, got {type(data).__name__}")
        try:
            return Reference(
                identifier=data.get('identifier'),
                group=data.get('group'),
                ref_type=data.get('type'),
                metadata=data.get('metadata'),
                text=ReferenceText.from_json(t_data) if (t_data := data.get('text')) else None,
                source=ReferenceText.from_json(s_data) if (s_data := data.get('source')) else None
            )
        except (TypeError, DataModelError) as e:
            ref_id = data.get('identifier', 'N/A')
            raise DataModelError(f"Failed to parse Reference '{ref_id}': {e}") from e

    @staticmethod
    def to_json(reference: 'Reference') -> dict:
        return {
            'identifier': reference.identifier,
            'group': reference.group,
            'type': reference.ref_type,
            'metadata': reference.metadata,
            'text': ReferenceText.to_json(reference.text) if reference.text else None,
            'source': ReferenceText.to_json(reference.source) if reference.source else None
        }

class StructuredTableCell:
    def __init__(self,
                 value: Optional[str] = None,
                 nested_table: Optional['StructuredTable'] = None):
        self.value = value
        self.nested_table = nested_table

    @staticmethod
    def from_json(data: dict) -> 'StructuredTableCell':
        if not isinstance(data, dict):
            raise DataModelError(f"Expected dict for StructuredTableCell, got {type(data).__name__}")
        try:
            return StructuredTableCell(
                value=data.get("value"),
                nested_table=StructuredTable.from_json(nt_data) if (nt_data := data.get("nested_table")) else None
            )
        except (TypeError, DataModelError) as e:
            raise DataModelError(f"Failed to parse StructuredTableCell: {e}") from e

    @staticmethod
    def to_json(cell: 'StructuredTableCell') -> dict:
        return {
            "value": cell.value,
            "nested_table": StructuredTable.to_json(cell.nested_table) if cell.nested_table else None
        }


class StructuredTable:
    def __init__(self,
                 identifier: Optional[str] = None,
                 headers: Optional[List[List['StructuredTableCell']]] = None,
                 rows: Optional[List[List['StructuredTableCell']]] = None,
                 footers: Optional[List[List['StructuredTableCell']]] = None,
                 confidence_score: Optional[float] = None):
        self.identifier = identifier
        self.headers = headers or []
        self.rows = rows or []
        self.footers = footers or []
        self.confidence_score = confidence_score

    @staticmethod
    def from_json(data: dict) -> 'StructuredTable':
        if not isinstance(data, dict):
            raise DataModelError(f"Expected dict for StructuredTable, got {type(data).__name__}")
        try:
            return StructuredTable(
                identifier=data.get("identifier"),
                headers=[[StructuredTableCell.from_json(c) for c in row] for row in data.get("headers", [])],
                rows=[[StructuredTableCell.from_json(c) for c in row] for row in data.get("rows", [])],
                footers=[[StructuredTableCell.from_json(c) for c in row] for row in data.get("footers", [])],
                confidence_score=data.get("confidence_score")
            )
        except (TypeError, DataModelError) as e:
            table_id = data.get('identifier', 'N/A')
            raise DataModelError(f"Failed to parse StructuredTable '{table_id}': {e}") from e

    @staticmethod
    def to_json(table: 'StructuredTable') -> dict:
        return {
            "identifier": table.identifier,
            "headers": [[StructuredTableCell.to_json(c) for c in row] for row in table.headers],
            "rows": [[StructuredTableCell.to_json(c) for c in row] for row in table.rows],
            "footers": [[StructuredTableCell.to_json(c) for c in row] for row in table.footers],
            "confidence_score": table.confidence_score
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
                 tables: Optional[List['StructuredTable']] = None,
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
        self.tables = tables or []

    @staticmethod
    def from_json(data: dict) -> 'StructuredContent':
        if not isinstance(data, dict):
            raise DataModelError(f"Expected dict for StructuredContent, got {type(data).__name__}")
        try:
            created_str = data.get('date_created')
            modified_str = data.get('date_modified')

            return StructuredContent(
                name=data.get('name'),
                identifier=data.get('identifier'),
                abstract=data.get('abstract'),
                description=data.get('description'),
                version=Version.from_json(v_data) if (v_data := data.get('version')) else None,
                url=data.get('url'),
                date_created=datetime.fromisoformat(created_str) if created_str else None,
                date_modified=datetime.fromisoformat(modified_str) if modified_str else None,
                main_entity=Entity.from_json(me_data) if (me_data := data.get('main_entity')) else None,
                additional_entities=[Entity.from_json(e) for e in data.get('additional_entities', [])],
                is_part_of=Project.from_json(p_data) if (p_data := data.get('is_part_of')) else None,
                in_language=Language.from_json(l_data) if (l_data := data.get('in_language')) else None,
                infoboxes=[Part.from_json(p) for p in data.get('infoboxes', [])],
                article_sections=[Part.from_json(s) for s in data.get('article_sections', [])],
                tables=[StructuredTable.from_json(t) for t in data.get('tables', [])],
                image=Image.from_json(i_data) if (i_data := data.get('image')) else None,
                references=[Reference.from_json(r) for r in data.get('references', [])]
            )
        except (ValueError, TypeError, DataModelError) as e:
            content_id = data.get('identifier', 'N/A')
            raise DataModelError(f"Failed to parse StructuredContent '{content_id}': {e}") from e

    @staticmethod
    def to_json(sc: 'StructuredContent') -> dict:
        return {
            'name': sc.name,
            'identifier': sc.identifier,
            'abstract': sc.abstract,
            'description': sc.description,
            'url': sc.url,
            'version': Version.to_json(sc.version) if sc.version else None,
            'date_created': sc.date_created.isoformat() if sc.date_created else None,
            'date_modified': sc.date_modified.isoformat() if sc.date_modified else None,
            'mainEntity': Entity.to_json(sc.main_entity) if sc.main_entity else None,
            'additional_entities': [Entity.to_json(e) for e in sc.additional_entities],
            'is_part_of': Project.to_json(sc.is_part_of) if sc.is_part_of else None,
            'inLanguage': Language.to_json(sc.in_language) if sc.in_language else None,
            'infoboxes': [Part.to_json(p) for p in sc.infoboxes],
            'article_sections': [Part.to_json(s) for s in sc.article_sections],
            'tables': [StructuredTable.to_json(t) for t in sc.tables],
            'image': Image.to_json(sc.image) if sc.image else None,
            'references': [Reference.to_json(r) for r in sc.references]
        }
