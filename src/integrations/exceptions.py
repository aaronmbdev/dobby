

class IntegrationException(Exception):
    """Base class for all integration exceptions."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message