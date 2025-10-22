"""Represents a formatted citation string from the bibliography"""

from typing import Optional
from pydantic import BaseModel

class StructuredReferenceText(BaseModel):
    """Represents the elements of a formatted citation string from the bibliography"""

    #A formatted citation string from the bibliography.
    value: Optional[str] = None

    #Links associated with the source.
    links: Optional[str] = None
