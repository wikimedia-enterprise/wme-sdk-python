from typing import Optional


class Probability:
    def __init__(self,
                 false: Optional[float] = None,
                 true: Optional[float] = None):
        self.false = false
        self.true = true

    @staticmethod
    def from_json(data: dict) -> 'Probability':
        return Probability(
            false=data['false'],
            true=data['true'])

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
        return ProbabilityScore(
            prediction=data['prediction'],
            probability=Probability.from_json(data['probability'])
        )

    @staticmethod
    def to_json(probability_score: 'ProbabilityScore') -> dict:
        return {
            'prediction': probability_score.prediction,
            'probability': Probability.to_json(probability_score.probability)
        }

class Scores:
    def __init__(self,
                 revert_risk: Optional[ProbabilityScore] = None):
        self.revert_risk = revert_risk

    @staticmethod
    def from_json(data: dict) -> 'Scores':
        return Scores(
            revert_risk=ProbabilityScore.from_json(data['revert_risk'])
        )

    @staticmethod
    def to_json(scores: 'Scores') -> dict:
        return {
            'revert_risk': ProbabilityScore.to_json(scores.revert_risk)
        }
