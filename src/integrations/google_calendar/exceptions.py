from src.integrations.exceptions import IntegrationException


class GoogleCalendarError(IntegrationException):
    """Raised when a Google Calendar API call fails."""
    pass


class GoogleCalendarNotConfiguredError(IntegrationException):
    """Raised when Google Calendar credentials are absent from settings."""
    pass
