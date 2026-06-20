from src.integrations.exceptions import IntegrationException


class FinanceIntegrationError(IntegrationException):
    """Base exception for finance integration errors."""
    pass