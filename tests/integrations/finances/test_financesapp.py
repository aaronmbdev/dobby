from unittest import TestCase

from src.integrations.finances.financesapp import FinancesAppClient
from src.integrations.finances.models import FinanceHealthMetrics, MonthlyReport


class TestFinancesAppClient(TestCase):
    def test_get_accounts(self):
        client = FinancesAppClient()
        account_balance = client.get_accounts()
        assert isinstance(account_balance, list)

    def test_get_stocks(self):
        client = FinancesAppClient()
        stocks = client.get_stocks()
        assert isinstance(stocks, list)

    def test_get_investment_funds(self):
        client = FinancesAppClient()
        funds = client.get_investment_funds()
        assert isinstance(funds, list)

    def test_get_metrics(self):
        client = FinancesAppClient()
        metrics = client.get_health_metrics()
        assert isinstance(metrics, FinanceHealthMetrics)

    def test_get_reports(self):
        client = FinancesAppClient()
        reports = client.get_report_by_month("2026-03")
        assert isinstance(reports, MonthlyReport)