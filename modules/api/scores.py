from typing import Optional


class Probability:
    def __init__(self,
                 false: Optional[float] = None,
                 true: Optional[float] = None):
        self.false = false
        self.true = true


class ProbabilityScore:
    def __init__(self,
                 prediction: Optional[bool] = None,
                 probability: Optional[Probability] = None):
        self.prediction = prediction
        self.probability = probability


class Scores:
    def __init__(self,
                 revert_risk: Optional[ProbabilityScore] = None):
        self.revert_risk = revert_risk
