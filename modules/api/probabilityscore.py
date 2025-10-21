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
        """
        Deserializes a dictionary into a ProbabilityScore instance.

        This method also deserializes the nested 'probability' object.

        Args:
            data: A dictionary containing the prediction and probability data.

        Returns:
            A ProbabilityScore instance.

        Raises:
            DataModelError: If the input is not a dict or if parsing fails
                            (e.g., missing keys, nested object parsing error).
        """
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
        """
        Serializes the ProbabilityScore instance into a JSON-compatible dictionary.

        This method also serializes the nested 'probability' object.

        Args:
            prob_score: The ProbabilityScore instance to serialize.

        Returns:
            A dictionary representation of the probability score.
        """
        return {
            'prediction': prob_score.prediction,
            'probability': Probability.to_json(prob_score.probability) if prob_score.probability else None
        }
