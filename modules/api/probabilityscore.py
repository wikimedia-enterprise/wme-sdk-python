class ProbabilityScore:
    """
    ProbabilityScore representation.
    """

    def __init__(self, likelihood=None, impact=None):
        """
        Initialize ProbabilityScore instance.

        :param likelihood: The likelihood score.
        :param impact: The impact score.
        """
        self.likelihood = likelihood
        self.impact = impact

    def to_dict(self):
        """
        Convert the ProbabilityScore instance to a dictionary.
        """
        return {
            "likelihood": self.likelihood,
            "impact": self.impact
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a ProbabilityScore instance from a dictionary.
        """
        return cls(
            likelihood=data.get("likelihood"),
            impact=data.get("impact")
        )
