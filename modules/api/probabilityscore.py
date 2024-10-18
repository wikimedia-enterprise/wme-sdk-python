from typing import Optional
from scores import Probability


class ProbabilityScore:
    def __init__(self,
                 prediction: Optional[bool] = None,
                 probability: Optional[Probability] = None):
        self.prediction = prediction
        self.probability = probability

    @staticmethod
    def from_json(data: dict) -> 'ProbabilityScore':
        return ProbabilityScore(
            prediction=data['prediction'],
            probability=Probability.from_json(data['probability'])
        )

    @staticmethod
    def to_json(self) -> dict:
        return {
            'prediction': self.prediction,
            'probability': self.probability.to_json()
        }
