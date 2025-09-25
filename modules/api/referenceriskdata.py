from pydantic import BaseModel

#Represents the structured response data for the reference-risk Liftwing API.
class ReferenceRiskData(BaseModel):
    #Quantifies the proportion of deprecated/blacklisted domains.
    reference_risk_score: float