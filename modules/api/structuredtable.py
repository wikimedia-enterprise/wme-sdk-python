from typing import List, Optional
from pydantic import BaseModel

class StructuredTable(BaseModel):
    #Represents a structured table
    
    #Identifier is a unique string that identifies the structured table.
    identifier: Optional[str] = None
    
    #Headers contain the header cells of the table
    headers: Optional[List[List[Optional['StructuredTableCell']]]] = None
    
    #Rows contain the main body cells of the table
    rows: Optional[List[List[Optional['StructuredTableCell']]]] = None
    
    #Footers contain the footer cells of the table.
    footers: Optional[List[List[Optional['StructuredTableCell']]]] = None
    
    #ConfidenceScore indicates the confidence (between 0.0 and 1.0)
    confidence_score: Optional[float] = None
    
class StructuredTableCell(BaseModel):
    #Represents a singl cell in a structured table
    
    #Value is the textual content of the cell.
    value: Optional[str] = None
    
    #NestedTable represents a table contained within this cell, if present.
    nested_table: Optional[StructuredTable] = None
    
#In Pydantic V2, resolving forward reference from StructuredTable to StructuredTableCell is handled automatically. In older version, we might explicitly call model_rebuild()
StructuredTable.model_rebuild()