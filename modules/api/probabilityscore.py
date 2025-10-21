# pylint: disable=R0801
"""Contains a probability score's boolean prediction along with the underlying probability scores that led to that prediction."""

from typing import Optional
from .scores import Probability
from .exceptions import DataModelError


class ProbabilityScore:
    """Contains a probability score's boolean prediction along with the underlying probability scores that led to that prediction."""
    def __init__(self,
                 prediction: Optional[bool] = None,
                 probability: Optional[Probability] = None):
        self.prediction = prediction
        self.probability = probability

    @staticmethod
    def from_json(data: dict) -> 'ProbabilityScore':
        """Constructs a ProbabilityScore object from a dictionary representation."""
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
        """Converts a ProbabilityScore instance into a dictionary for serialization."""
        return {
            'prediction': prob_score.prediction,
            'probability': Probability.to_json(prob_score.probability) if prob_score.probability else None
        }
