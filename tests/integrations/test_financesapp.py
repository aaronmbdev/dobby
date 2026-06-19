from unittest import TestCase

from src.integrations.finances.financesapp import FinancesAppClient


class TestFinancesAppClient(TestCase):
    def test_get_accounts(self):
        client = FinancesAppClient()
        account_balance = client.get_accounts()
        assert isinstance(account_balance, list)