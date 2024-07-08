class Scores:
    """
    Scores representation.
    """

    def __init__(self, attack_score=None, defense_score=None):
        """
        Initialize Scores instance.

        :param attack_score: The attack score.
        :param defense_score: The defense score.
        """
        self.attack_score = attack_score
        self.defense_score = defense_score

    def to_dict(self):
        """
        Convert the Scores instance to a dictionary.
        """
        return {
            "attack_score": self.attack_score,
            "defense_score": self.defense_score
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Scores instance from a dictionary.
        """
        return cls(
            attack_score=data.get("attack_score"),
            defense_score=data.get("defense_score")
        )
