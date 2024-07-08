class Visibility:
    """
    Visibility representation.
    """

    def __init__(self, public=None, protected=None, private=None):
        """
        Initialize Visibility instance.

        :param public: Indicates if the entity is public.
        :param protected: Indicates if the entity is protected.
        :param private: Indicates if the entity is private.
        """
        self.public = public
        self.protected = protected
        self.private = private

    def to_dict(self):
        """
        Convert the Visibility instance to a dictionary.
        """
        return {
            "public": self.public,
            "protected": self.protected,
            "private": self.private
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Visibility instance from a dictionary.
        """
        return cls(
            public=data.get("public"),
            protected=data.get("protected"),
            private=data.get("private")
        )
