import httpx

from src.config.settings import settings
from src.integrations.finances.exceptions import FinanceIntegrationError


class FinancesAppClient:

    def __init__(self):

        self.client = httpx.Client(
            base_url=settings.finances_url,
            headers={
                "Content-Type": "application/json",
            },
            follow_redirects=True,
        )


    def get_accounts(self) -> dict:
        """
        Fetches the list of accounts from the FinancesApp API.
        :return: A list of dicts with: description, id, latestBalance, latestBalanceDate, name
        """
        try:
            return self._make_get_request("/api/v1/accounts")
        except httpx.HTTPError as e:
            raise FinanceIntegrationError(f"Error fetching accounts: {e}") from e


    def get_stocks(self):
        """
        Fetches the list of stocks from the FinancesApp API.
        :return: A list of dicts with id, latestDate, latestPriceEur, latestShares, name, ticker
        """
        try:
            return self._make_get_request("/api/v1/investments/stocks")
        except httpx.HTTPError as e:
            raise FinanceIntegrationError(f"Error fetching stocks: {e}") from e


    def get_investment_funds(self):
        """
        Fetches the list of investment funds from the FinancesApp API.
        :return: A list of dicts with id, isin, latestDate, latestPriceEur, latestShares, name, yahooticker
        """
        try:
            return self._make_get_request("/api/v1/investments/funds")
        except httpx.HTTPError as e:
            raise FinanceIntegrationError(f"Error fetching investment funds: {e}") from e


    def get_net_worth_history(self):
        """
        Fetches the net worth history from the FinancesApp API.
        :return: A list of dicts with date, accountsTotal, fundsTotal, stocksTotal, total
        """
        try:
            return self._make_get_request("/api/v1/networth/history")
        except httpx.HTTPError as e:
            raise FinanceIntegrationError(f"Error fetching net worth history: {e}") from e


    def get_health_metrics(self):
        """
        Fetches the health metrics from the FinancesApp API.
        :return: A dict with various metrics:
        averageMonthlyIncome, essentialMonthlyBurn, totalAccountBalance, totalMonthlyBurn
        debtToIncome(structure with currentValue, healthLevel, history(month, value))
        emergencyFund(structure with currentValue, healthLevel, history(month, value))
        expenseDistribution(structure with categoryName, averageMonthly)
        expenseGrowthRate(structure with currentValue, healthLevel, history(month, value))
        fixedVsVariable(structure with currentValue, healthLevel, history(month, value))
        housingRatio(structure with currentValue, healthLevel, history(month, value))
        investmentRatio(structure with currentValue, healthLevel, history(month, value))
        savingsRate(structure with currentValue, healthLevel, history(month, value))
        """
        try:
            return self._make_get_request("/api/v1/health-metrics")
        except httpx.HTTPError as e:
            raise FinanceIntegrationError(f"Error fetching health metrics: {e}") from e


    def get_report_by_date(self, date: str):
        """
        Fetches the report for a specific date from the FinancesApp API.
        :param date: The date in YYYY-MM format.
        :return: struct(data, hasData)
        In data: categories, expenses, income, overview
        categories(dict with name, totalExpensed)
        expenses(list of dicts with date, period, description, categoryId, amount)
        income(list of dicts with liquido)
        overview(list of dicts with balance, monthlyExpenses, monthlyIncome)
        """
        try:
            return self._make_get_request(f"/api/v1/reports/{date}")
        except httpx.HTTPError as e:
            raise FinanceIntegrationError(f"Error fetching report for {date}: {e}") from e


    def _make_get_request(self, endpoint: str) -> dict:
        response = self.client.get(endpoint)
        response.raise_for_status()
        return response.json()