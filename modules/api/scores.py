from typing import Optional
from exceptions import DataModelError


class Probability:
    def __init__(self,
                 false: Optional[float] = None,
                 true: Optional[float] = None):
        self.false = false
        self.true = true

    @staticmethod
    def from_json(data: dict) -> 'Probability':
        if not isinstance(data, dict):
            raise DataModelError(f"Expected a dict for Probability data, but got {type(data).__name__}")
        
        try:
            return Probability(
                false=data.get('false'),
                true=data.get('true')
            )
        except (KeyError, TypeError) as e:
            raise DataModelError(f"Failed to parse Probability data: {e}") from e

    @staticmethod
    def to_json(probability: 'Probability') -> dict:
        return {
            'false': probability.false,
            'true': probability.true
        }


class ProbabilityScore:
    def __init__(self,
                 prediction: Optional[bool] = None,
                 probability: Optional[Probability] = None):
        self.prediction = prediction
        self.probability = probability

    @staticmethod
    def from_json(data: dict) -> 'ProbabilityScore':
        if not isinstance(data, dict):
            raise DataModelError(f"Expected a dict for ProbabilityScore data, but got {type(data).__name__}")
        
        try:
            return ProbabilityScore(
                prediction=data.get('prediction'),
                probability=Probability.from_json(p_data) if (p_data := data.get('probability')) else None
            )
        except (KeyError, TypeError, DataModelError) as e:
            raise DataModelError(f"Failed to parse ProbabilityScore data: {e}") from e

    @staticmethod
    def to_json(probability_score: 'ProbabilityScore') -> dict:
        return {
            'prediction': probability_score.prediction,
            'probability': Probability.to_json(probability_score.probability) if probability_score.probability else None
        }

class Scores:
    def __init__(self,
                 revert_risk: Optional[ProbabilityScore] = None):
        self.revert_risk = revert_risk

    @staticmethod
    def from_json(data: dict) -> 'Scores':
        if not isinstance(data, dict):
            raise DataModelError(f"Expected a dict for Scores data, but got {type(data).__name__}")
        
        try:
            return Scores(
                revert_risk=ProbabilityScore.from_json(rr_data) if (rr_data := data.get('revert_risk')) else None
            )
        except (KeyError, TypeError, DataModelError) as e:
            raise DataModelError(f"Failed to parse Scores data: {e}") from e

    @staticmethod
    def to_json(scores: 'Scores') -> dict:
        return {
            'revert_risk': ProbabilityScore.to_json(scores.revert_risk) if scores.revert_risk else None
        }
