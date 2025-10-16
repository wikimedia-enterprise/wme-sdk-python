from typing import List, Optional
from pydantic import BaseModel

from .structuredcontent import Link

class StructuredReferenceText(BaseModel):
    #Represents a formatted citation string from the bibliography
    
    #A formatted citation string from the bibliography.
    value: Optional[str] = None
    
    #Links associated with the source.
    links: Optional[str] = None