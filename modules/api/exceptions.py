class WikimediaAPIError(Exception):
    """Base exception class for this client."""
    pass

class APIRequestError(WikimediaAPIError):
    """Raised for network-level errors (e.g., connection refused, timeout)."""
    def __init__(self, message, request):
        super().__init__(message)
        self.request = request

class APIStatusError(WikimediaAPIError):
    """Raised for non-successful HTTP status codes (4xx or 5xx)."""
    def __init__(self, message, request, response):
        super().__init__(message)
        self.request = request
        self.response = response

class APIDataError(WikimediaAPIError):
    """Raised for errors during data processing (e.g., invalid JSON, corrupt archive)."""
    pass

class DataModelError(ValueError):
    """Raised when incoming data cannot be parsed into a data model"""
    pass