class Size:
    """
    Size representation according to https://schema.org/QuantitativeValue.
    """

    def __init__(self, value=None, unit_text=None):
        """
        Initialize Size instance.

        :param value: The size value.
        :param unit_text: The unit of the size value (e.g., 'MB').
        """
        self.value = value
        self.unit_text = unit_text

    def to_dict(self):
        """
        Convert the Size instance to a dictionary.
        """
        return {
            "value": self.value,
            "unit_text": self.unit_text
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Size instance from a dictionary.
        """
        return cls(
            value=data.get("value"),
            unit_text=data.get("unit_text")
        )
