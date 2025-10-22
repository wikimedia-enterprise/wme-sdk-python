"""Represents the structured response data for the reference-risk Liftwing API."""

from pydantic import BaseModel

class ReferenceRiskData(BaseModel):
    """Quantifies the proportion of deprecated/blacklisted domains."""
    reference_risk_score: float
