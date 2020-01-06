class ValidationError(Exception):
    """
    Base exception for errors coming from
    bad class attributes in `RandomGen`.
    """
    pass


class InvalidProbabilitiesError(ValidationError):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code


class LengthMismatchError(ValidationError):
    def __init__(self, code=1):
        super().__init__(
            "`RandomGen._probabilities` and `RandomGen._random_nums`"
            "should have the same length."
        )
        self.code = code
