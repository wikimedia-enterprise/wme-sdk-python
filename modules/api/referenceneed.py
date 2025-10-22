"""Represents the likelihood of a ReferenceNeeded"""

from pydantic import BaseModel

class ReferenceNeedData(BaseModel):
    """Represents the structured response data for the reference-need Liftwing API."""
    # Estimates the likelihood that a statement requires citation.
    reference_need_score: float
