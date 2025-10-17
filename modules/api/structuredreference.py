"""Represents a structured source linked to citations, containing metadata and formatted text for verification."""

from typing import Dict, Optional
from pydantic import BaseModel, Field

from .structuredreferencetext import StructuredReferenceText

class StructuredReference(BaseModel):
    """Represents a structured source linked to citations, containing metadata and formatted text for verification."""

    # A unique identifier for the article.
    identifier: Optional[str] = None

    # The reference group.
    group: Optional[str] = None

    # The type of reference.
    reference_type: Optional[str] = Field(alias="type", default="None")

    # Additional structured details like author, publisher, year, etc.
    metadata: Optional[Dict[str, str]] = None

    # The reference as it appears in the article.
    text: Optional[StructuredReferenceText] = None

    # If the reference is from a bibliography, this stores its original source details.
    source: Optional[StructuredReferenceText] = None
