from typing import Optional
from scores import Probability
from exceptions import DataModelError


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
                prediction=data['prediction'],
                probability=Probability.from_json(data['probability'])
            )
        except (KeyError, TypeError, DataModelError) as e:
            raise DataModelError(f"Failed to parse ProbabilityScore data: {e}") from e

    @staticmethod
    def to_json(prob_score: 'ProbabilityScore') -> dict:
        return {
            'prediction': prob_score.prediction,
            'probability': Probability.to_json(prob_score.probability) if prob_score.probability else None
        }
