from pydantic import BaseModel

#Represents the structured response data for the reference-need Liftwing API.
class ReferenceNeedData(BaseModel):
    #estimates the likelihood that a statement requires citation.
    reference_need_score: float