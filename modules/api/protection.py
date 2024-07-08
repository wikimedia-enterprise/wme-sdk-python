class Protection:
    """
    Protection representation.
    """

    def __init__(self, firewall_enabled=None, antivirus_enabled=None):
        """
        Initialize Protection instance.

        :param firewall_enabled: Indicates if the firewall is enabled.
        :param antivirus_enabled: Indicates if the antivirus is enabled.
        """
        self.firewall_enabled = firewall_enabled
        self.antivirus_enabled = antivirus_enabled

    def to_dict(self):
        """
        Convert the Protection instance to a dictionary.
        """
        return {
            "firewall_enabled": self.firewall_enabled,
            "antivirus_enabled": self.antivirus_enabled
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Protection instance from a dictionary.
        """
        return cls(
            firewall_enabled=data.get("firewall_enabled"),
            antivirus_enabled=data.get("antivirus_enabled")
        )
