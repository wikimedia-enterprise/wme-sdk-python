class Editor:
    """
    Editor representation.
    """

    def __init__(self, name=None, experience=None):
        """
        Initialize Editor instance.

        :param name: The name of the editor.
        :param experience: The experience level of the editor.
        """
        self.name = name
        self.experience = experience

    def to_dict(self):
        """
        Convert the Editor instance to a dictionary.
        """
        return {
            "name": self.name,
            "experience": self.experience
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create an Editor instance from a dictionary.
        """
        return cls(
            name=data.get("name"),
            experience=data.get("experience")
        )
