from typing import Optional
from pydantic import BaseModel

class StructuredCitation(BaseModel):
    #Represents a collection of inline citations within an article, linking specific content to corresponding references.
    
    #Unique identifier for the article
    identifier: Optional[str] = None
    
    #The reference group
    group: Optional[str] = None
    
    #The inline citation as it appears in the article
    text: Optional[str] = None